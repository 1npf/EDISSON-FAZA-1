from django.core.management.base import BaseCommand
from npf.contrib.dict.models import Bank

import os
import zipfile
import urllib.request
import dbfread
import lxml.html
import tempfile
import shutil


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run_bik_update()

    def get_cb_link(self, url):
        url = 'http://www.cbr.ru/mcirabis/?Prtid=bic'

        html = urllib.request.urlopen(url).read()
        doc = lxml.html.document_fromstring(html.decode('utf-8'))
        files = doc.cssselect('p.file.ZIP.small_icon')
        link = ''

        for file in files:
            if 'актуальный ' in file.text_content():
                link = file.cssselect('a')[0].attrib['href']
                break

        link = 'http://www.cbr.ru' + link
        return link

    def unzip_file(self, file_name, outpath):
        with open(file_name, 'rb') as f:
            z = zipfile.ZipFile(f)
            for name in z.namelist():
                z.extract(name, outpath)

    def save_main_banks(self, file_dir):
        regn_vs_id = {}
        table = dbfread.DBF(os.path.join(file_dir, 'BNKSEEK.dbf'), encoding='ibm866')
        for item in table:
            regn = item['REGN']
            name = item['NAMEP']
            bik = item['NEWNUM']
            if regn and '/' in regn:
                continue
            id = Bank.objects.create(name=name, bik=bik).id
            regn_vs_id[regn] = id
        return regn_vs_id

    def save_branches_banks(self, file_dir, regn_vs_id):
        table = dbfread.DBF(os.path.join(file_dir, 'BNKSEEK.dbf'), encoding='ibm866')
        for item in table:
            regn = item['REGN']
            name = item['NAMEP']
            bik = item['NEWNUM']
            if regn and '/' in regn:
                regn = regn.split('/')[0]
                id = regn_vs_id[regn]
                Bank.objects.create(
                    parent=Bank.objects.get(id=id), name=name, bik=bik
                )

    def run_bik_update(self):
        file_dir = tempfile.mkdtemp()
        file_name = tempfile.mktemp(dir=file_dir, suffix='.zip')

        try:
            url = 'http://www.cbr.ru/mcirabis/?Prtid=bic'

            print('Download file:')
            print('  Read {0}...'.format(url))
            link = self.get_cb_link(url)

            print('  Download {0}...'.format(link))
            urllib.request.urlretrieve(link, file_name)

            print('  Unzip file {0}...'.format(file_name))
            self.unzip_file(file_name, file_dir)

            print('Update banks:')
            print('  Clean old banks...')

            Bank.objects.all().delete()

            print('  Save banks...')
            regn_vs_id = self.save_main_banks(file_dir)

            print('  Save bank branches...')
            self.save_branches_banks(file_dir, regn_vs_id)

        finally:
            shutil.rmtree(file_dir)
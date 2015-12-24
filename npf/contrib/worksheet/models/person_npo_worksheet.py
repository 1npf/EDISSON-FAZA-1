from npf.contrib.worksheet.models import Worksheet


class PersonNpoWorksheet(Worksheet):

    class Meta:
        proxy = True
        verbose_name = 'Анкета ФЛ о НПО в свою пользу'
        verbose_name_plural = 'Реестр анкет ФЛ для заключения договоров о НПО в свою пользу'
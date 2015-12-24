from npf.contrib.worksheet.models import Worksheet


class PersonOpsWorksheet(Worksheet):

    class Meta:
        proxy = True
        verbose_name = 'Анкета ЗЛ о ОПС'
        verbose_name_plural = 'Реестр анкет ЗЛ для заключения договоров о ОПС'
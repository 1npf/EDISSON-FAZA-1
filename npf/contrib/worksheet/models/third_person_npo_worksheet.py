from npf.contrib.worksheet.models import Worksheet


class ThirdPersonNpoWorksheet(Worksheet):

    class Meta:
        proxy = True
        verbose_name = 'Анкета ФЛ о НПО в пользу 3-го лица'
        verbose_name_plural = 'Реестр анкет ФЛ для заключения договоров о НПО в пользу 3-го лица'
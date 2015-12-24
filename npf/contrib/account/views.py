import json

from django.http import HttpResponse
from django.views.generic import View

from npf.contrib.account.models import Operation, Account


class ProcessAccount(View):
    def get(self, request):
        # Account balance
        account_balance = request.GET.get('account_balance')
        if account_balance:
            balance = self._get_balance(account_balance)
            return HttpResponse(json.dumps({'success': True, 'balance': balance}), content_type='application/json')

        # Close account
        close_account = request.GET.get('close_account')
        if close_account:
            self._close_account(request)
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')

    def _close_account(self, request):
        account_number = request.GET.get('close_account')
        Account.objects.filter(number=account_number).update(state='c')

    def _get_balance(self, account_balance):
        account = Account.objects.get(number=account_balance)
        operations_credit = Operation.objects.filter(bill_credit=account)
        operations_debit = Operation.objects.filter(bill_debit=account)
        credit = sum([i.sum for i in operations_credit])
        debit = sum([i.sum for i in operations_debit])
        return debit - credit


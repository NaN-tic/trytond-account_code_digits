#This file is part account_code_digits module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['AccountTemplate', 'CreateChartAccount', 'CreateChart',
    'UpdateChartStart', 'UpdateChart']
__metaclass__ = PoolMeta


class AccountTemplate:
    __name__ = 'account.account.template'

    def _get_account_value(self, account=None):
        res = super(AccountTemplate, self)._get_account_value(account)
        Config = Pool().get('account.configuration')
        digits = Config.browse([1])[0].default_account_code_digits
        print res
        print res.get('code')
        print type(res.get('code'))
        if res.get('code') and res.get('kind') != 'view' and digits != None:
            digits = int(digits - len(res['code']))
            print type(digits)
            if digits > 0:
                if '%' in res['code']:
                    res['code'] = res['code'].replace('%', '0'*digits)
                else:
                    res['code'] = res['code'] + '0'*digits
        return res


class CreateChartAccount:
    __name__ = 'account.create_chart.account'

    account_code_digits = fields.Integer('Account Code Digits', readonly=True,
        help='Number of digits to be used for all non-view accounts. ' \
            '(Defined at Account/Account Configuration/Account Code Digits)')

    @staticmethod
    def default_account_code_digits():
        Config = Pool().get('account.configuration')
        config = Config.browse([1])[0]
        return config.default_account_code_digits


class CreateChart:
    __name__ = 'account.create_chart'

    def _action_create_account(self, datas):
        digits = datas['form']['account_code_digits']
        Config = Pool().get('account.configuration')
        Config.write(1, {
                'default_account_code_digits': digits
                })
        return super(CreateChartAccount, self)._action_create_account(datas)


class UpdateChartStart:
    __name__ = 'account.update_chart.start'

    account_code_digits = fields.Integer('Account Code Digits', readonly=True,
        help='Number of digits to be used for all non-view accounts. ' \
            '(Defined at Account/Account Configuration/Account Code Digits)')

    @staticmethod
    def default_account_code_digits():
        Config = Pool().get('account.configuration')
        config = Config.browse([1])[0]
        return config.default_account_code_digits


class UpdateChart:
    __name__ = 'account.update_chart'

    def _action_update_account(self, datas):
        digits = datas['form']['account_code_digits']
        Config = Pool().get('account.configuration')
        Config.write(1, {
                'default_account_code_digits': digits
                })
        return super(CreateChartAccount, self)._action_update_account(datas)

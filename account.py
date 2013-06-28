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
        if res.get('code') and res.get('kind') != 'view' and digits != None:
            digits = int(digits - len(res['code']))
            if digits > 0:
                if '%' in res['code']:
                    res['code'] = res['code'].replace('%', '0' * (digits + 1))
                else:
                    res['code'] = res['code'] + '0' * digits
        return res


class CreateChartAccount:
    __name__ = 'account.create_chart.account'

    account_code_digits = fields.Integer('Account Code Digits',
        help='Number of digits to be used for all non-view accounts.')

    @staticmethod
    def default_account_code_digits():
        config = Pool().get('account.configuration').get_singleton()
        return config.default_account_code_digits if config else None


class CreateChart:
    __name__ = 'account.create_chart'

    def transition_create_account(self):
        digits = self.account.account_code_digits
        Config = Pool().get('account.configuration')
        config = Config.get_singleton() or Config()
        config.default_account_code_digits = digits
        config.save()
        return super(CreateChart, self).transition_create_account()


class UpdateChartStart:
    __name__ = 'account.update_chart.start'

    account_code_digits = fields.Integer('Account Code Digits',
        help='Number of digits to be used for all non-view accounts.')

    @staticmethod
    def default_account_code_digits():
        config = Pool().get('account.configuration').get_singleton()
        return config.default_account_code_digits if config else None


class UpdateChart:
    __name__ = 'account.update_chart'

    def transition_update(self, datas):
        digits = self.start.account_code_digits
        Config = Pool().get('account.configuration')
        config = Config.get_singleton() or Config()
        config.default_account_code_digits = digits
        config.save()
        return super(UpdateChart, self).transition_update()

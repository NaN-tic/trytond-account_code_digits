#This file is part account_code_digits module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['AccountTemplate', 'Account', 'CreateChartAccount', 'CreateChart',
    'UpdateChartStart', 'UpdateChart']


class AccountTemplate:
    __metaclass__ = PoolMeta
    __name__ = 'account.account.template'

    def _get_account_value(self, account=None):
        res = super(AccountTemplate, self)._get_account_value(account)
        Config = Pool().get('account.configuration')
        digits = Config.browse([1])[0].default_account_code_digits
        if res.get('code') and res.get('kind') != 'view' and digits != None:
            digits = int(digits - len(res['code']))
            if '%' in res['code']:
                res['code'] = res['code'].replace('%', '0' * (digits + 1))
            else:
                res['code'] = res['code'] + '0' * digits
        # Don't upgrade code if the correct digits value is computed
        if account and res.get('code', '') == account.code:
            del res['code']
        return res


class Account:
    __metaclass__ = PoolMeta
    __name__ = 'account.account'

    @classmethod
    def __setup__(cls):
        super(Account, cls).__setup__()
        cls._error_messages.update({
                'invalid_code_digits': ('The number of code digits '
                    '%(account_digits)d of account "%(account)s" must be '
                    '%(digits)d.'),
                })

    @classmethod
    def validate(cls, accounts):
        config = Pool().get('account.configuration').get_singleton()
        super(Account, cls).validate(accounts)
        if (config and config.default_account_code_digits and
                config.force_digits):
            for account in accounts:
                account.check_digits(config.default_account_code_digits)

    def check_digits(self, digits):
        #Only the first item of code is checked: "570000 (1)" -> "570000"
        code = self.code.split(' ')[0]
        if self.kind != 'view' and len(code) != digits:
            self.raise_user_error('invalid_code_digits', error_args={
                    'account_digits': len(code),
                    'account': self.rec_name,
                    'digits': digits,
                    })


class CreateChartAccount:
    __metaclass__ = PoolMeta
    __name__ = 'account.create_chart.account'

    account_code_digits = fields.Integer('Account Code Digits',
        help='Number of digits to be used for all non-view accounts.')

    @staticmethod
    def default_account_code_digits():
        config = Pool().get('account.configuration').get_singleton()
        return config.default_account_code_digits if config else None


class CreateChart:
    __metaclass__ = PoolMeta
    __name__ = 'account.create_chart'

    def transition_create_account(self):
        if hasattr(self.account, 'account_code_digits'):
            digits = self.account.account_code_digits
            Config = Pool().get('account.configuration')
            config = Config.get_singleton() or Config()
            config.default_account_code_digits = digits
            config.save()
        return super(CreateChart, self).transition_create_account()


class UpdateChartStart:
    __metaclass__ = PoolMeta
    __name__ = 'account.update_chart.start'

    account_code_digits = fields.Integer('Account Code Digits',
        help='Number of digits to be used for all non-view accounts.')

    @staticmethod
    def default_account_code_digits():
        config = Pool().get('account.configuration').get_singleton()
        return config.default_account_code_digits if config else None


class UpdateChart:
    __metaclass__ = PoolMeta
    __name__ = 'account.update_chart'

    def transition_update(self):
        digits = self.start.account_code_digits
        Config = Pool().get('account.configuration')
        config = Config.get_singleton() or Config()
        config.default_account_code_digits = digits
        config.save()
        return super(UpdateChart, self).transition_update()

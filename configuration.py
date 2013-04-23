#This file is part account_code_digits module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


__all__ = ['Configuration']
__metaclass__ = PoolMeta


class Configuration:
    __name__ = 'account.configuration'

    default_account_code_digits = fields.Property(
        fields.Numeric('Account Code Digits', digits=(16, 0),
            help='Number of digits to be used for all non-view accounts.'))


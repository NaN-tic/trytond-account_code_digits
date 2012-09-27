#This file is part account_code_digits module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval, Bool


class Configuration(ModelSingleton, ModelSQL, ModelView):
    _name = 'account.configuration'

    default_account_code_digits = fields.Numeric('Account Code Digits', digits=(16, 0),
            help='Number of digits to be used for all non-view accounts.')

Configuration()

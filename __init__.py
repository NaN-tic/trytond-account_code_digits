#This file is part account_code_digits module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.pool import Pool
from .account import *
from .configuration import *

def register():
    Pool.register(
        Configuration,
        AccountTemplate,
        CreateChartAccount,
        UpdateChartStart,
        module='account_code_digits', type_='model')
    Pool.register(
        CreateChart,
        UpdateChart,
        module='account_code_digits', type_='wizard')

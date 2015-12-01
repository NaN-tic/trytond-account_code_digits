# This file is part of the account_code_digits module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountCodeDigitsTestCase(ModuleTestCase):
    'Test Account Code Digits module'
    module = 'account_code_digits'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountCodeDigitsTestCase))
    return suite
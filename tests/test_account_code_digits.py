# This file is part of the account_code_digits module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import doctest
import unittest
import trytond.tests.test_tryton
from trytond.exceptions import UserError
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction


class AccountCodeDigitsTestCase(ModuleTestCase):
    'Test Account Code Digits module'
    module = 'account_code_digits'

    def setUp(self):
        super(AccountCodeDigitsTestCase, self).setUp()
        self.account = POOL.get('account.account')
        self.config = POOL.get('account.configuration')

    def test0010_force_digits(self):
        'Test force digits'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            config = self.config.get_singleton() or self.config()
            config.default_account_code_digits = 6
            config.force_digits = True
            config.save()

            view, = self.account.search([
                    ('kind', '=', 'view'),
                    ], limit=1)
            non_view,  = self.account.search([
                    ('kind', '!=', 'view'),
                    ], limit=1)

            self.assertRaises(UserError, self.account.write, [non_view],
                {'code': '000'})
            self.account.write([view], {'code': '0'})
            self.account.write([non_view], {'code': '000000'})
            self.assertEqual(view.code, '0')
            self.assertEqual(non_view.code, '000000')
            config.force_digits = False
            config.save()
            self.account.write([non_view], {'code': '0000'})
            self.assertEqual(non_view.code, '0000')


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.account.tests import test_account
    for test in test_account.suite():
        if test not in suite and not isinstance(test, doctest.DocTestCase):
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountCodeDigitsTestCase))
    return suite

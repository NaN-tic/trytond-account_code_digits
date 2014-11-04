#!/usr/bin/env python
# This file is part account_code_digits module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction


class AccountCodeDigitsTestCase(unittest.TestCase):
    'Test AccountCodeDigits module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('account_code_digits')
        self.account = POOL.get('account.account')
        self.config = POOL.get('account.configuration')

    def test0005views(self):
        'Test views'
        test_view('account_code_digits')

    def test0006depends(self):
        'Test depends'
        test_depends()

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

            self.assertRaises(Exception, self.account.write, [non_view],
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
        #Skip doctest
        class_name = test.__class__.__name__
        if test not in suite and class_name != 'DocFileCase':
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountCodeDigitsTestCase))
    return suite

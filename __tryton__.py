#This file is part account_code_digits module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
{
    'name': 'Account Code Digits',
    'version': '2.5.0',
    'author': 'NaN·tic',
    'email': 'info@nan-tic.com',
    'website': 'http://www.nan-tic.com/',
    'description': '''Adds the possibility to set the number of digits to be 
used for account codes.''',
    'depends': [
        'ir',
        'res',
        'company',
        'party',
        'currency',
        'account',
    ],
    'xml': [
        'account.xml',
        'configuration.xml',
    ],
    'translation': [
        'locale/ca_ES.po',
        'locale/es_ES.po',
    ],
}

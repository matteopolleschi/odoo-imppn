# -*- coding: utf-8 -*-
{
    'name': "odoo-imppn",

    'summary': "Financial and Analytic Accounting",
    'description': "Module build to export invoices (active and passive) to an accounting system format (python library)",

    'author': "Mounir LAHSINI",
    'website': "http://www.github.com/matteopolleschi/odoo-imppn",

    'category': 'Accounting & Finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_accountant'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

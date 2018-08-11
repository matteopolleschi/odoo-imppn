# -*- coding: utf-8 -*-
{
    'name': "Odoo imppn",

    'summary': "Financial and Analytic Accounting",

    'description': "Module build to export invoices (active and passive) to an accounting system format (python library)",

    'author': "Jothimani R",
    'website': "http://www.github.com/matteopolleschi/odoo_imppn",
    'category': 'Accounting & Finance',
    'version': '0.1',

    'depends': ['web','base','account_accountant'],

    'data': [
        'views.xml',
        'wizard/account_invoice_export_imppn_views.xml'
    ],
}
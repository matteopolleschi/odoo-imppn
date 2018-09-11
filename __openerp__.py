# -*- coding: utf-8 -*
#
#    Copyright 2018 Matteo Polleschi <yes@daphne-solutions.com>
#    Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#    Copyright 2018 Odoo Italia Associazione <https://odoo-italia.org/>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#-
{
    'name': "Odoo imppn",

    'summary': "Financial and Analytic Accounting",

    'description': "Module build to export invoices (active and passive) to an accounting system format (python library)",

    'author': "Jothimani R",
    'website': "http://www.github.com/matteopolleschi/odoo_imppn",
    'category': 'Accounting & Finance',
    'version': '0.1',

    'depends': ['web',
                'base',
                'account_accountant',
                'account_invoice_entry_date'],
    'data': [
        'views/res_company_view.xml',
        'wizard/account_invoice_export_imppn_views.xml'
    ],
    'external_dependencies': {
        'python': [
            'fixedwidth',
        ],
    },

}
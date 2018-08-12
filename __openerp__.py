# -*- coding: utf-8 -*-
{
    'name': "Odoo imppn",
    'sequence': 2,

    'summary': "Financial and Analytic Accounting",
    'description': "Module build to export invoices (active and passive) to an accounting system format (python library)",

    'author': "Mounir LAHSINI",
    'website': "http://www.github.com/matteopolleschi/odoo_imppn",

    'category': 'Accounting & Finance',
    'version': '1.0',
    
    # any module necessary for this one to work correctly
    'depends': ['base','account','account_accountant'],

    # always loaded
    'data': [
        #'security/security.xml',
        #'security/ir.model.access.csv',
        'templates.xml',
        'views/odoo_imppn_view.xml',
        'views/company_imppn.xml',
    ],

    # only loaded in demonstration mode
    'demo': ['demo.xml'],
    
    # installation statue 
    'auto_install': False,
    'installable': True,
    'application': True,

     # module external dependencies
    'external_dependencies': {
        'python': [],
    },
}

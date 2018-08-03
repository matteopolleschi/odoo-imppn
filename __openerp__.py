# -*- coding: utf-8 -*-
{
    'name': "Odoo imppn",

    'summary': "Financial and Analytic Accounting",
    'description': "Module build to export invoices (active and passive) to an accounting system format (python library)",

    'author': "Mounir LAHSINI",
    'website': "http://www.github.com/matteopolleschi/odoo_imppn",

    'category': 'Accounting & Finance',
    'version': '1.0.8',
    
    # any module necessary for this one to work correctly
    'depends': ['web','base','account_accountant'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'templates.xml',
        'views/odoo_imppn.xml',
        'views/company_imppn.xml',
    ],

    # always loaded
    'qweb' : [
        'static/src/xml/*.xml',
    ],
    
    # installation statue 
    'auto_install': False,
    'installable': True,

     # module external dependencies
    'external_dependencies': {
        'python': [],
    },
}
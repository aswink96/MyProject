# -*- coding: utf-8 -*-
{
    'name': "Product Warranty",


    'summary': "Warranty details of products",
    'sequence': 1,

    'description': """
        All about product warranty.
    """,

    'author': "Aswin K",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Products',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'reports/report.xml',
        'reports/warranty_report.xml',
        'wizards/create_report.xml',
        'views/warranty.xml',
        'views/templates.xml',
        'views/warranty_locations.xml'


    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

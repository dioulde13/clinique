# -*- coding: utf-8 -*-
{
    'name': "clinique",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'sale', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence_data.xml',
        'data/sequence_rendez_vous_data.xml',
        'views/menu.xml',
        'views/departement.xml',
        'views/ir_cron.xml',
        'data/mail_template_data.xml',
        # 'views/user_heritage.xml',
        'views/facturation_heritage.xml',
        'views/patient.xml',
        'views/rendez_vous.xml',
        # 'reports/facture_report_inherit.xml',
        # 'reports/report_header_footer_inhert.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

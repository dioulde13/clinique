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

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail', 'sale', 'account', 'portal'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence_data.xml',
        'data/sequence_rendez_vous_data.xml',
        'views/menu.xml',
        'views/departement.xml',
        'views/portal_template.xml',
        'views/ir_cron.xml',
        'data/mail_template_data.xml',
        'views/patient.xml',
        'views/templates.xml',
        'views/rendez_vous.xml',
        'wizard/annuler_render_vous.xml',
        'wizard/appointement_report_view.xml',
        'reports/appointement_detail.xml',
        'reports/report.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

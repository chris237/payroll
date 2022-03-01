# -*- coding: utf-8 -*-
{
    'name': "payroll_cu",

    'summary': """
        customiser payroll pour la paie du cameroun""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Odoo Tech camer",
    'website': "http://www.odoo-tech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/contribution.xml',
        'data/hr_payroll_data.xml',
        'data/data.xml',
        'views/templates.xml',
        'views/report_payslips.xml',
        'views/email_template.xml',
        'views/cotisation_individuelle.xml',
        'views/dsn_recp.xml',
        'views/dsn_ursa.xml',
        'views/dsn_liste.xml',
        # 'views/dsn_mensu.xml',
        'reports/cotisation_individuelle.xml',
        'reports/dsn_recp.xml',
        # 'reports/dsn_ursa.xml',
        'reports/dsn_liste.xml',
        # 'reports/dsn_mensu.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}

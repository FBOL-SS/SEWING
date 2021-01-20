# -*- coding: utf-8 -*-
{
    'name': "Departamentos y Municipios de El Salvador",
    'summary': """Permite generar el reporte de Departamentos y Municipios de El Salvador""",
    'description': """
        Permite generar el reporte de  Departamentos y Municipios de El Salvador
        """,
    'author': "SewingSolution",
    'website': "",
    'price': 50.00,
    'currency': 'USD',
    'license': 'GPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'General',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base',
                'sales_team',
                'sale'],
    # always loaded
    'data': [
        'data/res.country.state.csv',
        'data/res.municipality.csv',
        'views/res_municipality.xml',
        'views/res_partner.xml',
        'views/res_bank.xml',
        'security/ir.model.access.csv',
   # 'views/view_res_company.xml',
    #'views/view_res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    #'demo.xml',
    ],
}
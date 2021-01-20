# -*- coding: utf-8 -*-

{
    'name': 'Unir Ordenes de Ventas',
    'category': 'Sales',
    'summary': 'Este módulo fusionará orden de venta.',
    'version': '12.0.1.0.0',
    'website': '',
    'author': 'SewingSolution',
    'description': 'Este módulo une presupuestos y crea uno solo',
    'license': "AGPL-3",

    'depends': [
        'sale_management'
    ],

    'data': [
        'wizard/merge_sale_order_wizard_view.xml',
    ],

    'images': [
        'static/description/banner.jpg',
    ],

    'installable': True,

}

# -*- coding: utf-8 -*-

{
    'name': 'Merge Ordenes de Compra BDS',
    'category': 'Purchase',
    'summary': 'Este módulo fusionará la orden de compra.',
    'version': '12.0.1.0.0',
    'website': '',
    'author': 'SewingSolution',
    'description': 'Unión de Ordenes de Compra',
    'license': "AGPL-3",

    'depends': [
        'purchase',
        'stock'
    ],

    'data': [
        'wizard/merge_puchase_order_wizard_view.xml',
    ],

    'images': [
        'static/description/banner.jpg',
    ],

    'auto_install': False,
    'installable': True,
    'application': False

}

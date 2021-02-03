# -*- coding: utf-8 -*-
# Copyright (C) 2017-present  Technaureus Info Solutions(<http://www.technaureus.com/>).

{
    'name': 'Boleta de entrega',
    'version': '1.0',
    'category': 'Warehouse',
    'sequence': 1,
    'author':'SewingSolution',
    'summary': 'Delivery Slip with Barcodes',
    'website': '',
    'description': """
This addon will help to show barcode in delivery slip...""",
    'depends': ['sale_stock'],
    'data': [
        'report/stock_report_views.xml',
        'report/report_deliveryslip.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

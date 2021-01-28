# -*- coding: utf-8 -*-
# Copyright (C) 2017-present  Technaureus Info Solutions(<http://www.technaureus.com/>).

{
    'name': 'Delivery Slip with Barcodes',
    'version': '1.0',
    'category': 'Warehouse',
    'sequence': 1,
    'author':'Technaureus Info Solutions Pvt. Ltd.',
    'summary': 'Delivery Slip with Barcodes',
    'website': 'http://www.technaureus.com/',
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

# -*- coding: utf-8 -*-
# Copyright (C) 2017-present  ).

{
    'name': 'Boleta de Entrega',
    'version': '1.0',
    'category': 'Warehouse',
    'sequence': 1,
    'author':'SewingSolution',
    'summary': 'Boleta de Entrega',
#    'summary': 'Boleta de Entrega con Codigo de Barra',
    'website': '',
    'description': """
Este complemento ayudará a mostrar el código de barras en el Ordenes de Entrega...""",
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

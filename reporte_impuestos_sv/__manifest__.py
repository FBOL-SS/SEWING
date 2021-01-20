# -*- coding: utf-8 -*-
{
    'name': 'Reporte de Iva Para El Salvador',
    'version': '12.0.0.7',
    'category': 'Accounting',
    'description': '''
    Este modulo crea lo necesario para generar un reporte impreso
     del libro de iva y poder generar el de compra y ventas''',
    'author': 'SewingSolution',
    'website': '',
    'price': 250.00,
    'currency': 'USD',
    'license': 'GPL-3',
    'data': [
        'report/libro_iva_fcf.xml',
        'report/libro_iva_ccf.xml',
        'report/libro_iva_compras.xml',
        'report/report_libro_iva.xml',
        'report/libro_iva.xml',
        'views/libro_iva_view.xml',
        'views/wizard_tax_adjustments.xml',
        'security/ir.model.access.csv',
        'security/iva_security.xml',
    ],
    'depends': [
        'base',
        'account',
        'l10n_invoice_sv',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'post_init_hook': 'drop_print',
}

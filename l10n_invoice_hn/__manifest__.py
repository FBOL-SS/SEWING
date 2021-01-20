# -*- coding: utf-8 -*-
{
    'name': "Facturacion de Honduras",
    'summary': """Facturacion de """,
    'author': "SewingSolution",
    'website': "",
    'category': 'Contabilidad',
    'version': '0.5',
    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant'],
    # always loaded
    'data': [
        'views/extra_fields_view.xml',
        'report/report_invoice_hn.xml',
        'report/invoice_report.xml',
        'report/report_invoice_main.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    #'demo.xml',
    'installable': True,

}

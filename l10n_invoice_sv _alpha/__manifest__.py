# -*- coding: utf-8 -*-
{
    'name': "Facturacion de El Salvador Alpha",
    'summary': """Facturacion de El Salvador Alpha""",
    'description': """
       Facturacion de El Salvador Alpha.
       Permite Imprimir los tres tipos de facturas utilizados en El Salvador
        - Consumidor Final
        - Credito Fiscal
        - Exportaciones
      Tambien permite imprimir los documentos que retifican:
        - Anulaciones.
        - Nota de Credito
      Valida que todos los documentos lleven los registros requeridos por ley
        """,
    'author': "SewingSolution",
    'website': "",
    'price': 150.00,
    'currency': 'USD',
    'license': 'GPL-3',
    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Contabilidad',
    'version': '0.5',
    # any module necessary for this one to work correctly
    'depends': ['base', 'l10n_sv', 'account', 'account_accountant', 'product'],
    # always loaded
    'data': [
        'views/account_journal.xml',
        'views/posicion_arancel_view.xml',
        'views/product_template_view.xml',
        'views/account_invoice_view.xml',
        'views/account_invoice_proveedor_view.xml',
	    'views/extra_fields_view.xml',
        'views/account_tax.xml',
        'data/journal_data.xml',
        'report/report_invoice_anu.xml',
        'report/report_invoice_ccf.xml',
        'report/report_invoice_fcf.xml',
        'report/report_invoice_exp.xml',
        'report/report_invoice_ndc.xml',
        'report/report_invoice_digital.xml',
        'report/report_invoice_exp_ins.xml',
        'report/report_invoice_ccf_ins.xml',
        'report/report_invoice_fcf_ins.xml',
        'report/invoice_report.xml',
        'report/report_invoice_main.xml',
        'security/ir.model.access.csv',
        'wizard/account_invoice_refund.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    #'demo.xml',
    'installable': True,
    'application': False,
    'auto_install': False,
    'post_init_hook': 'invoices_refunds',
}

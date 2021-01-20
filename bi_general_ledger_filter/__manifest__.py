# -*- coding: utf-8 -*-
#  See LICENSE file for full copyright and licensing details.
##################################################################################

{
    'name': 'Libro Mayor (filtros avanzados)',
    'version': '12.0.0.1',
    'category': 'Accounting',
    'summary': 'This apps helps to apply account and account type fiter on Libro Mayor Report',
    'description': """
    
    Detailed Libro Mayor
    This apps helps to apply account and account type fiter on Libro Mayor Report
    Libro Mayor Report filter by Accounts
	Libro Mayor filter in odoo
	Libro Mayor filter for 
    Account Filter on Libro Mayor Reports
    Accounting Filter on Libro Mayor Reports
    Filter By Account on Libro Mayor Report
    Account Filter on Accounting Report

    Libro Mayor Report with Account Type Filter
	Libro Mayor Report with analytic account
	Libro Mayor filter with analytic account
	Libro Mayor Report filter by Account Type
    Account Type Filter on Libro Mayor Reports
    Accounting Type Filter on Libro Mayor Reports
    Filter By Account Type on Libro Mayor Report
    Account Type Filter on Accounting Report
    Libro Mayor report filter with Account
    Libro Mayor report filter with account type
    enterprise accounting report filter

    Libro Mayor Report filter by Balance
    Balace Filter on Libro Mayor Reports
    With Balance Filter on Libro Mayor Reports
    Without Balance Filter on Libro Mayor Reports
    Filter By Balance on Libro Mayor Report
    Balance without Filter on Accounting Report
    Libro Mayor report filter with balance amount
    Libro Mayor report filter without balance amount
    enterprise Libro Mayor report filter
    View Libro Mayor report with Display Name
    Display Name on Libro Mayor Report
    Display name visible on Libro Mayor report
""",
    'author': 'SewingSolution',
    'price': 500,
    'currency': "USD",
    'website': '',
    'images': [],
    'depends': ['account', 'account_accountant', 'account_reports'],
    'data': [

        'data/account_financial_report_data.xml',
        'views/general_ledger_filter.xml',
        'views/custom_account_report.xml',
    ],
    'qweb': [
         'static/src/xml/custom_account_report.xml',
    ],
    
    'installable': True,
    'auto_install': False,
    'application': True,
    "images":['static/description/Banner.png'],
}























# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019.

#
##############################################################################

{
    'name': 'Dynamic Print Cheque - Check writing',
    'version': '12.0.1.2',
    'sequence': 1,
    'category': 'Generic Modules/Accounting',
    'description': """
         odoo App will  configure and print cheque/check 
         Dynamically for any bank with different Cheque format.

Cheque print, check print, check writing, bank check print, 
check dynamic, bank cheque, cheque dynamic, cheque printing, 
bank cheque, dynamic print cheque, cheque payment, payment check, 

    Dynamic print cheque
    How can we create dynamic cheque
    Dynamic cheque print
    Accounting voucher
    Cheque acconting voucher
    Odoo dynamic cheque
    Odoo dynamic cheque print
    Print dynamic cheque
    Odoo11 dynamic cheque print
    Print cheque
    Print cheque odoo
    Dynamically print cheque
    Dynamic cheque
    Cheque accounting voucher
    Accounting cheque voucher
    Dynamic bank cheque
    Dynamic bank cheque print in odoo
    Odoo dynamic cheque
    Odoo dynamic bank cheque
    Odoo dynamic bank cheque print
    cheque Printer
    check print
    dynamic check print
    check printing configuration
    cheque printing
    payment cheque print
    cheque payment print 


    """,
    'author': 'SewingSolution',
    'website': '',
    'summary': 'odoo App will  configure and print '
               'cheque/check Dynamically for any '
               'bank with different Cheque format',
    'depends': ['account', 'account_voucher'],
    'data': [
        'security/ir.model.access.csv',
        'views/report_print_cheque.xml',
        'views/report_menu.xml',
        'views/cheque_setting_view.xml',
        'views/account_vocher_view.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 350.0,
    'currency': 'USD',
}

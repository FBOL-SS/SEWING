# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Resgistro de Quedan',
    'author': 'SewingSolution',
    'summary': 'Modulo para llevan un registro de los quedans realizados',
    'category': 'Extra Tools',
    'depends': ['base', 'account'],
    'data': [
        'views/quedan_register_view.xml',
    ],
    'installable': True,
    'application': True,
}

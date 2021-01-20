# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    active = fields.Boolean(
        string='Libro Iva',
        help='- Estara activo si esta factura ya '
             'fue contabilizada en el libro de iva',
        default=True
    )


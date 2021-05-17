# -*- coding: utf-8 -*-
from odoo import fields, models


class Journal(models.Model):
    _inherit = 'account.journal'

    type_report = fields.Selection(
        [
            ('fcf', 'Factura Consumidor Final'),
            ('ccf', 'Comprobante Credito Fiscal'),
            ('exp', 'Factura de Exportacion'),
            ('ndc', 'Nota de Credito'),
            ('anu', 'Anulacion'),
            ('compras', 'CCF Compras'),
            ('anu_compras', 'Reintegro de CCF Compras'),
        ],
        default=False,
        string='Tipo de Documento Fiscal',
        copy=False,
        help="El 'Tipo de Documento Fiscal' es usado en las impresiones "
            "de los diferentes documentos, solo selecionar si la numeracion" 
            "corresponde a algunos de los documentos fiscales de venta")

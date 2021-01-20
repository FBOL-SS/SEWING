# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "account.invoice"

    fecha = fields.Date(string="Fecha", required=False, )
    no_quedan = fields.Char(string="No. de Quedan", required=False, )
    entrega = fields.Char(string="Entrega", required=False, )
    recibe = fields.Many2one('res.users', string='Recibe')
    other_invoice = fields.Char(string="Otras Facturas", required=False,)












# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "sale.order.line"

    entrega_nota = fields.Selection(string="ENTREGA/NOTA", selection=[
                                                            ('IN', 'INMEDIATO'),
                                                            ('10', '10 DIAS'),
                                                            ('3-4', '3-4 SEMANAS'),
                                                            ], required=False, )

    entrega_nota2 = fields.Char(string="ENTREGA/NOTA", required=False, )








# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "account.invoice"
    
    orden_no = fields.Char(string="Orden No.:")
    customer_no = fields.Char(string="Numero del Cliente")
    envio = fields.Selection(string="Metodo de Envio",
                             selection=[('cif', 'CIF El Salvador'), ],
                             default='cif', readonly=True)















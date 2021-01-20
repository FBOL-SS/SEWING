# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "account.invoice"

    amount_letters_hn = fields.Char(string="Monto en Letras", required=False, )
    no_bultos = fields.Char(string="No. Bultos", required=False, )
    amount_units = fields.Char(string="Total Unid:",  required=False, )
    amount_kg = fields.Char(string="Total KG:", required=False, )
    emision_date_hn = fields.Date(string="Fecha Límite de Emisión", required=False)
    numeracion = fields.Char(string="Numeración Autorizada", required=False, )















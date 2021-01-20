# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'phone.validation.mixin']
    # Datos Personales
    dui = fields.Char(string="D.U.I.")
    nit = fields.Char(string="N.I.T.")
    nrc = fields.Char(string="N.R.C.")
    giro = fields.Char(string="Giro")
    

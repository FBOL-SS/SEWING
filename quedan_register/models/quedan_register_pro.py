# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api, _


class QuedanRegisterPro(models.Model):
    _name = "quedan.register.pro"

    fecha_1 = fields.Date(string="Fecha", required=False, )
    empresa_1 = fields.Many2one('res.partner', string='Empresa', domain="[('supplier', '=', 1)]")
    entrega_1 = fields.Char(string="Entrega", required=False, )
    recibe_1 = fields.Many2one('res.users', string='Recibe')
    no_factura_1 = fields.Char(string="No. de Factura", required=False, )
    seq_quedan = fields.Char(string='Quedan No', required=True, copy=False, readonly=True,
                             index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('seq_quedan', _('New')) == _('New'):
            vals['seq_quedan'] = self.env['ir.sequence'].next_by_code('quedan.register') or _('New')
        result = super(QuedanRegisterPro, self).create(vals)
        return result








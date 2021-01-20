# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class Partner(models.Model):
    _inherit = 'res.bank'

    munic_id = fields.Many2one('res.municipality', _('Municipality'),ondelete='restrict')
    
    @api.onchange('state')
    def _onchange_state(self):
        if not self.country:
            self.country = self.state.country_id
        if self.state:
            return {'domain': {'munic_id': [('dpto_id', '=', self.state.id)]}}
        else:
            return {'domain': {'munic_id': []}}
    
    @api.onchange('munic_id')
    def _onchange_munic_id(self):
        if not self.state:
            self.state = self.munic_id.dpto_id
            
    

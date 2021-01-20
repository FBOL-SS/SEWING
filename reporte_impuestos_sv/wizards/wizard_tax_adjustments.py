# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TaxAdjustments(models.TransientModel):
    _inherit = "tax.adjustments.wizard"

    @api.multi
    def _get_default_journal(self):
        return self.env['account.journal'].search(
            [('type', '=', 'general'),
             ('company_id', '=', self.env.user.company_id.id)], limit=1).id

    journal_id = fields.Many2one('account.journal',
                                 string='Journal',
                                 required=True,
                                 default=_get_default_journal)

    company_id = fields.Many2one('res.company',
                                 string='Compañia',
                                 ondelete='restrict',
                                 default=lambda
                                     self: self.env.user.company_id.id)

    partner_id = fields.Many2one('res.partner',
                                 string='Proveedor',
                                 ondelete='restrict')

    @api.multi
    def _create_move(self):
        debit_vals = {
            'name': self.reason,
            'debit': self.amount,
            'credit': 0.0,
            'company_id': self.company_id.id,
            'partner_id': self.partner_id.id,
            'account_id': self.debit_account_id.id,
            'tax_line_id': self.tax_id.id,
        }
        credit_vals = {
            'name': self.reason,
            'debit': 0.0,
            'credit': self.amount,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'account_id': self.credit_account_id.id,
            'tax_line_id': self.tax_id.id,
        }
        vals = {
            'journal_id': self.journal_id.id,
            'date': self.date,
            'ref': self.reason,
            'company_id': self.company_id.id,
            'state': 'draft',
            'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
        }
        move = self.env['account.move'].create(vals)
        move.post()
        return move.id

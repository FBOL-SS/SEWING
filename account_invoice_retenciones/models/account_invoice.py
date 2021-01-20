# -*- encoding: utf-8 -*-
#   Copyright 2019 

from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        for line in self.invoice_line_ids:
            fpos = self.fiscal_position_id
            if fpos:
                fpos_name = self.fiscal_position_id.name
                amount_untaxed = self.amount_untaxed
                # todo: Imp No Hardcode Tax and FP by name
                values = ['Gran Contribuyente']
                if fpos_name in values and amount_untaxed >= 100.00:
                    'Retención 1%'
                    taxes = line.invoice_line_tax_ids.filtered(
                        lambda x: x.description != 'Retención 1%'
                    )

                    line.update({'invoice_line_tax_ids': [(6, 0, taxes.ids)]})
                else:
                    if self.type in ('out_invoice', 'out_refund'):
                        taxes = line.product_id.taxes_id or \
                                line.account_id.tax_ids
                    else:
                        taxes = line.product_id.supplier_taxes_id or \
                                line.account_id.tax_ids

                    # Keep only taxes of the company
                    company_id = line.company_id or line.env.user.company_id
                    taxes = taxes.filtered(
                        lambda r: r.company_id == company_id)

                    line.invoice_line_tax_ids = self.fiscal_position_id.\
                        map_tax(taxes, line.product_id, self.partner_id)
        return super(AccountInvoice, self)._onchange_invoice_line_ids()


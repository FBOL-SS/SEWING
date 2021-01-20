# -*- coding: utf-8 -*-
from odoo.tools.safe_eval import safe_eval
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountInvoiceRefund(models.TransientModel):
    """Refunds invoice"""

    _inherit = "account.invoice.refund"

    journal_id = fields.Many2one('account.journal', 'Diario',
                                 domain="[('type_report','in',['anu','ndc'])]")
    sale = fields.Boolean('Es Venta?', compute='_is_sale')

    @api.depends('date_invoice')
    @api.one
    def _is_sale(self):
        invoice_id = self.env['account.invoice'].browse(
            self._context.get('active_id', False))
        if invoice_id.journal_id.type == 'sale' \
                and invoice_id.type == 'out_invoice':
            self.sale = True
        else:
            self.sale = False

    @api.multi
    def compute_refund(self, mode='refund'):
        inv_obj = self.env['account.invoice']
        inv_tax_obj = self.env['account.invoice.tax']
        inv_line_obj = self.env['account.invoice.line']
        context = dict(self._context or {})
        xml_id = False

        for form in self:
            created_inv = []
            date = False
            description = False
            for inv in inv_obj.browse(context.get('active_ids')):
                if inv.state in ['draft', 'proforma2', 'cancel']:
                    raise UserError(
                        _('Cannot refund draft/proforma/cancelled invoice.'))
                if inv.reconciled and mode in ('cancel', 'modify'):
                    raise UserError(_(
                        'Cannot refund invoice which is already reconciled, '
                        'invoice should be unreconciled first. You can only '
                        'refund this invoice.'))

                date = form.date or False
                refund_id = inv.id
                description = form.description or inv.name
                if self.journal_id:
                    refund = inv.refund(form.date_invoice, date, description,
                                        self.journal_id.id)
                else:
                    refund = inv.refund(form.date_invoice, date, description,
                                        inv.journal_id.id)

                # agregamos trazabilidad de documento
                for i in refund:
                    i.inv_refund_id = refund_id

                # agregamos enlaze a factura anulada
                inv.inv_refund_id = refund.id

                created_inv.append(refund.id)
                if mode in ('cancel', 'modify'):
                    movelines = inv.move_id.line_ids
                    to_reconcile_ids = {}
                    to_reconcile_lines = self.env['account.move.line']
                    for line in movelines:
                        if line.account_id.id == inv.account_id.id:
                            to_reconcile_lines += line
                            to_reconcile_ids.setdefault(line.account_id.id,
                                                        []).append(line.id)
                        if line.reconciled:
                            line.remove_move_reconcile()
                    refund.action_invoice_open()
                    for tmpline in refund.move_id.line_ids:
                        if tmpline.account_id.id == inv.account_id.id:
                            to_reconcile_lines += tmpline
                            to_reconcile_lines.filtered(
                                lambda l: l.reconciled == False).reconcile()

                    # marcamos la factura original como anulada
                    inv.state_refund = 'refund'

                    if mode == 'modify':
                        invoice = inv.read(
                            inv_obj._get_refund_modify_read_fields())
                        invoice = invoice[0]
                        del invoice['id']
                        invoice_lines = inv_line_obj.browse(
                            invoice['invoice_line_ids'])
                        invoice_lines = inv_obj.with_context(
                            mode='modify')._refund_cleanup_lines(invoice_lines)
                        tax_lines = inv_tax_obj.browse(invoice['tax_line_ids'])
                        tax_lines = inv_obj._refund_cleanup_lines(tax_lines)
                        invoice.update({
                            'type': inv.type,
                            'date_invoice': form.date_invoice,
                            'state': 'draft',
                            'number': False,
                            'invoice_line_ids': invoice_lines,
                            'tax_line_ids': tax_lines,
                            'date': date,
                            'origin': inv.origin,
                            'fiscal_position_id': inv.fiscal_position_id.id,
                            'inv_refund_id': refund_id,
                        })
                        for field in inv_obj._get_refund_common_fields():
                            if inv_obj._fields[field].type == 'many2one':
                                invoice[field] = invoice[field] and \
                                                 invoice[field][0]
                            else:
                                invoice[field] = invoice[field] or False
                        inv_refund = inv_obj.create(invoice)
                        inv_refund.inv_refund_id = refund_id
                        if inv_refund.payment_term_id.id:
                            inv_refund._onchange_payment_term_date_invoice()
                        created_inv.append(inv_refund.id)
                xml_id = (inv.type in ['out_refund',
                                       'out_invoice']) and \
                         'action_invoice_tree1' or \
                         (inv.type in ['in_refund',
                                       'in_invoice']) \
                         and 'action_invoice_tree2'
                # Put the reason in the chatter
                subject = _("Invoice refund")
                body = description
                refund.message_post(body=body, subject=subject)
        if xml_id:
            result = self.env.ref('account.%s' % (xml_id)).read()[0]
            invoice_domain = safe_eval(result['domain'])
            invoice_domain.append(('id', 'in', created_inv))
            result['domain'] = invoice_domain
            return result
        return True

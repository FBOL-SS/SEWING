# -*- coding: utf-8 -*-
from .amount_to_text_sv import to_word
from odoo import api, fields, models, _, exceptions


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    inv_refund_id = fields.Many2one('account.invoice', 'Factura Relacionada',
                                    copy=False, track_visibility='onchange')

    state_refund = fields.Selection([
        ('refund', 'Retificada'),
        ('no_refund', 'No Retificada'),
    ], string="Retificada", index=True, readonly=True, default='no_refund',
        track_visibility='onchange', copy=False)

    amount_text = fields.Char(string=_('Amount to text'), store=True,
                              readonly=True,
                              compute='_amount_to_text',
                              track_visibility='onchange')

    @api.one
    @api.depends('amount_total')
    def _amount_to_text(self):
        self.amount_text = to_word(self.amount_total)

    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True

        report = self.journal_id.type_report

        if report == 'ccf':
            return self.env.ref(
                'l10n_invoice_alpha.report_credito_fiscal').report_action(self)
        if report == 'fcf':
            return self.env.ref('account.account_invoices').report_action(self)
        if report == 'exp':
            return self.env.ref(
                'l10n_invoice_alpha.report_exportacion').report_action(self)
        if report == 'ndc':
            return self.env.ref('l10n_invoice_alpha.report_ndc').report_action(
                self)
        if report == 'anu':
            return self.env.ref(
                'account.account_invoice_action_report_duplicate').\
                report_action(self)
        if report == 'axp':
            return self.env.ref(
                'l10n_invoice_alpha.report_anul_export').report_action(self)

        return self.env.ref('account.account_invoices').report_action(self)

    @api.multi
    def msg_error(self, campo):
        raise exceptions.ValidationError(
            "No puede emitir un documento si falta "
            "un campo Legal Verifique {}".format(campo))

    @api.multi
    def action_invoice_open(self):
        """
        validamos que partner cumple los requisitos basados en el tipo
        de documento de la sequencia del diario selecionado
        :return: Native super method
        """
        inv_type = self.type
        # si es factura normal
        type_report = self.journal_id.type_report

        if type_report == 'ccf':
            if not self.partner_id.parent_id:
                if not self.partner_id.nrc:
                    self.msg_error("N.R.C.")
                if not self.partner_id.nit:
                    self.msg_error("N.I.T.")
                if not self.partner_id.giro:
                    self.msg_error("Giro")
            else:
                if not self.partner_id.parent_id.nrc:
                    self.msg_error("N.R.C.")
                if not self.partner_id.parent_id.nit:
                    self.msg_error("N.I.T.")
                if not self.partner_id.parent_id.giro:
                    self.msg_error("Giro")

        if type_report == 'fcf':
            if not self.partner_id.parent_id:
                if not self.partner_id.nit:
                    self.msg_error("N.I.T.")
                if self.partner_id.company_type == 'person':
                    if not self.partner_id.dui:
                        self.msg_error("D.U.I.")
            else:
                if not self.partner_id.parent_id.nit:
                    self.msg_error("N.I.T.")
                if self.partner_id.parent_id.company_type == 'person':
                    if not self.partner_id.dui:
                        self.msg_error("D.U.I.")

        # si es retificativa
        if type_report == 'ndc':
            if not self.partner_id.parent_id:
                if not self.partner_id.nrc:
                    self.msg_error("N.R.C.")
                if not self.partner_id.nit:
                    self.msg_error("N.I.T.")
                if not self.partner_id.giro:
                    self.msg_error("Giro")
            else:
                if not self.partner_id.parent_id.nrc:
                    self.msg_error("N.R.C.")
                if not self.partner_id.parent_id.nit:
                    self.msg_error("N.I.T.")
                if not self.partner_id.parent_id.giro:
                    self.msg_error("Giro")

        return super(AccountInvoice, self).action_invoice_open()

    @api.multi
    def print_report(self):
        return self.env.ref('l10n_invoice_alpha.report_invoice_digital').report_action(self)



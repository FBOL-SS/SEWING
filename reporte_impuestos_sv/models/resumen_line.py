# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp


class ResumenLine(models.Model):
    _name = 'resumen.line'
    _inherit = ['mail.thread', 'mail.activity.mixin',
                'portal.mixin']  # Redes Sociales
    _description = "Resumen de Libro de Iva"

    company_id = fields.Many2one(
        'res.company', string='Company',
        change_default=True,
        required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env[
            'res.company']._company_default_get(
            'resumen.line'))

    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string="Company Currency",
        readonly=True)
    libro_iva_id = fields.Many2one(
        'libro.iva', _('Referencia de libro'),
        required=True, ondelete='cascade',
        index=True, readonly=True)

    # comunes
    detalle = fields.Char(string=_("Resumen"), readonly=True)

    # contribuyentes
    neto_p = fields.Monetary(_('Valor Neto'), store=True,
                             currency_field='company_currency_id',
                             readonly=True)
    iva_p = fields.Monetary(_('Debito Fiscal'), store=True,
                            currency_field='company_currency_id',
                            readonly=True)
    neto_t = fields.Monetary(_('Valor Neto'), store=True,
                             currency_field='company_currency_id',
                             readonly=True)
    iva_t = fields.Monetary(_('Debito Fiscal'), store=True,
                            currency_field='company_currency_id',
                            readonly=True)
    iva_retenido = fields.Monetary(_('IVA Retenido'), store=True,
                                   currency_field='company_currency_id',
                                   readonly=True)

    # consumidor
    total = fields.Monetary(_('Total'), store=True,
                            currency_field='company_currency_id',
                            readonly=True)
    mes = fields.Char(String=_("Mes"), readonly=True)
    year = fields.Char(String=_("Año"), readonly=True)

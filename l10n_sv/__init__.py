# -*- coding:utf-8 -*-
from . import models

from odoo import api, SUPERUSER_ID

def drop_journal(cr, registry):
  env = api.Environment(cr, SUPERUSER_ID, {})
  journal_ids = env['account.journal'].search([('code', 'in',['INV','BILL'])])
  for j in journal_ids:
    j.active = False
  tax_ids = env['account.tax'].search([('name', 'in',['Tax 15.00%','Impuesto 15.00%'])])
  for t in tax_ids:
    t.active = False
  partner_ids = env['res.partner'].search([('vat', '=', True)])
  for p in partner_ids:
    p.nit = p.vat
  company_ids = env['res.company'].search(['|', ('vat', '=', True),('company_registry','=',True)])
  for p in partner_ids:
    p.nit = p.vat
    p.nrc = p.company_registry
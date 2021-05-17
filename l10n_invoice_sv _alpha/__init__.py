# -*- coding: utf-8 -*-
from . import models
from . import wizard

from odoo import api, SUPERUSER_ID


def invoices_refunds(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    inv_obj = env['account.invoice']
    inv_ids = inv_obj.search([('type', '=', 'out_invoice'),
                              ('state', '=', 'paid'), ])
    for inv_id in inv_ids:
        # print(inv_id,'Id')
        refund_id = inv_obj.search([('origin', '=', inv_id.number)])
        # print(refund_id,'Refun')
        if refund_id:
            refund_data = inv_obj.browse(refund_id.id)
            # print(refund_data,"Data")
            if refund_id and len(refund_id) < 2:
                # print('Se valida y asigna',refund_data.id,
                # inv_id.inv_refund_id)
                inv_id.inv_refund_id = refund_data.id
                # print('escribimos valores')
                refund_data.write({
                    'inv_refund_id': inv_id.id,
                    'state_refund': 'refund'})

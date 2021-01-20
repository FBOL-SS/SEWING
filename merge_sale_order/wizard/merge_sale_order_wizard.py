# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class MergePurchaseOrder(models.TransientModel):
    _name = 'merge.sale.order'

    merge_type = \
        fields.Selection([
            ('new_cancel',
                'Crear un nuevo pedido y cancelar todos los pedidos de venta seleccionados'),
            ('new_delete',
             'Crear un nuevo pedido y eliminar todos los pedidos de venta seleccionados'),
            ('merge_cancel',
             'Unir orden en una orden seleccionada existente y cancelar otras'),
            ('merge_delete',
                'Unir orden en orden seleccionada existente y eliminar otras ')],
            default='new_cancel')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    @api.onchange('merge_type')
    def onchange_merge_type(self):
        res = {}
        for order in self:
            order.sale_order_id = False
            if order.merge_type in ['merge_cancel', 'merge_delete']:
                sale_orders = self.env['sale.order'].browse(
                    self._context.get('active_ids', []))
                res['domain'] = {
                    'sale_order_id':
                    [('id', 'in',
                        [sale.id for sale in sale_orders])]
                }
            return res

    @api.multi
    def merge_orders(self):
        sale_orders = self.env['sale.order'].browse(
            self._context.get('active_ids', []))
        existing_so_line = False
        if len(self._context.get('active_ids', [])) < 2:
            raise UserError(
                _('Seleccione al menos dos órdenes de venta para realizar'
                    'la Unión.'))
        if any(order.state != 'draft' for order in sale_orders):
            raise UserError(
                _('Seleccione Pedidos de venta que estén en estado de presupuesto '
                  'para realizar la Unión.'))
        partner = sale_orders[0].partner_id.id
        if any(order.partner_id.id != partner for order in sale_orders):
            raise UserError(
                _('Seleccione Pedidos de venta cuyos clientes sean iguales para '
                    ' realizar la Unión.'))
        if self.merge_type == 'new_cancel':
            so = self.env['sale.order'].with_context({
                'trigger_onchange': True,
                'onchange_fields_to_trigger': [partner]
            }).create({'partner_id': partner})
            default = {'order_id': so.id}
            for order in sale_orders:
                for line in order.order_line:
                    if so.order_line:
                        for soline in so.order_line:
                            if line.product_id == soline.product_id and \
                                    line.price_unit == soline.price_unit:
                                existing_so_line = soline
                                break
                    if existing_so_line:
                        existing_so_line.product_uom_qty += \
                            line.product_uom_qty
                        so_taxes = [
                            tax.id for tax in existing_so_line.tax_id]
                        [so_taxes.append((tax.id))
                         for tax in line.tax_id]
                        existing_so_line.tax_id = \
                            [(6, 0, so_taxes)]
                    else:
                        line.copy(default=default)
            for order in sale_orders:
                order.action_cancel()
        elif self.merge_type == 'new_delete':
            so = self.env['sale.order'].with_context({
                'trigger_onchange': True,
                'onchange_fields_to_trigger': [partner]
            }).create({'partner_id': partner})
            default = {'order_id': so.id}
            for order in sale_orders:
                for line in order.order_line:
                    if so.order_line:
                        for soline in so.order_line:
                            if line.product_id == soline.product_id and \
                                    line.price_unit == soline.price_unit:
                                existing_so_line = soline
                                break
                    if existing_so_line:
                        existing_so_line.product_uom_qty += \
                            line.product_uom_qty
                        so_taxes = [
                            tax.id for tax in existing_so_line.tax_id]
                        [so_taxes.append((tax.id))
                         for tax in line.tax_id]
                        existing_so_line.tax_id = \
                            [(6, 0, so_taxes)]
                    else:
                        line.copy(default=default)
            for order in sale_orders:
                order.sudo().action_cancel()
                order.sudo().unlink()
        elif self.merge_type == 'merge_cancel':
            default = {'order_id': self.sale_order_id.id}
            so = self.sale_order_id
            for order in sale_orders:
                if order == so:
                    continue
                for line in order.order_line:
                    if so.order_line:
                        for soline in so.order_line:
                            if line.product_id == soline.product_id and \
                                    line.price_unit == soline.price_unit:
                                existing_so_line = soline
                                break
                    if existing_so_line:
                        existing_so_line.product_uom_qty += \
                            line.product_uom_qty
                        so_taxes = [
                            tax.id for tax in existing_so_line.tax_id]
                        [so_taxes.append((tax.id))
                         for tax in line.tax_id]
                        existing_so_line.tax_id = \
                            [(6, 0, so_taxes)]
                    else:
                        line.copy(default=default)
            for order in sale_orders:
                if order != so:
                    order.sudo().action_cancel()
        else:
            default = {'order_id': self.sale_order_id.id}
            so = self.sale_order_id
            for order in sale_orders:
                if order == so:
                    continue
                for line in order.order_line:
                    if so.order_line:
                        for soline in so.order_line:
                            if line.product_id == soline.product_id and \
                                    line.price_unit == soline.price_unit:
                                existing_so_line = soline
                                break
                    if existing_so_line:
                        existing_so_line.product_uom_qty += \
                            line.product_uom_qty
                        so_taxes = [
                            tax.id for tax in existing_so_line.tax_id]
                        [so_taxes.append((tax.id))
                         for tax in line.tax_id]
                        existing_so_line.tax_id = \
                            [(6, 0, so_taxes)]
                    else:
                        line.copy(default=default)
            for order in sale_orders:
                if order != so:
                    order.sudo().action_cancel()
                    order.sudo().unlink()

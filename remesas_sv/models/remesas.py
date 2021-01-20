# -*-conding:utf-8-*-

from odoo import _
import odoo.addons.decimal_precision as dp
from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models


class ListAsientos(models.Model):
  _name = "list.asientos"
  _description = "Listado de Asientos Contables de Remesas"
  
  name = fields.Char('Nombre',
                     relate='asiento_contable_id.name')

  asiento_contable_id = fields.Many2one('account.move',
                                        'Asientos Contables',
                                        readonly=True,
                                        invisible=True,
                                        states={'entered': [
                                            ('invisible', False)
                                            ]})
  remesa_id = fields.Many2one('remesa.sv',
                            string = 'Remesa')


class Remesa_Sv(models.Model):
    _name = 'remesa.sv'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = "Remesas"

    company_id = fields.Many2one('res.company', string='Company',
                                 change_default=True, required=True,
                                 readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 default=lambda self: self.env['res.company']._company_default_get('resumen.line'))

    fecha_remesa = fields.Date(string='Fecha Remesa',
                               states={'draft': [('readonly', False)]},
                               readonly=True,
                               index=True, help="Fecha de Realizada La remesa",
                               copy=False)

    total = fields.Float('Total Remesa',
                         digits=dp.get_precision('Account'),
                         states={'draft': [('readonly', False)]},
                         required=True, readonly=True, help="Total depositado al banco")

    referencia = fields.Char('Referencia Banco', required=True, readonly=True,
                             states={'draft': [('readonly', False)]},
                             help="Ingrese el numero de voucher correspondiente de la remesa")

    banco_id = fields.Many2one('res.bank', 'Banco', ondelete='set null',
                               required=True, readonly=True,
                               states={'draft': [('readonly', False)]},
                               help="Seleccione el banco al cual ha remesado")

    cuenta_id = fields.Many2one('account.journal', 'Cuenta bancaria',
                                required=True,
                                readonly=True,
                                states={'draft': [('readonly', False)]},
                                help="Seleccione la cuenta a la cual ha remesado",
                                domain="[('bank_id', '=', banco_id)]")

    origen_id = fields.Many2one('account.journal', 'Origen de Fondos',
                                required=True,
                                states={'draft': [('readonly', False)]},
                                domain="[('type','in', ['cash','bank'])]")

    responsable_id = fields.Many2one('res.users', 'Responsable',
                                     required=True,
                                     readonly=True,
                                     states={'draft': [('readonly', False)]},
                                     help="Seleccione la persona que ha remesado")
    
    # Agregar Listado de Asientos Contables
    list_asientos = fields.One2many('list.asientos','remesa_id','Asientos Contables',
                                    readonly=True)
    
    asiento_contable_id = fields.Many2one('account.move',
                                          'Asientos Contables',
                                          readonly=True,
                                          invisible=True,
                                          states={'entered': [
                                              ('invisible', False)
                                              ]})
    usuario_id = fields.Many2one('res.users',
                                 string='Usuario',
                                 track_visibility='onchange',
                                 readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 default=lambda self: self.env.user)

    name = fields.Char(String="Remesa Numero",
                       readonly=True,
                       help="Correlativo asignado automaticamente",
                       copy=False,
                       default="Remesa Borrador")

    cancelada = fields.Boolean(string='Remesa Cancelada',
                               copy=False,
                               default=False)

    numero = fields.Char(string='Numero',
                         copy=False)

    state = fields.Selection([
            ('draft', 'Borrador'),
            ('open', 'Abierta'),
            ('entered', 'Ingresada'),
            ('cancel', 'Cancelada'),
        ], string='Estado', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * El borrador sirve para registrar la informacion correspondiente.\n"
             " * El abierto sirve para poder verificar por su superior si la remesa ha sido cargada correctamente a la cuenta.\n"
             " * El ingresada sirve para validar que la transaccion fue realizada.\n"
             " * El cancelado se hace cuando una remesa fallo.")

    @api.model
    def _get_next_number(self):
        sequence_id = self.env['ir.sequence'].next_by_code('RN') or 'New'
        self.write({'name': sequence_id,
                    'numero': sequence_id})
        return True

    @api.multi
    def contabilizar_remesa(self):
        if not self.company_id.transfer_account_id:
            raise exceptions.except_orm(
                _('Cuenta de Transferencia No Establecida'),
                _('Es requerido Establecer una cuenta para Transferencias Bancarias'))
        if not self.cuenta_id:
            raise exceptions.except_orm(
                _('Cuenta No Selecccionada!'),
                _('Por Favor seleccionar una cuenta bancaria para poder registrar la remesa'))
        if not self.cuenta_id.default_debit_account_id or not self.origen_id.default_credit_account_id:
            raise exceptions.except_orm(
                _('Cuenta No Asignada!'),
                _('Por Favor seleccionar una cuenta bancaria configurada correctamente para poder registrar la remesa'))
        if not self.total:
            raise exceptions.except_orm(
                _('Total No Asignado!'),
                _('Por Favor Ingrese un total valido para poder registrar la remesa'))
        if not self.referencia:
            raise exceptions.except_orm(
                _('Referencia No Asignada!'),
                _('Por Favor Ingrese una referencia valida para poder registrar la remesa'))
        self.move(self.origen_id.id,'a')
        self.move(self.cuenta_id.id,'b')
        return True

    @api.one
    def move(self, journal_id, tipo):

        # obtenemos los datos necesarios
        # ===============================================================
        # cuenta origen
        if tipo == 'a':
          account_debit_id = self.company_id.transfer_account_id.id
          account_credit_id = self.origen_id.default_credit_account_id.id
          
        # cuenta destino
        if tipo == 'b':
          account_debit_id = self.cuenta_id.default_credit_account_id.id
          account_credit_id = self.company_id.transfer_account_id.id
        
        company_id = self.company_id.id
        ref = self.name
        date = self.fecha_remesa  # ime.strftime('%Y-%m-%d')
        saldo = self.total

        account_move_obj = self.env['account.move']
        account_move_line_obj = self.env['account.move.line']
        # state = 'draft'
        # ================================================================

        # creamos el registro en el modelo de los asientos contables
        move_id = account_move_obj.create({
                'name': '/',
                'state': 'draft',
                'ref': ref,
                'journal_id': journal_id,
                'date': date,
                'company_id': company_id,
                })
        # print move_id.id ,"HOLA"
        self.env['list.asientos'].create({
          'asiento_contable_id': move_id.id,
          'remesa_id': self.id})
        # buscamos el asiento contable que ha sido creado
        # para poder enlazarlo con los apuntes contables.
        # move_id = account_move_obj.browse(cr, uid,[('ref','=',ref)],
        # context=context).id

        # ahora crearemos el registro de los apuntes contables
        # crearemos dos registro uno para la cuenta deudora
        # y otro para la cuenta acredora
        
        # Creamos el apunte de la cuenta acreedora
        account_move_line_obj.with_context(check_move_validity=False).create({
                        'name': ref,
                        # 'journal_id': journal_id,
                        # 'ref': ref,
                        'debit': (0.0),
                        'credit': abs(saldo),
                        'account_id': account_credit_id,
                        # 'date': date,
                        'move_id': move_id.id,
                })

        # cuenta deudora
        account_move_line_obj.with_context(check_move_validity=False).create({
                    'name': ref,
                    # 'journal_id': journal_id,
                    # 'ref': ref,
                    'debit': abs(saldo),
                    'credit': (0.0),
                    'account_id': account_debit_id,
                    # 'date': date,
                    'move_id': move_id.id,

                })
        move_id.post()

        self.entered()
        return True

    @api.one
    def entered(self):
        self.state = 'entered'

    @api.one
    def cancel(self):
        self.write(
            {
                'state': 'cancel',
                'cancelada': 'True',
                'name': 'Remesa Cancelada'
            }
        )
        for l in self.list_asientos:
          l.asiento_contable_id.button_cancel()
          l.asiento_contable_id.unlink()
          l.unlink()

    @api.one
    def borrador(self):
        self.write(
            {
                'state': 'draft',
                'name': 'Remesa Borrador'
            }
        )

    @api.one
    def validar(self):
        if self.cancelada:
            # print self.numero
            # print self.cancel
            self.write(
                {
                    'state': 'open',
                    'name': self.numero,
                }
            )
        else:
            self.state = "open"
            self._get_next_number()
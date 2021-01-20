# -*- coding: utf-8 -*-
import time
import calendar
from datetime import date, datetime
from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from . import func


class LibroIva(models.Model):
    _name = 'libro.iva'
    _inherit = ['mail.thread', 'mail.activity.mixin',
                'portal.mixin']  # ## Redes Sociales
    _description = "Libros de Iva"
    _order = 'fecha, mes'

    # campos del encabezado
    name = fields.Char('Nombre', copy=False, default='Libro de Iva',
                       track_visibility='always')

    fecha = fields.Date(string=_('Fecha'),
                        index=True, help=_("Fecha de realizado el informe"),
                        copy=False, default=time.strftime('%Y-%m-%d'),
                        track_visibility='onchange')

    company_id = fields.Many2one('res.company', string=_('Compañia'),
                                 change_default=True,
                                 default=lambda
                                     self: self.env.user.company_id.id)

    company_currency_id = fields.Many2one('res.currency',
                                          related='company_id.currency_id',
                                          string="Company Currency",
                                          readonly=True)

    nrc = fields.Char(string=_("NRC"), readonly=True,
                      help=_("Numero de registro contribuyente"),
                      default=lambda self: self.env.user.company_id.nrc)

    nit = fields.Char(string=_("NIT"), readonly=True,
                      help=_("Numero de Identificacion Tributario"),
                      default=lambda self: self.env.user.company_id.nit)

    mes = fields.Selection([
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    ], string=_("Mes"), index=True, default=time.strftime("%m"), copy=False,
        required=True, track_visibility='onchange')

    state = fields.Selection([
        ('draft', _('Borrador')),
        ('open', _('Validado')),
        ('cancel', _('Cancelado')),
    ], string=_('Estado'), index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=_(
            " * El Borrador sirve para verificar la "
            "informacion correspondiente.\n"
            " * El Validado sirve para dar por realizado el libro de iva.\n"
            " * El cancelado se hace cuando ha fallado un libro."))

    responsable_id = fields.Many2one(
        'res.users', _('Responsable'),
        required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        help=_(
            "Seleccione la persona que validara el libro"),
        track_visibility='always')

    usuario_id = fields.Many2one('res.users', string=_('Usuario'),
                                 readonly=True,
                                 default=lambda self: self.env.user)

    type = fields.Selection(
        [('fcf', 'Libro Consumidor Final'), ('ccf', 'Libro Credito Fiscal'),
         ('compras', 'Libro Compras')], string=None,
        default=lambda self: self._context.get('type', 'fcf'), )

    # campos que contienen el detalle y resumen del reporte.


    libro_line_compras = fields.One2many('libro.line', 'libro_iva_id',
                                         'Lineas Libro', readonly=True)
    libro_line_ccf = fields.One2many('libro.line', 'libro_iva_id',
                                     'Lineas Libro', readonly=True)
    libro_line_fcf = fields.One2many('libro.line', 'libro_iva_id',
                                     'Lineas Libro', readonly=True)
    resumen_line_fcf = fields.One2many('resumen.line', 'libro_iva_id',
                                       'Lineas Resumen', readonly=True)
    resumen_line_ccf = fields.One2many('resumen.line', 'libro_iva_id',
                                       'Lineas Resumen', readonly=True)
    resumen_line_compras = fields.One2many('resumen.line', 'libro_iva_id',
                                           'Lineas Resumen', readonly=True)

    ##################################################
    @api.multi
    def iva_print(self):
        if self.type == 'fcf':
            return self.env.ref(
                'reporte_impuestos_sv.libro_iva_fcf').report_action(self)
        if self.type == 'ccf':
            return self.env.ref(
                'reporte_impuestos_sv.libro_iva_ccf').report_action(self)
        if self.type == 'compras':
            return self.env.ref(
                'reporte_impuestos_sv.libro_iva_compras').report_action(self)

    # funciones para obtener valores
    @api.model
    def create(self, vals):

        meses = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre'
        }
        inv_type = {
            'fcf': 'Consumidor Final',
            'ccf': 'Credito Fiscal',
            'compras': 'Compras'
        }
        mes_actual = meses.get(time.strftime("%m"))
        name = "{} - {} - {}".format(
            inv_type.get(vals.get('type')), str(date.today().year), mes_actual)
        vals.update({'name': name})
        libro_id = super(LibroIva, self).create(vals)
        return libro_id

    @api.one
    def datos_iva_compra(self):
        # Limpiamos registros por cada actualizacion
        func.limpieza(self)
        # Variables Iniciales Requeridas
        company_id = self.company_id.id
        invoice_obj = self.env['account.invoice']
        correlativo = 1
        mes = int(self.mes)
        year = self.fecha.year
        dia = calendar.monthrange(year, mes)
        refund_list = []

        for i in range(dia[1]):
            # aumentamos uno a la variable que representa los dias
            i += 1
            fecha = date(year, mes, i)

            # buscamos todas las facturas del dia
            invoice_list = invoice_obj.search([
                ('date_invoice', '=', fecha),
                ('company_id', '=', company_id),
                '|', ('state', '=', 'paid'),
                ('state', '=', 'open'),
                ('type', '=', 'in_invoice'),
                ('journal_id.type_report', '=', 'compras')],
                order='number, date_invoice')

            for inv_id in invoice_list:
                credito_fiscal = 0
                cg_internas = 0
                cg_importacion = 0
                ce_internas = 0
                ce_importacion = 0
                percepcion = 0
                retencion = 0
                excluidas = 0
                totales = inv_id.amount_total

                name = inv_id.partner_id.name
                nrc = inv_id.partner_id.nrc
                numero = inv_id.reference

                if inv_id.state_refund == 'no_refund':
                    for tax_id in inv_id.tax_line_ids:
                        if tax_id.tax_id.name == 'IVA 13% Compras':
                            credito_fiscal = tax_id.amount_total
                            cg_internas = tax_id.base

                        if tax_id.tax_id.name == 'Importación 13%':
                            credito_fiscal = tax_id.amount_total
                            cg_importacion = tax_id.base

                        if tax_id.tax_id.name == 'Percepción 1%':
                            percepcion = tax_id.amount_total

                    if excluidas != 0:
                        dui = inv_id.partner_id.dui
                        nit = inv_id.partner_id.dui
                    else:
                        dui = nit = False

                    # #print totales,'TOTALES'
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'num_doc': numero,
                        'nrc': nrc,
                        'dui': dui,
                        'nit': nit,
                        'name': name,
                        'internas_e': ce_internas,
                        'importaciones_e': ce_importacion,
                        'internas_g': cg_internas,
                        'importaciones_g': cg_importacion,
                        'iva_credito_g': credito_fiscal,
                        'retenciones': retencion,
                        'percepcion': percepcion,
                        'totales': totales,
                        'excluidas': excluidas,
                    })
                else:
                    refund_list.append(inv_id.inv_refund_id.id)
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'num_doc': numero,
                        'nrc': nrc,
                        'dui': dui,
                        'nit': nit,
                        'name': name,
                        'internas_e': ce_internas,
                        'importaciones_e': ce_importacion,
                        'internas_g': cg_internas,
                        'importaciones_g': cg_importacion,
                        'iva_credito_g': credito_fiscal,
                        'retenciones': retencion,
                        'percepcion': percepcion,
                        'totales': totales,
                        'excluidas': excluidas,
                    })
                # aumentamos el correlativo de cantidad de facturas
                correlativo += 1

            tax_ids = self.env['account.tax'].search([
                ('company_id', '=', company_id),
                ('type_tax_use', '=', 'none'),
                #('tax_adjustment', '=', True)
            ])
            for tax in tax_ids:

                move_list = self.env['account.move.line'].search([
                    ('tax_line_id', '=', tax.id),
                    ('account_id', '=', tax.account_id.id),
                    ('company_id', '=', company_id),
                    ('date', '=', fecha)])
                ##print move_list
                for m in move_list:
                    iva = m.balance if tax.type_tax == 'iva_compra' else 0
                    retencion = m.balance if tax.type_tax == 'retencion' else 0
                    percepcion = m.balance if tax.type_tax == 'percepcion1' or \
                                              tax.type_tax == 'percepcion2' \
                        else 0
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'num_doc': m.name,
                        'nrc': m.partner_id.nrc,
                        # 'dui': m.partner_id.dui,
                        # 'nit': m.partner_id.nit,
                        'name': m.partner_id.name,
                        'internas_e': 0,
                        'importaciones_e': 0,
                        'internas_g': 0,
                        'importaciones_g': 0,
                        'iva_credito_g': iva,
                        'retenciones': retencion,
                        'percepcion': percepcion,
                        'totales': iva + retencion + percepcion,
                        'excluidas': m.balance if tax.type_tax == 'exento' else 0,
                    })
                    correlativo += 1

            refund_old = self.env['account.invoice'].search([
                ('id', 'not in', refund_list),
                ('state', '=', 'paid'),
                ('date_invoice', '=', fecha),
                ('type', '=', "out_refund"),
                ('journal_id.type_report', '=', 'anu_compras')])

            for r_id in refund_old:
                for tax_id in r_id.tax_line_ids:
                    if tax_id.tax_id.type_tax == 'tax1':
                        credito_fiscal += tax_id.amount
                        cg_internas += tax_id.base
                    if tax_id.tax_id.type_tax == 'exento':
                        ce_internas += tax_id.base
                        # #print ventas_exentas, 'EXENTAS'
                    if tax_id.tax_id.type_tax == 'tax5':
                        percepcion += abs(tax_id.amount)
                    if tax_id.tax_id.type_tax == 'tax6':
                        retencion += abs(tax_id.amount)
                    if tax_id.tax_id.type_tax == 'excluidos':
                        excluidas += tax_id.base
                    if tax_id.tax_id.type_tax == 'importacion':
                        cg_importacion += tax_id.base
                        credito_fiscal += tax_id.amount
                totales = inv_id.amount_total
                if excluidas != 0:
                    dui = inv_id.partner_id.dui
                    nit = inv_id.partner_id.dui
                else:
                    dui = nit = False

                self.env['libro.line'].create({
                    'libro_iva_id': self.id,
                    'correlativo': correlativo,
                    'fecha_doc': fecha,
                    'num_doc': numero,
                    'nrc': nrc,
                    'dui': dui,
                    'nit': nit,
                    'name': name,
                    'internas_e': ce_internas * -1,
                    'importaciones_e': ce_importacion * -1,
                    'internas_g': cg_internas * -1,
                    'importaciones_g': cg_importacion * -1,
                    'iva_credito_g': credito_fiscal * -1,
                    'retenciones': retencion * -1,
                    'percepcion': percepcion * -1,
                    'totales': totales * -1,
                    'excluidas': excluidas * -1,
                })

        self.resumen_compras()
        return True

    ##################################################

    @api.one
    def resumen_compras(self):
        # Inicio de variables

        internas_e = 0
        importaciones_e = 0
        internas_g = 0
        importaciones_g = 0
        iva_credito_g = 0
        retenciones = 0
        percepciones = 0
        totales = 0
        excluidas = 0

        # recorremos todas las lineas para obtener datos
        for l in self.libro_line_compras:
            internas_e += l.internas_e
            importaciones_e += l.importaciones_e
            internas_g += l.internas_g
            importaciones_g += l.importaciones_g
            iva_credito_g += l.iva_credito_g
            retenciones += l.retenciones
            percepciones += l.percepcion
            totales += l.totales
            excluidas = l.excluidas
            # # print ventas_exentas, ventas_gravadas, exportaciones,
            # retenciones, debito_fiscal, totales

        # guardamos todos los resumen
        self.env['resumen.line'].create({
            'detalle': "Compras Internas Exentas",
            'total': internas_e,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Importaciones Exentas",
            'total': importaciones_e,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Compras Internas Gravadas",
            'total': internas_g,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Importaciones Gravadas",
            'total': importaciones_g,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Credito Fiscal",
            'total': iva_credito_g,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Retenciones",
            'total': retenciones,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Percepciones",
            'total': percepciones,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Totales",
            'total': totales,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Compras Excluidas",
            'total': excluidas,
            'libro_iva_id': self.id,
        })

    ##################################################

    @api.one
    def datos_iva_ccf(self):
        # Limpiamos registros por cada actualizacion
        func.limpieza(self)
        # Variables Iniciales Requeridas
        company_id = self.company_id.id
        invoice_obj = self.env['account.invoice']
        correlativo = 1
        mes = int(self.mes)
        year = self.fecha.year
        dia = calendar.monthrange(year, mes)
        refund_list = []

        for i in range(dia[1]):
            # variables iniciales requeridas por dia
            # aumentamos uno a la variable que representa los dias
            i += 1
            fecha = date(year, mes, i)

            # buscamos todas las facturas del dia
            invoice_list = invoice_obj.search([
                ('date_invoice', '=', fecha),
                ('company_id', '=', company_id),
                ('state', 'in', ['open', 'paid']),
                ('type', '=', 'out_invoice'),
                ('journal_id.type_report', '=', 'ccf')],
                order='number, date_invoice')

            for inv_id in invoice_list:
                debito_fiscal = 0
                ventas_gravadas = 0
                ventas_exentas = 0
                retenciones = 0
                totales = inv_id.amount_total
                # metodos si es factura no retificada
                numeracion = func.numeracion(inv_id.number)

                # #print numeracion,'Datos'
                prefijo = numeracion.get('pre')
                longitud = numeracion.get('longitud')
                numero = int(numeracion.get('num'))
                name = inv_id.partner_id.name
                nrc = inv_id.partner_id.nrc

                if inv_id.state_refund == 'no_refund':
                    for tax_id in inv_id.tax_line_ids:
                        if tax_id.tax_id.name == 'IVA 13% Ventas':
                            debito_fiscal = tax_id.amount_total
                            ventas_gravadas += tax_id.base
                            # #print debito_fiscal,ventas_gravadas,'IVA'
                        if tax_id.tax_id.name == 'Retención 1%':
                            retenciones = tax_id.amount_total

                    # #print debito_fiscal,ventas_gravadas,'IVA'
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'num_doc': numero,
                        'prefijo': prefijo,
                        'name': name,
                        'nrc': nrc,
                        'exentas_nosujetas': ventas_exentas,
                        'gravadas': ventas_gravadas,
                        'retenciones': retenciones,
                        'debito_fiscal': debito_fiscal,
                        'totales': totales,
                    })
                else:
                    if datetime.strftime(inv_id.inv_refund_id.date_invoice, '%Y-%m-%d'):
                        refund_list.append(inv_id.inv_refund_id.id)
                        self.env['libro.line'].create({
                            'libro_iva_id': self.id,
                            'correlativo': correlativo,
                            'fecha_doc': fecha,
                            'num_doc': numero,
                            'prefijo': prefijo,
                            'name': name,
                            'nrc': nrc,
                            'exentas_nosujetas': 0,
                            'gravadas': 0,
                            'retenciones': 0,
                            'debito_fiscal': 0,
                            'totales': 0,
                        })
                    else:
                        for tax_id in inv_id.tax_line_ids:
                            if tax_id.tax_id.type_tax == 'IVA 13% Venta':
                                debito_fiscal += tax_id.amount_total
                                ventas_gravadas += tax_id.base
                                # #print debito_fiscal,ventas_gravadas,'IVA'
                            if tax_id.tax_id.type_tax == 'exento':
                                ventas_exentas += tax_id.base + tax_id.amount_total
                                ##print ventas_exentas, 'EXENTAS'
                            if tax_id.tax_id.type_tax == 'Retencion 1%':
                                retenciones += abs(tax_id.amount_total)
                                ##print retenciones, 'RETENCIONES'

                        totales = ventas_gravadas + debito_fiscal + ventas_exentas
                        # #print debito_fiscal,ventas_gravadas,'IVA'
                        self.env['libro.line'].create({
                            'libro_iva_id': self.id,
                            'correlativo': correlativo,
                            'fecha_doc': fecha,
                            'num_doc': numero,
                            'prefijo': prefijo,
                            'name': name,
                            'nrc': nrc,
                            'exentas_nosujetas': ventas_exentas,
                            'gravadas': ventas_gravadas,
                            'retenciones': retenciones,
                            'debito_fiscal': debito_fiscal,
                            'totales': totales,
                        })
                # aumentamos el correlativo de cantidad de facturas
                correlativo += 1
            # Buscamos Facturas Anuladas de mes anteriores
            refund_old = self.env['account.invoice'].search([
                ('id', 'not in', refund_list),
                ('state', '=', 'paid'),
                ('date_invoice', '=', fecha),
                ('type', '=', "out_refund"),
                ('journal_id.type_report', 'in', ['anu', 'ndc']),
                ('inv_refund_id.journal_id.type_report', '=', 'ccf')])

            for r_id in refund_old:
                debito_fiscal = 0
                ventas_gravadas = 0
                ventas_exentas = 0
                retenciones = 0
                totales = 0

                for tax_id in r_id.tax_line_ids:
                    if tax_id.tax_id.type_tax == 'IVA 13% Venta':
                        debito_fiscal += tax_id.amount_total
                        ventas_gravadas += tax_id.base
                        # #print debito_fiscal,ventas_gravadas,'IVA'
                    if tax_id.tax_id.type_tax == 'exento':
                        ventas_exentas += tax_id.base + tax_id.amount
                        # #print ventas_exentas, 'EXENTAS'
                    if tax_id.tax_id.type_tax == 'Retencion 1%':
                        retenciones += abs(tax_id.amount)
                        # #print retenciones, 'RETENCIONES'
                totales = r_id.amount_total

                self.env['libro.line'].create({
                    'libro_iva_id': self.id,
                    'correlativo': correlativo,
                    'fecha_doc': fecha,
                    'num_doc': numero,
                    'prefijo': prefijo,
                    'name': name,
                    'nrc': nrc,
                    'exentas_nosujetas': ventas_exentas * -1,
                    'gravadas': ventas_gravadas * -1,
                    'retenciones': retenciones * -1,
                    'debito_fiscal': debito_fiscal * -1,
                    'totales': totales * -1,
                })

        self.resumen_ccf()
        return True

    @api.one
    def resumen_ccf(self):
        # Inicio de variables
        ventas_exentas = 0
        ventas_gravadas = 0
        retenciones = 0
        debito_fiscal = 0
        totales = 0

        # recorremos todas las lineas para obtener datos
        for l in self.libro_line_ccf:
            ventas_exentas += l.exentas_nosujetas
            ventas_gravadas += l.gravadas
            retenciones += l.retenciones
            debito_fiscal += l.debito_fiscal
            totales += l.totales
            # #print ventas_exentas, ventas_gravadas,
            # exportaciones, retenciones, debito_fiscal, totales

        # guardamos todos los resumen
        self.env['resumen.line'].create({
            'detalle': "Ventas Exentas",
            'total': ventas_exentas,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Gravadas",
            'total': ventas_gravadas,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Debito Fiscal",
            'total': debito_fiscal,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Retenciones",
            'total': retenciones,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Totales",
            'total': totales,
            'libro_iva_id': self.id,
        })

    # #################################################
    @api.one
    def datos_iva_fcf(self):
        # limpiamos registros por cada actualizacion
        func.limpieza(self)
        # Variables Iniciales Requeridas
        company_id = self.company_id.id
        invoice_obj = self.env['account.invoice']
        h = 0
        mes = int(self.mes)
        # #print self.fecha
        year = self.fecha.year
        # #print year
        dia = calendar.monthrange(year, mes)
        refund_list = []
        for i in range(dia[1]):
            # variables iniciales requeridas por dia
            num_inicial = 0
            num_final = 0
            ventas_exentas = 0
            ventas_gravadas = 0
            exportaciones = 0
            nosujetas = 0
            ventas_totales = 0
            debito_fiscal = 0

            # aumentamos uno a la variable que representa los dias
            i += 1

            fecha = date(year, mes, i)
            ##print fecha
            # buscamos todas las facturas del dia
            invoice_list = invoice_obj.search([
                ('date_invoice', '=', fecha),
                ('company_id', '=', company_id),
                '|', ('state', '=', 'paid'),
                ('state', '=', 'open'),
                ('type', '=', 'out_invoice'),
                ('journal_id.type_report', '=', 'fcf')],
                order='number, date_invoice')

            # #print invoice_list,'LISTADO DE FACTURAS'
            # revisamos toda las facturas del dia
            prefijo_ant = 0
            numero_ant = 0
            for inv_id in invoice_list:

                # validamos que no esta retificada
                if inv_id.state_refund == 'no_refund':
                    # metodos si es factura no retificada
                    numeracion = func.numeracion(inv_id.number)

                    # #print numeracion,'Datos'
                    prefijo = numeracion.get('pre')
                    longitud = numeracion.get('longitud')
                    numero = int(numeracion.get('num'))
                    # #print numero,'Numero'
                    # #print num_inicial, 'Incial'
                    # #print numero_ant, 'Num Anterior'

                    if num_inicial == 0:
                        num_inicial = inv_id.number
                        num_final = inv_id.number
                        num_anterior = numero
                        prefijo_ant = prefijo

                    else:

                        if prefijo_ant != prefijo or (
                                num_anterior) != numero:
                            # Guardar
                            self.env['libro.line'].create({
                                'libro_iva_id': self.id,
                                'dia': i,
                                'num_inicial': num_inicial,
                                'num_final': num_final,
                                'exentas_nosujetas': ventas_exentas,
                                'gravadas': ventas_gravadas,
                                'exportaciones': exportaciones,
                                'nosujetas': nosujetas,
                                'totales': ventas_totales,
                                'debito_fiscal': debito_fiscal,
                            })
                            num_anterior = numero
                            num_inicial = inv_id.number
                            num_final = inv_id.number
                            ventas_exentas = 0
                            ventas_gravadas = 0
                            exportaciones = 0
                            retenciones = 0
                            ventas_totales = 0
                            debito_fiscal = 0
                            prefijo_ant = prefijo
                            h = 0  # Datos Guardados
                        else:
                            if prefijo_ant == prefijo:
                                prefijo_ant = prefijo
                            if (num_anterior + 1) == numero:
                                num_anterior = numero
                                num_final = inv_id.number

                    # Generamos datos a guardarse
                    for tax_id in inv_id.tax_line_ids:
                        # #print tax_id.tax_id.name
                        # #print tax_id.tax_id.type_tax
                        # ventas normales
                        if tax_id.tax_id.name == 'IVA 13% Ventas':
                            ventas_gravadas += tax_id.base + tax_id.amount_total
                            ventas_totales += tax_id.base + tax_id.amount_total
                            debito_fiscal += tax_id.amount_total
                        if tax_id.tax_id.name == 'Exportaciones 0%':
                            exportaciones += tax_id.base + tax_id.amount_total
                            ventas_totales += tax_id.base + tax_id.amount_total
                        if tax_id.tax_id.name == 'Exentas 0%':
                            ventas_exentas += tax_id.base + tax_id.amount_total
                            ventas_totales += tax_id.base + tax_id.amount_total
                        if tax_id.tax_id.name == 'No sujetas 0%':
                            nosujetas += tax_id.base + tax_id.amount_total
                            ventas_totales += tax_id.base + tax_id.amount_total



                    h = 1  # establecemos que hay valors sin guardarse

                else:
                    # validamos que la anulacion sea del mes correspondiente
                    if datetime.strftime(inv_id.inv_refund_id.date_invoice,
                                         '%Y-%m-%d'):
                        refund_list.append(inv_id.inv_refund_id.id)
                        # debemos guardar los datos buenos
                        # creamos un salto guardamos los datos
                        # de la retificativa
                        # metodos si es factura retificada

                        if h == 1:
                            # #print 'Guardar Datos Buenos'
                            self.env['libro.line'].create({
                                'libro_iva_id': self.id,
                                'dia': i,
                                'num_inicial': num_inicial,
                                'num_final': num_final,
                                'exentas_nosujetas': ventas_exentas,
                                'gravadas': ventas_gravadas,
                                'exportaciones': exportaciones,
                                'nosujetas': nosujetas,
                                'totales': ventas_totales,
                                'debito_fiscal': debito_fiscal,
                            })
                            h = 0  # Datos Guardados

                        num_inicial = inv_id.number
                        num_final = inv_id.number
                        ventas_exentas = 0
                        ventas_gravadas = 0
                        exportaciones = 0
                        nosujetas = 0
                        ventas_totales = 0
                        debito_fiscal = 0

                        self.env['libro.line'].create({
                            'libro_iva_id': self.id,
                            'dia': i,
                            'num_inicial': num_inicial,
                            'num_final': num_final,
                            'exentas_nosujetas': ventas_exentas,
                            'gravadas': ventas_gravadas,
                            'exportaciones': exportaciones,
                            'nosujetas': nosujetas,
                            'totales': ventas_totales,
                            'debito_fiscal': debito_fiscal,
                        })
                        h = 0  # Datos Guardados

                        num_inicial = 0
                        num_final = 0

                        ##print 'RETIFICADA'

            # validamos que no existan datos sin guardar al salir
            if h == 1:
                h = 0  # Datos Guardados
                self.env['libro.line'].create({
                    'libro_iva_id': self.id,
                    'dia': i,
                    'num_inicial': num_inicial,
                    'num_final': num_final,
                    'exentas_nosujetas': ventas_exentas,
                    'gravadas': ventas_gravadas,
                    'exportaciones': exportaciones,
                    'nosujetas': nosujetas,
                    'totales': ventas_totales,
                    'debito_fiscal': debito_fiscal,
                })
                ventas_exentas = 0
                ventas_gravadas = 0
                exportaciones = 0
                nosujetas = 0
                ventas_totales = 0
                debito_fiscal = 0

            # Buscamos Facturas Anuladas de mes anteriores
            print(refund_list)
            refund_old = self.env['account.invoice'].search([
                ('id', 'not in', refund_list),
                ('state', '=', 'paid'),
                ('date_invoice', '=', fecha),
                ('type', '=', "out_refund"),
                ('journal_id.type_report', 'in', ['anu', 'ndc']),
                ('inv_refund_id.journal_id.type_report', '=', 'fcf')])

            for r_id in refund_old:
                for tax_id in r_id.tax_line_ids:
                    # #print tax_id.tax_id.name
                    # #print tax_id.tax_id.type_tax
                    # ventas normales
                    if tax_id.tax_id.type_tax == 'tax2':
                        debito_fiscal += tax_id.amount
                        ventas_gravadas += tax_id.base + tax_id.amount
                    if tax_id.tax_id.type_tax == 'exento':
                        ventas_exentas += tax_id.base + tax_id.amount
                    if tax_id.tax_id.type_tax == 'tax6':
                        retenciones += abs(tax_id.amount)
                    if tax_id.tax_id.type_tax == 'tax4':
                        exportaciones += tax_id.base
                    ventas_totales = ventas_gravadas + ventas_exentas + exportaciones

                self.env['libro.line'].create({
                    'libro_iva_id': self.id,
                    'dia': i,
                    'num_inicial': r_id.inv_refund_id.number,
                    'num_final': r_id.inv_refund_id.number,
                    'exentas_nosujetas': ventas_exentas * -1,
                    'gravadas': ventas_gravadas * -1,
                    'exportaciones': exportaciones * -1,
                    'nosujetas': nosujetas * -1,
                    'totales': ventas_totales * -1,
                    'debito_fiscal': debito_fiscal * -1,
                })
                num_inicial = inv_id.number
                num_final = inv_id.number
                ventas_exentas = 0
                ventas_gravadas = 0
                exportaciones = 0
                nosujetas = 0
                ventas_totales = 0
                debito_fiscal = 0

        self.resumen_fcf()

    @api.one
    def resumen_fcf(self):
        # Inicio de variables
        ventas_exentas = 0
        ventas_gravadas = 0
        exportaciones = 0
        nosujetas = 0
        debito_fiscal = 0
        totales = 0

        # recorremos todas las lineas para obtener datos
        for l in self.libro_line_fcf:
            ventas_exentas += l.exentas_nosujetas
            ventas_gravadas += l.gravadas
            exportaciones += l.exportaciones
            nosujetas += l.nosujetas
            debito_fiscal += l.debito_fiscal
            totales = ventas_exentas + ventas_gravadas + exportaciones
            # #print ventas_exentas, ventas_gravadas, exportaciones,
            # retenciones, debito_fiscal, totales

        # guardamos todos los resumen
        self.env['resumen.line'].create({
            'detalle': "Ventas Exentas",
            'total': ventas_exentas,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Gravadas",
            'total': ventas_gravadas,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Exportaciones",
            'total': exportaciones,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Debito Fiscal",
            'total': debito_fiscal,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Totales",
            'total': totales,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "No Sujetas",
            'total': nosujetas,
            'libro_iva_id': self.id,
        })

# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019 
#
##############################################################################
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class cheque_setting(models.Model):
    _name = 'cheque.setting'

    name = fields.Char('Nombre', required="1")
    font_size = fields.Float('Tamaño Fuente', default="13", required="1")
    color = fields.Char('Color', default="#000", required="1")
    set_default = fields.Boolean('Cheque por defecto', copy=False)
    company_id = fields.Many2one('res.company',string='Compañia', default=lambda self:self.env.user.company_id.id, required="1")

    is_partner = fields.Boolean('Print Beneficiario', default=True)
    is_partner_bold = fields.Boolean('En Negrita')
    partner_text = fields.Selection([('prefix', 'Prefijo'), ('suffix', 'Sufijo')], string='Titulo')
    partner_m_top = fields.Float('From Top', default=130)
    partner_m_left = fields.Float('From Left', default=70)

    is_date = fields.Boolean('Print Fecha', default=True)
    date_formate = fields.Selection([('dd_mm', 'DD MM'), ('mm_dd', 'MM DD')], string='Formato Fecha', default='dd_mm')
    year_formate = fields.Selection([('yy', 'YY'), ('yyyy', 'YYYY')], string='Formato de Año', default='yy')
    date_m_top = fields.Float('From Top', default=90)
    f_d_m_left = fields.Float('1er Digito', default=550)
    s_d_m_left = fields.Float('2do Digito', default=560)
    t_d_m_left = fields.Float('3er Digito', default=590)
    fo_d_m_left = fields.Float('4to Digito', default=600)
    fi_d_m_left = fields.Float('5to Digito', default=625)
    si_d_m_left = fields.Float('6to Digito', default=635)
    se_d_m_left = fields.Float('7mo Digito', default=645)
    e_d_m_left = fields.Float('8vo Digito', default=655)
    
    date_seprator = fields.Char('Separador')

    is_amount = fields.Boolean('Print Monto', default=True)
    amt_m_top = fields.Float('From Top', default=185)
    amt_m_left = fields.Float('From Left', default=550)
    is_star = fields.Boolean('Print Asteriscos', help="Si está activo imprime 3 ateriscos antes y depsués del monto", default=True)

    is_currency = fields.Boolean('Print Moneda')

    is_amount_word = fields.Boolean('Print Monto Letras', default=True)
    is_word_bold = fields.Boolean('En Negrita')
    word_in_f_line = fields.Float('Separar monto Letras', default=5,
                                  help="Cantidad de palabras que desea imprimir en la linea 1, el resto va en la 2")
    amt_w_m_top = fields.Float('From First Top', default=158.76)
    amt_w_m_left = fields.Float('From First Left', default=70)
    is_star_word = fields.Boolean('Print Ateriscos', help="Si está activo imprime 3 ateriscos antes y depsués del monto",
                                  default=True)

    amt_w_s_m_top = fields.Float('From Sec Top', default=185)
    amt_w_s_m_left = fields.Float('From Sec Left', default=70)

    is_company = fields.Boolean('Activar')
    c_margin_top = fields.Float('From Top', default=280)
    c_margin_left = fields.Float('From Left', default=560)

    print_journal = fields.Boolean('Activar')
    journal_margin_top = fields.Float('From Top', default=700)
    journal_margin_left = fields.Float('From Left', default=10)

    is_stub = fields.Boolean('Activar')
    stub_margin_top = fields.Float('From Top', default=400)
    stub_margin_left = fields.Float('From Left', default=10)

    is_cheque_no = fields.Boolean('Activar')
    cheque_margin_top = fields.Float('From Top', default=50)
    cheque_margin_left = fields.Float('From Left', default=520)

    is_free_one = fields.Boolean('Activar')
    f_one_margin_top = fields.Float('From Top', default=255)
    f_one_margin_left = fields.Float('From Left', default=70)

    is_free_two = fields.Boolean('Activar')
    f_two_margin_top = fields.Float('From Top', default=255)
    f_two_margin_left = fields.Float('From Left', default=300)

    is_acc_pay = fields.Boolean('Activar', default=True)
    acc_pay_m_top = fields.Float('From Top', default=50)
    acc_pay_m_left = fields.Float('From Left', default=50)
    
    is_f_line_sig = fields.Boolean('Activar')
    f_sig_m_top = fields.Float('From Top', default=255)
    f_sig_m_left = fields.Float('From Left', default=510)
    
    is_s_line_sig = fields.Boolean('Activar')
    s_sig_m_top = fields.Float('From Top', default=350)
    s_sig_m_left = fields.Float('From Left', default=510)
    
    
    @api.constrains('set_default', 'company_id')
    def _check_description(self):
        for line in self:
            if line.set_default:
                line_ids = self.env['cheque.setting'].search([('set_default','=',True),('company_id','=',line.company_id.id)])
                if len(line_ids) > 1:
                    raise ValidationError("Cada compañia tiene un formato de Cheque por Default")

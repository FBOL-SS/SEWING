# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError, AccessError
import csv
import base64
import io as StringIO
import xlrd
from odoo.tools import ustr

class import_emp_timesheet_wizard(models.TransientModel):
    _name="import.emp.timesheet.wizard"
    _description = "Import Employee Timesheet Wizard"       

    import_type = fields.Selection([
        ('csv','CSV File'),
        ('excel','Excel File')
        ], default="csv", string="Import File Type", required=True)
    file = fields.Binary(string="File",required=True)  
    
    @api.multi
    def show_success_msg(self,counter,skipped_line_no):
        
        #to close the current active wizard        
        action = self.env.ref('sh_all_in_one_import.sh_import_emp_timesheet_action').read()[0]
        action = {'type': 'ir.actions.act_window_close'} 
        
        #open the new success message box    
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False                                   
        context = dict(self._context or {})
        dic_msg = str(counter) + " Records imported successfully"
        if skipped_line_no:
            dic_msg = dic_msg + "\nNote:"
        for k,v in skipped_line_no.items():
            dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        context['message'] = dic_msg   
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
            }   

    
    @api.multi
    def import_emp_timesheet_apply(self):

        analytic_line_obj = self.env['account.analytic.line']
        #perform import lead
        if self and self.file:
            #For CSV
            if self.import_type == 'csv':
                counter = 1
                skipped_line_no = {}
                try:
                    file = str(base64.decodestring(self.file).decode('utf-8'))
                    myreader = csv.reader(file.splitlines())
                    skip_header=True
                    
                    for row in myreader:
                        try:
                            if skip_header:
                                skip_header=False
                                counter = counter + 1
                                continue
                            
                            if row[0] not in (None,"") and row[1] not in (None,"") and row[2] not in (None,"") and row[3] not in (None,""):
                                vals={}
                                
                                cd = row[0]                
                                cd = str(datetime.strptime(cd, '%Y-%m-%d').date())   
                                vals.update({'date' : cd})
                                
                                search_emp = self.env['hr.employee'].search([('name','=', row[1] )], limit = 1)   
                                if search_emp:
                                    vals.update({'employee_id' : search_emp.id})
                                else:
                                    skipped_line_no[str(counter)] = " - Employee not found. " 
                                    counter = counter + 1
                                    continue             
                                                            
                                vals.update({'name' : row[2] })
                                
                                
                                search_project = self.env['project.project'].search([ ('name', '=', row[3] )], limit = 1)
                                if search_project and search_project.allow_timesheets:
                                    vals.update({'project_id' : search_project.id })
                                else:
                                    skipped_line_no[str(counter)] = " - Project not found or it's not Allow timesheets" 
                                    counter = counter + 1
                                    continue
                                
                                if row[4] not in (None,""):
                                    search_task = self.env['project.task'].search([ ('name', '=', row[4] ) ], limit = 1)
                                    if search_task and search_task.project_id == search_project:
                                        vals.update({'task_id' : search_task.id})
                                    else:
                                        skipped_line_no[str(counter)] = " - Task not found or it's not belongs to this project - " + search_project.name  
                                        counter = counter + 1
                                        continue
                                    
                                if row[5] not in (None,""):
                                    vals.update({'unit_amount' : row[5]})
                                else:
                                    vals.update({'unit_amount' : 0.0})                                                                         
                                
                                analytic_line_obj.create(vals)
                                counter = counter + 1                             
                                
                            else:
                                skipped_line_no[str(counter)] = " - Date, Employee, Description or Project field is empty. "                                   
                                counter = counter + 1                                

                        except Exception as e:
                            skipped_line_no[str(counter)]=" - Value is not valid. " + ustr(e)   
                            counter = counter + 1 
                            continue          
                            
                except Exception as e:
                    raise UserError(_("Sorry, Your csv file does not match with our format. "+ ustr(e) ))
                
                if counter > 1:
                    completed_records = (counter - len(skipped_line_no)) - 2
                    res = self.show_success_msg(completed_records, skipped_line_no)
                    return res

            
            #For Excel
            if self.import_type == 'excel':
                counter = 1
                skipped_line_no = {}                  
                try:
                    wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
                    sheet = wb.sheet_by_index(0)     
                    skip_header = True    
                    for row in range(sheet.nrows):
                        try:
                            if skip_header:
                                skip_header = False
                                counter = counter + 1
                                continue
                            
                            if sheet.cell(row,0).value not in (None,"") and sheet.cell(row,1).value not in (None,"") and sheet.cell(row,2).value not in (None,"") and sheet.cell(row,3).value not in (None,""):
                                vals={}
                                
                                cd = sheet.cell(row,0).value                
                                cd = str(datetime.strptime(cd, '%Y-%m-%d').date())   
                                vals.update({'date' : cd})
                                
                                search_emp = self.env['hr.employee'].search([('name','=', sheet.cell(row,1).value )], limit = 1)   
                                if search_emp:
                                    vals.update({'employee_id' : search_emp.id})
                                else:
                                    skipped_line_no[str(counter)] = " - Employee not found. " 
                                    counter = counter + 1
                                    continue             
                                                            
                                vals.update({'name' : sheet.cell(row,2).value })
                                
                                
                                search_project = self.env['project.project'].search([ ('name', '=', sheet.cell(row,3).value )], limit = 1)
                                if search_project and search_project.allow_timesheets:
                                    vals.update({'project_id' : search_project.id })
                                else:
                                    skipped_line_no[str(counter)] = " - Project not found or it's not Allow timesheets" 
                                    counter = counter + 1
                                    continue
                                
                                if sheet.cell(row,4).value not in (None,""):
                                    search_task = self.env['project.task'].search([ ('name', '=', sheet.cell(row,4).value ) ], limit = 1)
                                    if search_task and search_task.project_id == search_project:
                                        vals.update({'task_id' : search_task.id})
                                    else:
                                        skipped_line_no[str(counter)] = " - Task not found or it's not belongs to this project - " + search_project.name  
                                        counter = counter + 1
                                        continue
                                    
                                if sheet.cell(row,5).value not in (None,""):
                                    vals.update({'unit_amount' : sheet.cell(row,5).value})
                                else:
                                    vals.update({'unit_amount' : 0.0})                                                                         
                                
                                analytic_line_obj.create(vals)
                                counter = counter + 1                             
                                
                            else:
                                skipped_line_no[str(counter)] = " - Date, Employee, Description or Project field is empty. "                                   
                                counter = counter + 1                                

                        except Exception as e:
                            skipped_line_no[str(counter)]=" - Value is not valid. " + ustr(e)   
                            counter = counter + 1 
                            continue          
                            
                except Exception as e:
                    raise UserError(_("Sorry, Your excel file does not match with our format. "+ ustr(e) ))
                
                if counter > 1:
                    completed_records = (counter - len(skipped_line_no)) - 2
                    res = self.show_success_msg(completed_records, skipped_line_no)
                    return res
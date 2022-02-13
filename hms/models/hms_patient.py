
from codeop import CommandCompiler
from dataclasses import field
from odoo import models, fields, api

class HmsPatient( models.Model ):
    _name = 'hms.patient'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    state = fields.Selection([
        ('fair', 'Fair'),
        ('undetermined', 'undetermined'),
        ('good', 'good'),
        ('serious', 'serious'),
        ])
    age = fields.Integer()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection( [
                    ('A', 'type A'), 
                    ('B', 'type B'), 
                    ('O', 'type O'), 
                    ('AB', 'type AB'),
                ])
    pcr = fields.Boolean() 
    image = fields.Image() 
    address = fields.Text() 
    department_id = fields.Many2one(comodel_name='hms.department')
    doctors_ids = fields.Many2many(comodel_name='hms.doctor')
    log_id = fields.Many2one(comodel_name='hms.patient.log')

    department_capacity = fields.Integer(related='department_id.capacity')


    @api.onchange('age')
    def _onchange_age( self ):
        if self.age and self.age < 30: 
            self.pcr = True
            return {
                'warning': {
                    'title': 'warning',
                    'message': 'pcr is checked'
                }
            }
    

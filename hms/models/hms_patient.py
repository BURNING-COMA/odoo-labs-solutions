import re

from odoo import models, fields, api 
from odoo.exceptions import ValidationError

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
    # TODO complete last step in lab 2 related to creating a log whenever state changes
    log_id = fields.Many2one(comodel_name='hms.patient.log')

    department_capacity = fields.Integer(related='department_id.capacity')

    # TODO link model hms.patient with model res.partner.inhert ( as one2one )
    # https://www.odoo.com/forum/help-1/one2one-relational-field-187864
    customer_id = fields.Many2one( comodel_name='res.partner' )


    # DONE add API constraint is_valide,
    # DONE sql constrain UNIQUE 
    email = fields.Char()


    _sql_constraints = [
        ("email_uniqueness", "UNIQUE(email)", "Email is already registered.")
    ]

    @api.constrains('email')
    def _check_email(self):
        for record in self: 
            # DONE use python regix to validate email ..
            # https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
            # https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression
            # just basic email check, no need for compelx check since further verifications will be done anyway 
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", record.email): 
                raise ValidationError(f"'{record.email}' is not a valid email.")




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
    

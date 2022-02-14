import re
from datetime import date

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
    age = fields.Integer( compute='_compute_age', store=True)
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
    log_ids = fields.One2many(comodel_name='hms.patient.log', inverse_name='patient_id')
    customer_ids = fields.One2many(comodel_name='res.partner', inverse_name='related_patient_id')

    department_capacity = fields.Integer(related='department_id.capacity')

    # DONE link model hms.patient with model res.partner.inhert ( as one2one )
    # https://www.odoo.com/forum/help-1/one2one-relational-field-187864
    # customer_id = fields.One2many(comodel_name='res.partner', inverse_name='related_patient_ids')


    customer_id = fields.Many2one(comodel_name='res.partner')
    # DONE add API constraint is_valide,
    # DONE sql constrain UNIQUE 
    email = fields.Char()

    _sql_constraints = [
        ("email_uniqueness", "UNIQUE(email)", "Email is already registered.")
    ]

    @api.constrains('state')
    def _onchange_state(self):
        if self.state: 
            self.env[
    'hms.patient.log'].create({'description':f"(State changed to {self.state}",'patient_id': self.id  })

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self: 
            if record.birth_date:
                record.age = date.today().year - record.birth_date.year
            else: 
                record.age = 0

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
    

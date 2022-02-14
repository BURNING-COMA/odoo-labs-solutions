from odoo import models, fields

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'


    description = fields.Char(required=True)
    patient_id = fields.Many2one(comodel_name='hms.patient')
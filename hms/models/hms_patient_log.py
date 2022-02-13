from odoo import models, fields

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'

    description = fields.Char(Required=True)

    patient_ids = fields.One2many(comodel_name='hms.patient', inverse_name='log_id')
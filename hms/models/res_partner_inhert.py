from odoo import models, fields, api

class ResPartnerInhert( models.Model ):
    _name = 'res.partner'
    _inherit = 'res.partner'

    # TODO make relation between patient and customer one2one
    related_patient_ids = fields.One2many( comodel_name='hms.patient', inverse_name='customer_id', 
            string='related patient ID')   

 
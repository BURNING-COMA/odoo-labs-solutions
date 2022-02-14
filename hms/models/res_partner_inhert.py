from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ResPartnerInhert( models.Model ):
    _name = 'res.partner'
    _inherit = 'res.partner'



    # TODO make relation between patient and customer one2one
    related_patient_id = fields.Many2one( comodel_name='hms.patient',
            string='related patient ID')   

    def unlink(self):
        if not self.related_patient_id: 
                raise UserError('customer is linked to a patient!')     
        return super().unlink()


    # TODO constraint on email 
    @api.constrains('email')
    def _check_email_not_in_hms_patient(self):
            for customer in self: 
                    for patient in self.env['hms.patient'].search([]):
                            if customer.email == patient.email: 
                                    raise UserError('invalid email. used by a patient')


                    



 
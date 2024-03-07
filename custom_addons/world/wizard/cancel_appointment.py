from odoo import models,fields,api


class CancelAppointment(models.TransientModel):
    _name = "cancel.appointment"

    appointment_id = fields.Many2one('hello.appointment',string="Appointment Id")
    reason = fields.Text(string="Reason")

    def action_cancel(self):
        print("anil")
        print(self.appointment_id.state)
        updated_records = self.appointment_id.write({'state': 'cancel'})
        print(self.appointment_id.state)
        print(f"Number of records updated: {updated_records}")

        return {}




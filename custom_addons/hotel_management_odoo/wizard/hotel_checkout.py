from odoo import models, fields, api

class HotelCheckoutWizard(models.TransientModel):
    _name = 'hotel.checkout'
    _description = 'Hotel Checkout Wizard'

    _inherit = 'room.checkout'

    reservation_number = fields.Char(string='Reservation Number')
    reservation_id = fields.Many2one('room.reservation', string='Reservation')


    def confirm_checkout(self):
        # Assuming reservation_number is a Char field
        print(self.reservation_number)
        self.reservation_number = self.reservation_id.name
        print("anil")
        if self.reservation_id and self.reservation_id.invoice_id:
            invoice = self.reservation_id.invoice_id
            print('anil')

            if invoice.payment_state == 'paid':
                # If the invoice is already paid, change the state to 'done'
                room_checkout = self.env['room.checkout'].search([('reservation_id', '=', self.reservation_id.id)])
                if room_checkout:
                    room_checkout.write({'state': 'done', 'amount_paid': invoice.amount_total})

                self.reservation_id.write({'state': 'done'})
                print('anil')

    def pay_checkout(self):
        self.reservation_number = self.reservation_id.name
        print("anil")
        if self.reservation_id and self.reservation_id.invoice_id:
            invoice = self.reservation_id.invoice_id
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'view_mode': 'form',
                'view_id': False,
                'target': 'current',
            }

    # def action_checkout(self):
    #     if self.reservation_id and self.reservation_id.invoice_id:
    #         invoice = self.reservation_id.invoice_id
    #
    #         if invoice.payment_state == 'paid':
    #             # If the invoice is already paid, show a message
    #             message = _('The payment for this reservation is already done.')
    #             return self.display_message(message)
    #
    #         else:
    #             print('anil')
    #             # If the invoice is not paid, show a message and open the invoice in the form view
    #             message = _('Payment is due. Please pay the amount.')
    #             return {
    #                 'type': 'ir.actions.act_window',
    #                 'res_model': 'account.move',
    #                 'res_id': invoice.id,
    #                 'view_mode': 'form',
    #                 'view_id': False,  # Update with the correct view id
    #                 'target': 'current',
    #             }
    #     else:
    #         raise UserError(_('No invoice found for the reservation.'))
    #
    # def display_message(self, message, view_mode=None, res_model=None, res_id=None):
    #     return {
    #         'name': _('Checkout Confirmation'),
    #         'type': 'ir.actions.act_window',
    #         'view_mode': view_mode or 'form',
    #         'res_model': 'hotel.checkout',
    #         'target': 'new',
    #         'view_id': self.env.ref('hotel_management_odoo.view_check_out_form').id,  # Update with the correct view id
    #         'context': {'default_message': message, 'default_reservation_number': self.reservation_number},
    #     }

# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class RoomCheckin(models.Model):
    _name = "room.checkin"
    _description = 'Room Checkin'

    name = fields.Char(string='Check-In Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    rm_ids = fields.Many2many('room.reservation.line',
                              domain="[('reservation_id','=',reservation_id)]",
                              string="Room No",
                              required=True)
    reservation_id = fields.Many2one('room.reservation', string='Reservation ', required=True,
                                     domain="[('state','=','confirm')]")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             default='draft')

    @api.onchange('reservation_id')
    def _rm_ids(self):
        res_line = []
        if self.reservation_id.reservation_line_ids:
            for line in self.reservation_id.reservation_line_ids:
                if line.room_id.status == 'book':
                    res_line.append(line.id)
        return {'domain': {'rm_ids': [('id', 'in', res_line)]}}

    def action_checkin(self):
        for rec in self.rm_ids: rec.room_id.write({'status': 'occupied'})
        state = self.reservation_id.reservation_line_ids.mapped('room_id')
        rs_flag = True
        for rec in state:
            if rec.status == 'occupied':
                rs_flag = True
            else:
                rs_flag = False
                break
        if rs_flag:
            self.reservation_id.write({'state': 'occupied'})
        self.state = 'done'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'room.checkin') or _('New')
        return super(RoomCheckin, self).create(vals)


class RoomCheckout(models.Model):
    _name = "room.checkout"
    _description = 'Room Checkout'

    name = fields.Char(string='Check-Out Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    rm_ids = fields.Many2many('room.reservation.line', domain="[('reservation_id','=',reservation_id)]",
                              string="Room No",
                              )
    reservation_id = fields.Many2one('room.reservation', string='Reservation', domain="[('state','=','occupied')]",
                                     required=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             default='draft')

    amount_paid = fields.Float(string='Amount Paid', digits='Account', readonly=True)

    default_message = fields.Char(string='message')


    @api.onchange('reservation_id')
    def _rm_ids(self):
        res_line = []
        if self.reservation_id.reservation_line_ids:
            for line in self.reservation_id.reservation_line_ids:
                if line.room_id.status == 'occupied':
                    res_line.append(line.id)
        return {'domain': {'rm_ids': [('id', 'in', res_line)]}}

    def action_checkout(self):
        if self.reservation_id and self.reservation_id.invoice_id:
            invoice = self.reservation_id.invoice_id
            self.reservation_id.write({'state':'process'})

            if invoice.payment_state == 'paid':
                # If the invoice is already paid, show a message
                message = _('The payment for this reservation is already done.')
                return self.display_message(message)

            else:

                return {
                    'name': _('Checkout Confirmation'),
                    'type': 'ir.actions.act_window',
                    'view_mode':  'form',
                    'res_model': 'hotel.checkout',
                    'target': 'new',
                    'view_id': self.env.ref('hotel_management_odoo.view_pay_check_out_form').id,
                    # Update with the correct view id
                    'context': { 'default_reservation_number': self.reservation_id.name,
                                'default_reservation_id': self.reservation_id.id}

                }

                print('anil')
                # If the invoice is not paid, show a message and open the invoice in the form view

                # return {
                #     'type': 'ir.actions.act_window',
                #     'res_model': 'account.move',
                #     'res_id': invoice.id,
                #     'view_mode': 'form',
                #     'view_id': False,
                #     'target': 'current',
                #    }

        else:
            raise UserError(_('No invoice found for the reservation.'))

    def display_message(self, message, view_mode=None, res_model=None, res_id=None):
        return {
            'name': _('Checkout Confirmation'),
            'type': 'ir.actions.act_window',
            'view_mode': view_mode or 'form',
            'res_model': 'hotel.checkout',
            'target': 'new',
            'view_id': self.env.ref('hotel_management_odoo.view_check_out_form').id,  # Update with the correct view id
            'context': {'default_message': message,'default_reservation_number':self.reservation_id.name,'default_reservation_id':self.reservation_id.id},
        }

    # def confirm_checkout(self):
    #     print("anil")
    #     if self.reservation_id and self.reservation_id.invoice_id:
    #         invoice = self.reservation_id.invoice_id
    #         print('anil')
    #
    #     if invoice.payment_state == 'paid':
    #         # If the invoice is already paid, change the state to 'done'
    #         self.write({'state': 'done', 'amount_paid': invoice.amount_total})
    #         self.reservation_id.write({'state': 'done'})
    #         print('anil')

    # def action_checkout(self):
    #
    #     # reservation_id_state = self.env['room.reservation'].search([('id', '=', self.reservation_id)]).write({'state': 'done'})
    #
    #     if self.reservation_id and self.reservation_id.invoice_id:
    #         invoice = self.reservation_id.invoice_id
    #
    #         if invoice.payment_state == 'paid':
    #             # If the invoice is already paid, change the state to 'done'
    #             self.write({'state': 'done', 'amount_paid': invoice.amount_total})
    #             self.reservation_id.write({'state': 'done'})
    #
    #         else:
    #             # If the invoice is not paid, open the invoice in the form view
    #             self.reservation_id.write({'state': 'process'})
    #             return {
    #                 'type': 'ir.actions.act_window',
    #                 'res_model': 'account.move',
    #                 'res_id': invoice.id,
    #                 'view_mode': 'form',
    #                 'view_id': False,
    #                 'target': 'current',
    #             }
    #     else:
    #         return {}

    # def action_checkout(self):
    #
    #     invoices = self.env['account.move'].search([('id', '=', self.reservation_id.id)])
    #     print(invoices.id)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'account.move',
    #         'res_id': invoices.id,
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('account.view_move_form').id,
    #         'target': 'current',
    #     }




    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'room.checkout') or _('New')

        return super(RoomCheckout, self).create(vals)

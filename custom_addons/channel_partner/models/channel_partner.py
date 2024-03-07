from odoo import models, fields,api,_
from odoo.exceptions import ValidationError




class ChannelPartner(models.Model):
    _name = 'channel.partner'




    # channel partner details
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', )
    email = fields.Char(string='Email', required=True)
    pan = fields.Char(string='PAN',)
    mobile_number = fields.Char(string='Mobile Number',  )
    landline_number = fields.Char(string='Landline Number')

    # Address and Region Information
    communication_address = fields.Text(string='Communication Address', )
    professional_relationship_details = fields.Text(string='Proffesional Details')
    region_of_operation = fields.Char(string='Region of Operation in India')


    # Company Information
    company_name = fields.Char(string='Name of the Company')
    pan_card_number = fields.Char(string='PAN Card No.')
    website_url = fields.Char(string='Website Address (URL)')
    registered_address = fields.Text(string='Registered Address')

    rera_registration = fields.Char(string='RERA Registration No', )
    scanned_cheque_file = fields.Binary(string='Cheque', attachment=True, )
    gst_number = fields.Char(string='GST No',)
    pan_scan_file = fields.Binary(string='PAN Scan File', attachment=True)

    c_partner_id = fields.Char(string='C Partner ID', readonly=True)
    file_name = fields.Char('File Name')

    _rec_name = 'c_partner_id'
    no_of_leads = fields.Integer(string='Leads',compute="_get_no_of_leads_channel_partner")

    @api.model
    def _get_no_of_leads_channel_partner(self):
        self.no_of_leads = self.env['crm.lead'].search_count([('channel_partner_id','=',self.c_partner_id)])
        print(self.no_of_leads)






    @api.model
    def create(self, vals):
        # Generate C Partner ID and assign it to the record being created
        vals['c_partner_id'] = self._generate_c_partner_id(vals.get('pan', ''))
        return super(ChannelPartner, self).create(vals)



    def _generate_c_partner_id(self, pan):
        # Helper function to generate C Partner ID
        if pan and len(pan) >= 4:
            last_four_digits = pan[-4:]
            current_year_last_two_digits = str(fields.Date.today().year)[-2:]
            c_partner_id = f"UBCP{current_year_last_two_digits}{last_four_digits}".upper()

            # Check for existing records with the same last four digits
            existing_records = self.search([('pan', 'like', f'%{last_four_digits}')])
            if existing_records:
                raise ValidationError(_('User already exists with similar PAN.'))

            return c_partner_id
        else:
            raise ValidationError(_('PAN is required to generate a C Partner ID.'))




    # Checkboxes
    credai = fields.Boolean(string='CREDAI')
    rera = fields.Boolean(string='RERA')

    other = fields.Boolean(string='OTHER')

    @api.onchange('pan')
    def _onchange_pan(self):
        if self.pan:
            self.pan = self.pan.upper()

    def get_leads(self):
        action = self.env.ref("crm.crm_case_tree_view_leads").read()[0]
        action.update({
            'name': 'Leads',
            'res_model': 'crm.lead',
            'view_mode': 'tree',
            'domain': [('channel_partner_id', '=', self.c_partner_id)],
            'context': {
                'default_channel_partner_id': self.c_partner_id,
            },
        })
        return action


from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ChannelCrmAdd(models.Model):
    _inherit = 'crm.lead'

    channel_partner_id = fields.Char(string='Channel Partner')
    serial_no = fields.Integer(string='S.No', readonly=True, copy=False)

    _sql_constraints = [
        ('unique_serial_no', 'unique(serial_no)', 'Serial Number must be unique.'),
    ]

    @api.model
    def create(self, values):
        record = super(ChannelCrmAdd, self).create(values)
        record.update_serial_numbers()
        return record

    def unlink(self):
        for record in self:
            serial_no = record.serial_no
            super(ChannelCrmAdd, record).unlink()
            self._update_serial_numbers_after_delete(serial_no)

    @api.model
    def _update_serial_numbers_after_delete(self, deleted_serial_no):
        records_to_update = self.search([('serial_no', '>', deleted_serial_no)])
        for record in records_to_update:
            record.serial_no -= 1

    @api.model
    def update_serial_numbers(self):
        records = self.search([], order='create_date asc')
        for index, record in enumerate(records, start=1):
            record.serial_no = index

    @api.model
    def cron_update_serial_numbers(self):
        self.update_serial_numbers()


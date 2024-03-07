from odoo import http
from odoo.http import request
import base64

class ChannelPartner(http.Controller):

    @http.route('/channelpartner_form/',auth="public")
    def index(self,**kwargs):
        return http.request.render('channel_partner.channel_partner_template')

    @http.route('/submit_form/', type='http', auth="public", methods=['POST'], website=True)
    def submit_form(self, **post):
        # List of field names in the channel.partner model
        field_names = [
            'first_name', 'last_name', 'email', 'pan', 'mobile_number', 'landline_number',
            'communication_address', 'professional_relationship_details', 'region_of_operation',
            'company_name', 'pan_card_number', 'website_url', 'registered_address',
            'rera_registration', 'scanned_cheque_file', 'gst_number', 'pan_scan_file'
        ]

        # Get field values from the post dictionary
        form_values = {field: post.get(field) for field in field_names}

        existing_partner = request.env['channel.partner'].sudo().search([('pan', '=', form_values['pan'])])
        if existing_partner:
            return http.request.render('channel_partner.pan_error_template')

        # Handle file uploads for scanned_cheque_file
        scanned_cheque_file = request.httprequest.files.get('scanned_cheque_file')
        if scanned_cheque_file:
            form_values['scanned_cheque_file'] = base64.b64encode(scanned_cheque_file.read())

        # Handle file uploads for pan_scan_file
        pan_scan_file = request.httprequest.files.get('pan_scan_file')
        if pan_scan_file:
            form_values['pan_scan_file'] = base64.b64encode(pan_scan_file.read())

        # Create or update records in the channel.partner model
        channel_partner_model = request.env['channel.partner']
        new_partner = channel_partner_model.create(form_values)

        # For example, you can redirect to a thank you page
        return request.redirect('/thank_you_page/')

    @http.route('/thank_you_page/', auth="public")
    def thank_you_page(self, **kwargs):
        return http.request.render('channel_partner.thank_you_template')


    @http.route('/lead_form/',auth='public')
    def lead_form(self,**kwargs):
        return http.request.render('channel_partner.channel_partner_lead_template')

    @http.route('/submit_lead_form', type='http', auth='public', website=True)
    def submit_lead_form(self, **post):




        # Extract values from the submitted form
        project_name = post.get('project_name')
        customer_name = post.get('customer_name')
        customer_email = post.get('customer_email')
        customer_phone = post.get('customer_phone')


        channel_partner_id = post.get('channel_partner_id')
        message = post.get('message')

        existing_lead = request.env['crm.lead'].sudo().search([('phone', '=', customer_phone)])
        if existing_lead:
            return http.request.render('channel_partner.lead_error_template')

        channel_partner = request.env['channel.partner'].sudo().search([('c_partner_id', '=', channel_partner_id.upper())])
        if not channel_partner:
            return http.request.render('channel_partner.incorrect_channel_partner_id')

        # Create a lead in crm.lead
        lead_values = {
            'name': project_name,  # You can adjust the fields based on your requirements
            'contact_name': customer_name,
            'email_from': customer_email,
            'phone': customer_phone,
            'channel_partner_id':channel_partner_id.upper(),
            'description': message,
            # Add more fields as needed
        }

        lead = request.env['crm.lead'].sudo().create(lead_values)

        # Redirect or provide a response as needed
        return http.request.render('channel_partner.lead_success_template')



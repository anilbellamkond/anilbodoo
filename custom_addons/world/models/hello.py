from datetime import datetime
from odoo import models, fields ,api
from werkzeug.security import check_password_hash, generate_password_hash

class HelloWorld(models.Model):
    _name = 'hello.world'
    _inherit = ['mail.thread' ,'mail.activity.mixin']
    _description = 'Hello World Model'


    name = fields.Char(string='Name', required=True, )
    age = fields.Integer(string="Age", required=True, default=0)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id, readonly=True)
    gender = fields.Selection([('male','Male'),('female','Female') ],string="Gender")
    is_checked = fields.Boolean(string='Is Checked', default=False)
    document = fields.Binary(string='Document')
    image = fields.Binary(string='Image', attachment=True)
    ref = fields.Char(string='Reference')
    active = fields.Boolean(default=True, readonly='1')
    status = fields.Selection([('pending','Pending'),('updated','Updated')],string='Status',default='pending')
    tag_ids = fields.Many2many("patient.tags",string='Tag')


    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name

    def name_get(self):
        result = []
        for rec in self:
            if not self.env.context.get('code'):
                  name = f"[{rec.id}] {rec.name}"
                  result.append((rec.id, name))
            else:
                 name = rec.name
                 result.append((rec.id, name))
        return result

    def action_done(self):
        self.write({'status': 'updated'})

    def search_data(self):
        record_details = self.env['hello.world'].search([])
        print(record_details)

    def filter_data(self):
        records = self.search([('age', '<', 25)])

        filtered_records = records.filtered(lambda r: r.name == 'archana')

        print(filtered_records)

        reference_id = self.env.ref('world.view_hello_world_form')

        print(reference_id)

    def update_data(self):
        self.write({'age': 30})


    def browse_data(self):
        k=self.env['hello.world'].browse(2)

        print(k)




    def create_data(self):

        new_record = self.env['hello.world'].create({
            'name': "archana",
            'age': 23,
        })

        print(new_record)
        return True

    def delete_data(self):
        self.unlink()

    # @api.model
    # def create(self, values):
    #     # Call the original create method to create the patient record
    #     new_record = super(HelloWorld, self).create(values)
    #
    #     # Automatically create a user for the patient
    #     user_values = {
    #         'name': new_record.name,
    #         'login': new_record.email,
    #         'partner_id': new_record.id,
    #         'email': new_record.email,
    #         'password': new_record.password,
    #         # Add other user-related fields as needed
    #     }
    #
    #     user = self.env['res.users'].create(user_values)
    #
    #     # Link the created user to the patient record
    #     new_record.write({'user_id': user.id})
    #
    #     return new_record
    #
    # def login(self):
    #     user = self.env['res.users'].sudo().search([('login', '=', self.email)])
    #
    #     if user and check_password_hash(user.password, self.password_hash):
    #         # Log in logic, e.g., redirect to a specific view or perform some action
    #         return True
    #     else:
    #         # Handle incorrect login credentials
    #         return False
    #




class appointement(models.Model):
    _name = 'hello.appointment'
    _rec_name = "patient_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('hello.world',string="patient")
    age = fields.Integer(string="Age", required=True, compute="compute_age")
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id, readonly=True)
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender",required=True,related='patient_id.gender' ,)
    booking_date = fields.Datetime(string="Booking Date",default=lambda self: fields.Datetime.now())
    symptoms = fields.Text(string="Symptoms")
    medicine = fields.Text(string="medicine")
    mobile_number = fields.Char(string='Mobile Number')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    address = fields.Text(string="Address",required=True)
    appointment_time = fields.Datetime(string="Appointment Date")
    reference = fields.Char(string="Reference")
    prescription = fields.Html(string='Prescription')
    pharmacy_ids = fields.One2many("hello.pharmacy","appointment_id",string="pharmacy")
    state = fields.Selection(selection=[
       ('draft', 'Draft'),
       ('in consultation', 'In Consultation'),
       ('cancel', 'Cancelled'),
       ('done', 'Done'),
    ], string='Status', required=True, readonly=True,tracking=True, default='draft')







    @api.depends('date_of_birth')
    def compute_age(self):
        today = datetime.now().date()
        for rec in self:
            if rec.date_of_birth:
                dob = rec.date_of_birth
                rec.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            else:
                rec.age = 0


    @api.onchange('patient_id')
    def ref(self):
        for rec in self:
            rec.reference = rec.patient_id.ref



    def action_view_appointments(self):

        return {
            'name': "Appointments",
            'res_model': "hello.appointment",
            'view_mode': 'list,form',
            'context': {},
            'domain': [],
            'target': 'current',
            'type': 'ir.actions.act_window'

        }

    def hi(self):
        pass

    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_view_patient_details(self):
        return {
            'name': "Patient Details",
            'res_model': "hello.world",
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('your_module.view_hello_world_patient_details_form').id,
            'context': {},
            'domain': [],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }

class MedicalStore(models.Model):
    _name = 'medical.store'

    name = fields.Char(string='Medicine Name')
    med_price = fields.Float(string='Price')
    quantity = fields.Integer(string='Quantity')


class PharmacyLines(models.Model):
    _name = 'hello.pharmacy'
    _rec_name = "medicine_id"

    medicine_id = fields.Many2one('medical.store',string='medicine_name')
    medicine_price = fields.Float(string='Price',related='medicine_id.med_price')
    quantity = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hello.appointment',string="appointment")
    total_price = fields.Integer('Total Price')


    @api.onchange('quantity')
    def total_price_one_medicine(self):
        for rec in self:
            rec.total_price = rec.medicine_price * rec.quantity



class PatientStatus(models.Model):
     _name = 'patient.status'

     patient_id = fields.Many2one('hello.world', string="patient")
     progress = fields.Char(string='progress')
     status = fields.Selection([('normal', 'Normal'), ('critical', 'Critical')], string='Status',)
     health_number = fields.Integer(string='Health Number',)

     @api.onchange('health_number')
     class PatientTags(models.Model):
         _name = "patient.tags"

         name = fields.Char(string='Name')
         active = fields.Boolean(string='Active',default=True)
         color = fields.Integer(string='Color')
         color_2 = fields.Char(string="Color2")
     def onchange_health_number(self):
        print('abjdd')
        original_health_number = self._origin.health_number

        print(f"previous Health Number: {original_health_number}")



from odoo import models, fields,api

class StaffModel(models.Model):
    _name = 'staff.module'

    name = fields.Char(string='Staff')
    class_handle = fields.Many2one('class.module',string='Class')
    phone = fields.Integer(string='phone')
    address = fields.Text(string='Address')
    subject_handle = fields.One2many('subjects.module', 'staff_handle', string='Subjects',widget='many2many_tags')
    salary = fields.Integer(string='Salary')
    qualification = fields.Char(string='Qualification')


class ClassModel(models.Model):

    _name = 'class.module'

    name = fields.Char(string='Class')

    fee = fields.Integer(string="Fees")

    class_teacher = fields.Char(string='Class Teacher')


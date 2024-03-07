from odoo import models, fields,api

class SubjectModel(models.Model):
    _name = 'subjects.module'

    name = fields.Char(string='Subjects')
    staff_handle = fields.Many2one('staff.module', string='Staff')
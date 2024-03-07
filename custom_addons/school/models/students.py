from odoo import models, fields,api,_

import logging

_logger = logging.getLogger(__name__)

class StudentModel(models.Model):
    _name = 'student.model'
    _rec_name = 'roll_no'


    roll_no = fields.Char(string='Roll no',required=True,
                          readonly=True, default=lambda self: _('New'))
    name = fields.Char(string='Students')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    father_name = fields.Char(string="Father's name")
    class_name = fields.Many2one('class.module',string='Class')
    class_teacher = fields.Char(related ='class_name.class_teacher' ,store=True)
    student = fields.One2many('exams.module','stu',string='Student')
    photo = fields.Image(string='Photo ID')



    @api.model
    def create(self, vals):
        if vals.get('roll_no', _('New')) == _('New'):
            vals['roll_no'] = self.env['ir.sequence'].next_by_code(
                'student.model') or _('New')
        res = super(StudentModel, self).create(vals)
        return res






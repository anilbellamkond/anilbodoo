from odoo import models, fields,api



class ExamType(models.Model):
    _name = 'exam.type'

    name = fields.Char(string='Examination Name')

class ExamModel(models.Model):
    _name = 'exams.module'

    type = fields.Many2one(comodel_name='exam.type',string='Examination Name')
    stu = fields.Many2one('student.model',string='Student')
    marks = fields.Integer(string='Marks')
    telugu = fields.Integer(string="English")
    hindi = fields.Integer(string="Maths")
    english = fields.Integer(string="Science")
    maths = fields.Integer(string="Social")
    science = fields.Integer(string="Biology")
    social = fields.Integer(string="Chemistry")

    total = fields.Integer(string='Total Marks',compute='cal_total_marks')


    @api.depends('english','maths','science','social','telugu','hindi')
    def cal_total_marks(self):
        for rec in self:
            rec.total = rec.english+rec.maths+rec.science+rec.social+rec.telugu+rec.hindi



    def print_marks(self):
        # Trigger download of the PDF report
        return self.env.ref('school.action_report_exam_mark_sheet').report_action(self)

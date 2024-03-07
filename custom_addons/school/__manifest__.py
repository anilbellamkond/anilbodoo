# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Montessori School',

    'description': """',
    'version': '1.1',
    'author': 'Bellamkonda Anil',
    'sequence': -100,
    'summary': 'School Management System',
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'report/mark_sheet_pdf.xml',
        'views/school_model_view.xml',
        'views/students.xml',
'views/exams.xml',
        'views/staff.xml',
        'views/class.xml',
        'views/subjects.xml',
        'views/exams.xml'
           ],

    'demo': [],
    'installable': True,
    'application':True,
    'auto_install': False,

    'license': 'LGPL-3',
}
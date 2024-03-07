{
    'name': 'Hello World Module',
    'version': '1.0',
    'author': 'anil bellamkonda',
    'category': 'Uncategorized',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/world_rules.xml',
        'views/hellos.xml',
        'wizard/cancel_appointment.xml',
        'views/welcome.xml',
        'views/appointment.xml',
        'views/patient.xml',

        'views/patient_tag.xml',

    ],
    'sequence':'-100',
    'installable': True,
    'auto_install': False,
     'license': 'LGPL-3',
    'application':True,
}

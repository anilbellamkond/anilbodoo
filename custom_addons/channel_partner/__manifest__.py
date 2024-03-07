{
    'name': 'Channel Partner',
    'version': '1.0',
    'author': 'Anil Bellamkonda',
    'category': 'Uncategorized',
    'depends': ['base','crm'],
    'data': [
        "security/ir.model.access.csv",

       "views/channel_partner.xml",
        "views/customer_form.xml",
        "views/lead_form.xml",
        "views/crm_add_channel_part_field.xml"

    ],
'assets': {
        'web.assets_backend': [

        ],
    },
    'sequence':'-100',
    'installable': True,
    'auto_install': False,
     'license': 'LGPL-3',
    'application':True,
}

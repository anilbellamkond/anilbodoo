
from odoo import models,fields

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    computer_generation = fields.Char(string='computer Generation')
    detailed_type = fields.Selection(
        selection_add=[('others','Others')],
        ondelete= {'others':'cascade'})

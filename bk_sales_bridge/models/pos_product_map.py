# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class BkPosProductMap(models.Model):
    _name = 'bk.pos.product.map'
    _description = 'External POS Product Mapping'
    _rec_name = 'external_name'

    pos_source_id = fields.Many2one('bk.pos.source', string='POS Source', required=True)
    external_code = fields.Char(string='External Code', required=True,
                                help='POS product code')
    external_name = fields.Char(string='External Product Name',
                                help='POS product name (for reference)')
    product_id = fields.Many2one('product.product', string='Odoo Product',
                                 help='Corresponding product in Odoo')
    active = fields.Boolean(default=True)
    notes = fields.Char(string='Notes',   help='Internal notes about this mapping')

    _sql_constraints = [
        ('uniq_source_code', 'unique(pos_source_id, external_code)',
         'This external code is already mapped for this POS source.'),
    ]


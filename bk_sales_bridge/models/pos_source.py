# -*- coding: utf-8 -*-
import json
import logging
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import requests

_logger = logging.getLogger(__name__)

class BkPosSource(models.Model):
    _name = 'bk.pos.source'
    _description = 'POS Source / Outlet Configuration'
    _rec_name = 'name'

    name = fields.Char(string='Outlet Name/Device', required=True, help='e.g., Main Restaurant, Bar Counter, Grab & Go #1')
    business_line = fields.Selection([('bole_shop_1', 'Bole Shop 1'),
                                      ('bole_shop_2', 'bole_shop_2'),
                                      ('skylight', 'Skylight Shop')], string='Business Line', required=True)
    default_customer_id = fields.Many2one('res.partner', string="Default Customer", required=True)
    low_margin_threshold_pct = fields.Float(string='Low Margin Alert Threshold (%)',
        default=30.0, help='Items below this % margin will be flagged as "low_margin" in reports')
    pricelist_id = fields.Many2one('product.pricelist', string="Pricelist", required=True )
    currency_id = fields.Many2one(related="pricelist_id.currency_id", string='Currency')



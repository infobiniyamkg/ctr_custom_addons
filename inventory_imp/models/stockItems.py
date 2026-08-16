from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    customs_id = fields.Char(string="Customs ID")


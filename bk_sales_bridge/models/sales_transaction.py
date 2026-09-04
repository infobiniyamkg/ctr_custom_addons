# -*- coding: utf-8 -*-

from odoo import api, fields, models

class BkSalesTransaction(models.Model):
    _name = 'bk.sales.transaction'
    _description = 'POS Sales Transaction'
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', compute='_compute_name', store=True, )
    batch_id = fields.Many2one('bk.sales.order',  string='Import Batch', ondelete='cascade', index=True)
    pos_source_id = fields.Many2one('bk.pos.source', store=True, index=True, string='POS Source',)

    external_ref = fields.Char(string='POS Transaction Ref', required=True, index=True,
                               help='Transaction reference/code returned by the POS.',)
    device_name = fields.Char( string='Device',index=True)
    fs_number = fields.Char(string='FS#',index=True)
    shift_number = fields.Char(string='Shift',index=True)
    issued_datetime = fields.Datetime(string='POS Issued Date')
    user_name = fields.Char(string='User', )
    customer_name = fields.Char(string='Customer')

    date = fields.Date(string='Date', required=True, index=True)

    subtotal = fields.Float(string='Subtotal')
    grand_total = fields.Float(string='Grand Total')

    tax_total = fields.Float(string='Tax Total',)
    line_ids = fields.One2many('bk.sales.order.line', 'transaction_id', string='Sales Lines',)
    line_count = fields.Integer(string='Line Count',compute='_compute_line_count', store=True,)
    imported = fields.Boolean(string='Imported', default=True,index=True,)

    currency_code = fields.Char(string="Currency Code")
    base_currency_rate = fields.Float(string="Base Currency Rate")
    sales_type = fields.Selection([('sales', 'Sales'),
                                   ('return','Return'),
                                   ('void', 'Void')],string='Sales Type',default='sales')


    @api.depends('external_ref', 'device_name')
    def _compute_name(self):
        for transaction in self:
            if transaction.device_name:
                transaction.name = '%s / %s' % (
                    transaction.external_ref or '',
                    transaction.device_name,
                )
            else:
                transaction.name = transaction.external_ref or 'New'

    @api.depends('line_ids')
    def _compute_line_count(self):
        for transaction in self:
            transaction.line_count = len(transaction.line_ids)

    _sql_constraints = [
        (
            'uniq_pos_transaction',
            'unique(pos_source_id, external_ref)',
            'This POS transaction has already been imported for this POS source.'
        ),
    ]
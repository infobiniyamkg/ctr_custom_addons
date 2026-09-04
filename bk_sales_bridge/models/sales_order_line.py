# -*- coding: utf-8 -*-

from odoo import api, fields, models

class BkSalesOrderLine(models.Model):
    _name = 'bk.sales.order.line'
    _description = 'BK Sales Line (Staged POS Sale)'
    _order = 'date desc, id desc'

    transaction_id = fields.Many2one('bk.sales.transaction', string="Sales Transaction",
                                     required=True, ondelete='cascade')
    order_id = fields.Many2one('bk.sales.order', ondelete='restrict', readonly=True)
    pos_source_id = fields.Many2one(related='transaction_id.pos_source_id', store=True, index=True,
                                    string='POS Source', )

    external_code = fields.Char(string='External Code',index=True, required=True)
    external_name = fields.Char(string='External Product Name')

    device_name = fields.Char(related='transaction_id.device_name', store=True, string='Device Name')
    shift_number = fields.Char(related='transaction_id.shift_number', store=True, string='Shift',)
    fs_number = fields.Char(related='transaction_id.fs_number', store=True, string='FS#',)
    date = fields.Date(related='transaction_id.date', string='Sale Date', store=True, index=True)
    customer_name = fields.Char(related='transaction_id.customer_name', store=True,   string='Customer',)

    # Resolved Odoo product
    product_id = fields.Many2one('product.product', string='Product')
    sold_qty = fields.Float(string='Qty', required=True, default=1.0)
    unit_price = fields.Monetary(string='Price', required=True)

    currency_code = fields.Char(related='transaction_id.currency_code', string="Currency")
    base_currency_rate = fields.Float(related='transaction_id.base_currency_rate', string="Rate")
    amount_in_currency = fields.Float(string="Price (Base)", compute='_compute_totals', store=True)

    net_sales_value = fields.Monetary(string='Sales Value', currency_field='currency_id', compute='_compute_totals', store=True)
    net_sales_value_in_currency = fields.Monetary(string="Sales Value(Base)", currency_field='currency_company_id', compute='_compute_totals', store=True)

    current_cost = fields.Monetary(string='Unit Cost',currency_field='currency_company_id', compute='_compute_totals', store=True)
    total_cost = fields.Monetary(string='Total Cost', currency_field='currency_company_id', compute='_compute_totals', store=True)

    margin_value = fields.Monetary(string='Margin Value',currency_field='currency_company_id',  compute='_compute_totals', store=True)
    margin_pct = fields.Float(string='Margin %', compute='_compute_totals', store=True)

    flag = fields.Selection([('ok', 'OK'),
                             ('negative_margin', 'Negative Margin'),
                             ('low_margin', 'Below Threshold Margin'),
                             ('product_missing', 'Product Not Found'),
                             ('price_anomaly', 'Price Anomaly')],
                            string='Flag', compute='_compute_totals', store=True,help='Quality flag based on margins and business rules')
    currency_id = fields.Many2one(related='pos_source_id.pricelist_id.currency_id')
    currency_company_id = fields.Many2one(related='order_id.currency_company_id', store=True, )
    # ============================================================
    # SQL CONSTRAINT
    # ============================================================
    # _sql_constraints = [
    #     ('uniq_transaction_line',
    #      'unique(transaction_id, external_line_ref)',
    #      'This POS transaction line has already been imported.' ),
    #     ]


    def _find_product_mapping(self, pos_source, external_code):
        if not pos_source or not external_code:
            return self.env['bk.pos.product.map']

        return self.env['bk.pos.product.map'].search([
            ('pos_source_id', '=', pos_source.id),
            ('external_code', '=', external_code),
            ('active', '=', True),
        ], limit=1)

    def _find_product_by_external_code(self, external_code):
        """Fallback: search product.product directly by external code."""

        if not external_code:
            return self.env['product.product']

        return self.env['product.product'].search(['|',('default_code', '=', external_code),
                                                   ('barcode', '=', external_code)], limit=1)

    def _resolve_product(self):
        """
        Resolve product using:

        1. POS product mapping
        2. product.product external_code

        Returns the resolved product or False.
        """

        self.ensure_one()

        if not self.external_code:
            return False

        # ---------------------------------------------------------
        # 1. Try POS-specific mapping
        # ---------------------------------------------------------
        mapping = self._find_product_mapping(
            self.pos_source_id,
            self.external_code,
        )

        if mapping and mapping.product_id:
            return mapping.product_id

        # ---------------------------------------------------------
        # 2. Fallback to product.product external code
        # ---------------------------------------------------------
        product = self._find_product_by_external_code(
            self.external_code
        )

        if product:
            return product

        return False

    @api.onchange('external_code', 'pos_source_id')
    def _onchange_resolve_product(self):
        for line in self:
            line.product_id = line._resolve_product()

    @api.model_create_multi
    def create(self, vals_list):
        Transaction = self.env['bk.sales.transaction']

        for vals in vals_list:

            # Product already explicitly supplied
            if vals.get('product_id'):
                continue

            transaction_id = vals.get('transaction_id')
            external_code = vals.get('external_code')

            if not transaction_id or not external_code:
                continue

            transaction = Transaction.browse(transaction_id).exists()

            if not transaction:
                continue

            pos_source = transaction.pos_source_id

            if not pos_source:
                continue

            # ---------------------------------------------------------
            # 1. Mapping
            # 2. product.product external_code
            # ---------------------------------------------------------

            mapping = self._find_product_mapping(
                pos_source,
                external_code,
            )

            if mapping and mapping.product_id:
                vals['product_id'] = mapping.product_id.id
                continue

            product = self._find_product_by_external_code(
                external_code
            )

            if product:
                vals['product_id'] = product.id

        return super().create(vals_list)
    def _get_cost(self, product):
        return product.standard_price, False

    def _resolve_cost(self, product):
        if not product:
            return 0.0, 'none'
        return product.standard_price, 'standard'

    def action_refresh_products(self):
        resolved_count = 0
        unresolved_count = 0

        for line in self:
            product = line._resolve_product()
            if product:
                if line.product_id != product:
                    line.product_id = product
                resolved_count += 1
            else:
                line.product_id = False
                unresolved_count += 1

        return {
            'resolved': resolved_count,
            'unresolved': unresolved_count,
        }

    @api.depends(
        'sold_qty',
        'unit_price',
        'product_id',
        'pos_source_id',
        'base_currency_rate',
        'pos_source_id.low_margin_threshold_pct',
    )
    def _compute_totals(self):
        for line in self:
            net_value = line.unit_price * line.sold_qty
            line.net_sales_value = net_value
            line.net_sales_value_in_currency = net_value * line.base_currency_rate
            line.amount_in_currency = line.unit_price * line.base_currency_rate

            if not line.product_id:
                line.current_cost = 0.0
                line.total_cost = 0.0
                line.margin_value = 0.0
                line.margin_pct = 0.0
                line.flag = 'product_missing'
                continue

            cost = line.product_id.standard_price

            line.current_cost = cost
            line.total_cost = cost * line.sold_qty
            # line.margin_value = (line.net_sales_value - line.total_cost )
            line.margin_value = (line.net_sales_value_in_currency - line.total_cost )
            line.margin_pct = ( line.margin_value / line.net_sales_value_in_currency * 100.0 if line.net_sales_value_in_currency  else 0.0 )

            if line.unit_price <= 0:
                line.flag = 'price_anomaly'
            elif line.margin_value < 0:
                line.flag = 'negative_margin'
            elif line.margin_pct < (line.pos_source_id.low_margin_threshold_pct or 50.0):
                line.flag = 'low_margin'
            else:
                line.flag = 'ok'
from odoo import fields, models,api, _
from odoo.exceptions import UserError, ValidationError

class BkSalesOrder(models.Model):
    _name = 'bk.sales.order'
    _description = 'BK Sales Batch (POS Import Summary)'
    _order = 'end_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False,  default='New',)
    pos_source_id = fields.Many2one('bk.pos.source', string='POS Source / Outlet', required=True, index=True,)
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.context_today,)
    end_date = fields.Date(string='End Date', required=True, default=fields.Date.context_today,)
    pricelist_id = fields.Many2one(related='pos_source_id.pricelist_id', string='Price List',)
    currency_id = fields.Many2one(related='pricelist_id.currency_id', string='Currency')
    currency_company_id = fields.Many2one("res.currency", string='Currency', default=lambda self: self.env.user.company_id.currency_id)
    line_ids = fields.One2many('bk.sales.order.summary.line','order_id', string='Summary Lines',)

    total_sales = fields.Monetary(string='Total Sales', currency_field='currency_id', compute='_compute_summary', store=True,)
    total_sales_base = fields.Monetary(string='Total Sales (Base)', currency_field='currency_company_id', compute='_compute_summary', store=True,)
    exchange_avg_rate = fields.Float(string="Ex.Rate",  compute='_compute_summary', store=True,)
    total_cost = fields.Monetary(string='Total Cost', currency_field='currency_company_id', compute='_compute_summary', store=True,)

    total_margin_value = fields.Monetary(string='Total Margin', currency_field='currency_company_id', compute='_compute_summary', store=True,)
    margin_pct = fields.Float(string='Overall Margin %',compute='_compute_summary', store=True,)
    grand_total = fields.Monetary(string='Grand Total', currency_field='currency_id', compute='_compute_summary',store=True,)
    total_quantity = fields.Float(string='Total Quantity', compute='_compute_summary',store=True,)    #

    flagged_line_count = fields.Integer(string='Flagged Lines', compute='_compute_summary', store=True,)
    source_line_count = fields.Integer(string='Source Lines', compute='_compute_summary', store=True, )
    transaction_count = fields.Integer(string='Transactions', compute='_compute_summary', store=True,)

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('review', 'Pending Review'),
            ('validated', 'Validated'),
            ('posted', 'Posted'),
            ('error', 'Error'),
        ],
        string='Status', default='draft', required=True, copy=False, index=True)

    sale_order_id = fields.Many2one('sale.order', string='Odoo Sales Order', copy=False, readonly=True, index=True,)

    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS
    # -------------------------------------------------------------------------

    _sql_constraints = [
        (
            'unique_pos_date_range',
            'unique(pos_source_id, start_date, end_date)',
            'A sales batch already exists for this POS and date range.',
        ),
    ]

    # =========================================================================
    # CREATE
    # =========================================================================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('bk.sales.order') or 'New'

            # If POS source has a currency, use it.
            if vals.get('pos_source_id'):
                pos_source = self.env['bk.pos.source'].browse(vals['pos_source_id'])

                if pos_source.currency_id:
                    vals['currency_id'] = pos_source.currency_id.id

        return super().create(vals_list)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError(
                    _('Start Date cannot be after End Date.')
                )

    # =========================================================================
    # COMPUTE SUMMARY
    # =========================================================================

    @api.depends(
        'line_ids.sales_value',
        'line_ids.cost_value',
        'line_ids.margin_value',
        'line_ids.quantity',
        'line_ids.source_line_count',
        'line_ids.transaction_count',
    )
    def _compute_summary(self):

        for order in self:
            lines = order.line_ids
            order.total_sales = sum(lines.mapped('sales_value'))
            order.total_sales_base = sum(lines.mapped('sales_value_in_currency'))
            order.total_cost = sum(lines.mapped('cost_value') )
            order.total_margin_value = sum( lines.mapped('margin_value') )
            order.grand_total = order.total_sales
            order.total_quantity = sum(lines.mapped('quantity') )
            order.margin_pct = (order.total_margin_value / order.total_sales_base * 100  if order.total_sales_base else 0.0)
            order.exchange_avg_rate = (order.total_sales_base / order.total_sales if order.total_sales else 0.0)

            sales_line = self.env['bk.sales.order.line'].search([('order_id', '=', order.id)])
            order.flagged_line_count = len(sales_line.filtered(lambda line: line.flag not in (False, 'ok')))

            order.source_line_count = sum(lines.mapped('source_line_count'))
            order.transaction_count = sum(lines.mapped('transaction_count'))

    # =========================================================================
    # ACTION: GENERATE SUMMARY
    # =========================================================================

    def action_generate_summary(self):
        for order in self:
            if order.state not in ('draft', 'review'):
                raise UserError(_('Summary can only be generated while the batch '
                    'is in Draft or Pending Review.' ))

            if order.start_date > order.end_date:
                raise UserError(_('Start Date cannot be after End Date.'))

            # -------------------------------------------------------------
            # Validate POS.
            # -------------------------------------------------------------

            if not order.pos_source_id:
                raise UserError(_('Please select a POS Source / Outlet.'))

            if order.state == 'review' and order.line_ids:
                raise UserError(_(
                    'This batch already has a generated summary. '
                    'Use "Rebuild Summary" if you want to regenerate it.'
                ))

            source_lines = self.env[
                'bk.sales.order.line'
            ].search([
                ('order_id', '=', False),
                ('pos_source_id', '=', order.pos_source_id.id),
                ('date', '>=', order.start_date),
                ('date', '<=', order.end_date),
                ('transaction_id.sales_type', '=', 'sales')
            ])
            print(f"source_lines: {source_lines}")
            print(f"len: {len(source_lines)}")

            if not source_lines:
                raise UserError(_(
                    'No unprocessed sales lines were found for %s '
                    'between %s and %s.'
                ) % (
                    order.pos_source_id.display_name,
                    order.start_date,
                    order.end_date,
                ))

            # -------------------------------------------------------------
            # GROUP BY PRODUCT
            # -------------------------------------------------------------

            grouped = {}

            for line in source_lines:
                transaction = line.transaction_id
                if not transaction:
                    continue

                sales_type = transaction.sales_type
                if sales_type == 'void':
                    continue

                # ---------------------------------------------------------
                # PRODUCT MISSING
                # We don't create a sale summary line because Odoo
                # cannot create a sale.order.line without a product.
                # You can change this behavior later if needed.
                # ---------------------------------------------------------

                if not line.product_id:
                    continue

                product = line.product_id

                # ---------------------------------------------------------
                # Create grouping bucket.
                # ---------------------------------------------------------

                if product.id not in grouped:
                    grouped[product.id] = {
                        'product_id': product.id,
                        'external_code': line.external_code,
                        'product_name': (product.display_name or line.external_name ),
                        'quantity': 0.0,
                        'avg_price': 0.0,
                        'sales_value_in_currency':0.0,
                        'sales_value': 0.0,
                        'cost_value': 0.0,
                        'margin_value': 0.0,

                        'transaction_ids': set(),
                        'source_line_count': 0,

                    }

                data = grouped[product.id]

                # ---------------------------------------------------------
                # SALES = POSITIVE
                # RETURN = NEGATIVE
                # ---------------------------------------------------------

                sign = -1.0 if sales_type == 'return' else 1.0

                data['quantity'] += (line.sold_qty * sign)
                data['sales_value'] += (line.net_sales_value * sign)
                data['sales_value_in_currency'] += (line.net_sales_value_in_currency * sign)
                data['cost_value'] += (line.total_cost * sign)
                data['margin_value'] += (line.margin_value * sign)
                data['transaction_ids'].add(transaction.id)
                data['source_line_count'] += 1

            # -------------------------------------------------------------
            # CREATE SUMMARY LINES
            # -------------------------------------------------------------

            SummaryLine = self.env['bk.sales.order.summary.line']
            summary_values = []

            for data in grouped.values():
                sales_value = data['sales_value']
                quantity = data['quantity']
                sales_value_in_currency = data['sales_value_in_currency']
                cost_value = data['cost_value']
                margin_value = data['margin_value']

                margin_pct = (margin_value / sales_value_in_currency * 100 if sales_value_in_currency  else 0.0 )
                avg_price = (sales_value / quantity  if quantity  else 0.0 )
                summary_values.append({
                    'order_id': order.id,
                    'product_id': data['product_id'],
                    'external_code': data['external_code'],
                    'product_name': data['product_name'],
                    'quantity': data['quantity'],
                    'avg_price':avg_price,
                    'sales_value': sales_value,
                    'sales_value_in_currency': data['sales_value_in_currency'],
                    'cost_value': cost_value,
                    'margin_value': margin_value,
                    'margin_pct': margin_pct,
                    'transaction_count': len(data['transaction_ids']),
                    'source_line_count': data['source_line_count'],
                })
            print(f"summary_values: {summary_values}")
            if summary_values:
                SummaryLine.create(summary_values)

            # -------------------------------------------------------------
            # MARK SOURCE LINES AS CONSUMED
            # THIS IS WHAT PREVENTS DUPLICATION.
            # -------------------------------------------------------------
            source_lines.write({'order_id': order.id,})

            # -------------------------------------------------------------
            # Move batch to Review.
            # -------------------------------------------------------------
            order.write({'state': 'review',})
        #
        return True

    # =========================================================================
    # ACTION: REBUILD SUMMARY
    # =========================================================================

    def action_rebuild_summary(self):
        """
        Rebuild the summary for this batch.
        IMPORTANT:
        This is allowed ONLY before validation.
        We release ONLY source lines belonging to this batch.
        We NEVER touch lines belonging to another batch.
        """

        for order in self:

            if order.state not in ('draft', 'review'):
                raise UserError(_(
                    'Only Draft or Pending Review batches '
                    'can be rebuilt.'
                ))

            # -------------------------------------------------------------
            # Find source lines belonging to THIS batch.
            # -------------------------------------------------------------
            source_lines = self.env['bk.sales.order.line'].search([('order_id', '=', order.id)])
            # -------------------------------------------------------------
            # Release them.
            # -------------------------------------------------------------
            if source_lines:
                source_lines.write({'order_id': False,})
            # -------------------------------------------------------------
            # Delete current summary lines.
            # -------------------------------------------------------------
            order.line_ids.unlink()
            # -------------------------------------------------------------
            # Reset state.
            # -------------------------------------------------------------
            order.write({'state': 'draft',})

            # -------------------------------------------------------------
            # Generate again.
            # -------------------------------------------------------------
            order.action_generate_summary()

        return True

    # =========================================================================
    # ACTION: VALIDATE
    # =========================================================================

    def action_validate(self):

        for order in self:

            if order.state != 'review':
                raise UserError(_(
                    'Only batches in Pending Review can be validated.'
                ))

            if not order.line_ids:
                raise UserError(_(
                    'Cannot validate a batch without summary lines.'
                ))

            # -------------------------------------------------------------
            # Optional quality check.
            # -------------------------------------------------------------

            missing_product_lines = self.env[
                'bk.sales.order.line'
            ].search([
                ('order_id', '=', order.id),
                ('product_id', '=', False),
            ])

            if missing_product_lines:
                raise UserError(_(
                    'This batch contains %s source lines without '
                    'a resolved Odoo product. Please resolve them '
                    'before validation.'
                ) % len(missing_product_lines))

            # -------------------------------------------------------------
            # Validate.
            # -------------------------------------------------------------

            order.write({
                'state': 'validated',
            })

        return True

    # =========================================================================
    # ACTION: RESET TO REVIEW
    # =========================================================================

    def action_reset_to_review(self):

        for order in self:

            # if order.state != 'validated':
            #     raise UserError(_(
            #         'Only validated batches can be reset.'
            #     ))

            if order.sale_order_id:
                raise UserError(_(
                    'This batch already has an Odoo Sales Order and '
                    'cannot be reset.'
                ))

            order.write({
                'state': 'draft',#'review',
            })

        return True

    # =========================================================================
    # ACTION: POST TO SALE ORDER
    # =========================================================================

    def action_post_to_sale(self):
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']

        for order in self:
            if order.state != 'validated':
                raise UserError(_('Only validated batches can be posted to Sales.'))
            # -------------------------------------------------------------
            # Prevent duplicate sale orders.
            # -------------------------------------------------------------
            if order.sale_order_id:
                raise UserError(_('This batch has already been posted to Sales Order %s.') % order.sale_order_id.display_name)

            if not order.line_ids:
                raise UserError(_('Cannot post a batch without summary lines.'))

            # -------------------------------------------------------------
            # Create sale.order
            # -------------------------------------------------------------
            sale_order = SaleOrder.create({
                'partner_id': order.pos_source_id.default_customer_id.id,
                'company_id': self.env.user.company_id.id,
                'pricelist_id': order.pricelist_id.id,
                'origin': order.name,
            })

            # -------------------------------------------------------------
            # Create sale.order.line
            # -------------------------------------------------------------

            for line in order.line_ids:

                if not line.product_id:
                    raise UserError(_(
                        'Product is missing on summary line %s.'
                    ) % line.product_name)

                if not line.quantity:
                    continue

                # ---------------------------------------------------------
                # Price per unit.
                # Since summary line contains the final aggregated
                # sales value, calculate the effective unit price.
                # ---------------------------------------------------------

                price_unit = (line.sales_value / line.quantity
                    if line.quantity
                    else 0.0
                )

                SaleOrderLine.create({
                    'order_id': sale_order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': price_unit,
                    'name': line.product_name,
                })

            # -------------------------------------------------------------
            # Link batch to sale order.
            # -------------------------------------------------------------

            order.write({
                'sale_order_id': sale_order.id,
                'state': 'posted',
            })

        return True

    def action_refresh_products(self):
        """
        Refresh product assignments on source POS lines belonging
        to this sales batch.

        Resolution order:
            1. bk.pos.product.map
            2. product.product.external_code

        After refreshing products, rebuild the summary so that
        previously skipped product-missing lines can be included.
        """

        for order in self:

            if order.state not in ('draft', 'review'):
                raise UserError(_(
                    'Products can only be refreshed while the batch '
                    'is in Draft or Pending Review.'
                ))
            # ---------------------------------------------------------
            # Get source lines belonging to this batch
            # ---------------------------------------------------------
            source_lines = self.env['bk.sales.order.line'].search([('order_id', '=', order.id),])

            if not source_lines:
                raise UserError(_('No source sales lines are associated with this batch.'))

            # ---------------------------------------------------------
            # Refresh products
            # ---------------------------------------------------------

            result = source_lines.action_refresh_products()

            resolved = result['resolved']
            unresolved = result['unresolved']

            # ---------------------------------------------------------
            # Rebuild summary
            # This is important because lines that previously had no
            # product were skipped by action_generate_summary().
            # ---------------------------------------------------------

            order.action_rebuild_summary()
            # order.action_generate_summary()

            message = _('%s product(s) resolved successfully. '
                        '%s line(s) are still unresolved.'
                                ) % (resolved, unresolved)

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Product Refresh'),
                    'message': message,
                    'type': 'success' if unresolved == 0 else 'warning',
                    'sticky': False,
                },
            }

        return True


class BkSalesOrderSummaryLine(models.Model):
    _name = 'bk.sales.order.summary.line'
    _description = 'BK Sales Aggregated Product Line'
    _order = 'product_id, id'

    order_id = fields.Many2one('bk.sales.order', required=True, ondelete='cascade',index=True,)
    pos_source_id = fields.Many2one(related='order_id.pos_source_id',string="Pos Source", store=True)
    product_id = fields.Many2one('product.product',required=True, index=True,)
    external_code = fields.Char(string='External Code',)
    product_name = fields.Char(string='Product Name')
    quantity = fields.Float(string='Quantity', digits='Product Unit of Measure',)
    avg_price = fields.Monetary(string='Avg. Price', digits='Product Unit of Measure',currency_field='currency_id',)
    sales_value = fields.Monetary(string='Sales Value', currency_field='currency_id',)
    sales_value_in_currency = fields.Monetary(string='Sales Value(Base)', currency_field='currency_company_id',)
    cost_value = fields.Monetary(string='Cost', currency_field='currency_company_id',)
    margin_value = fields.Monetary(string='Margin',currency_field='currency_company_id',)
    margin_pct = fields.Float(string='Margin %',)
    transaction_count = fields.Integer(string='Transactions',)

    source_line_count = fields.Integer(string='Source Lines',)
    currency_id = fields.Many2one(related='order_id.currency_id', store=True,)
    currency_company_id = fields.Many2one(related='order_id.currency_company_id', store=True,)

    _sql_constraints = [
        (
            'unique_product_per_order',
            'unique(order_id, product_id)',
            'A product can only appear once in a sales batch.',
        ),
    ]

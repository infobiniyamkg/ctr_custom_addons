# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from odoo import http, fields
from odoo.http import request


class BkDashboardController(http.Controller):
    """BK Sales Bridge Dashboard Controller - Odoo 17"""

    @http.route('/bk_sales_bridge/dashboard', type='json', auth='user')
    def get_dashboard_data(self, start_date=None, end_date=None, pos_source_id=None,
                           product_category=None):
        """Get aggregated dashboard data"""

        # Parse dates
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        # Get domain
        domain = [
            ('order_id.start_date', '>=', start_date),
            ('order_id.end_date', '<=', end_date),
        ]

        if pos_source_id:
            try:
                domain.append(('pos_source_id', '=', int(pos_source_id)))
            except:
                pass

        if product_category:
            try:
                domain.append(('product_id.categ_id', '=', int(product_category)))
            except:
                pass

        # Fetch lines
        # lines = request.env['bk.sales.order.line'].search(domain)
        lines = request.env['bk.sales.order.summary.line'].search(domain)

        # Calculate KPIs
        kpis = self._calculate_kpis(lines)

        # Get charts data
        charts = {
            # 'sales_trend': self._get_sales_trend(lines, start_date, end_date),
            'margin_by_outlet': self._get_margin_by_outlet(lines),
            # 'flag_distribution': self._get_flag_distribution(lines),
            'category_performance': self._get_category_performance(lines),
            'profit_loss': self._get_profit_loss_analysis(lines),
            'low_margin_items': self._get_low_margin_items(lines),
        }

        # Get data tables
        tables = {
            'high_movers': self._get_high_movers(lines),
            'slow_movers': self._get_slow_movers(lines),
        }

        # Get filters
        filters = {
            'pos_sources': self._get_pos_sources(),
            'categories': self._get_categories(),
        }

        return {
            'kpis': kpis,
            'charts': charts,
            'tables': tables,
            'filters': filters,
        }

    def _calculate_kpis(self, lines):
        """Calculate key performance indicators"""
        if not lines:
            return {
                'total_sales': 0,
                'total_cost': 0,
                'total_margin': 0,
                'margin_pct': 0,
                'total_qty': 0,
                'avg_margin_pct': 0,
                'flagged_items': 0,
                'total_items': 0,
                'quality_score': 0,
                'avg_selling_price': 0,
            }

        total_sales = sum(lines.mapped('sales_value'))
        total_sales_base = sum(lines.mapped('sales_value_in_currency'))

        total_cost = sum(lines.mapped('cost_value'))
        total_margin = total_sales - total_cost

        margin_pct = (total_margin / total_sales * 100) if total_sales else 0
        total_qty = sum(lines.mapped('quantity'))

        flagged_count =0# len(lines.filtered(lambda l: l.flag != 'ok'))
        avg_margin_pct = sum(lines.mapped('margin_pct')) / len(lines) if lines else 0
        avg_selling_price = total_sales / total_qty if total_qty > 0 else 0

        return {
            'total_sales': round(float(total_sales), 2),
            'total_cost': round(float(total_cost), 2),
            'total_margin': round(float(total_margin), 2),
            'margin_pct': round(float(margin_pct), 1),
            'total_qty': int(total_qty),
            'avg_margin_pct': round(float(avg_margin_pct), 1),
            'flagged_items': flagged_count,
            'total_items': len(lines),
            'quality_score': round(((len(lines) - flagged_count) / len(lines) * 100), 1) if lines else 0,
            'avg_selling_price': round(float(avg_selling_price), 2),
        }

    def _get_sales_trend(self, lines, start_date, end_date):
        """Get daily sales trend"""
        trend_data = {}
        for line in lines:
            date_key = line.date.strftime('%Y-%m-%d')
            if date_key not in trend_data:
                trend_data[date_key] = {'sales': 0, 'cost': 0, 'margin': 0}
            trend_data[date_key]['sales'] += line.sales_value
            trend_data[date_key]['cost'] += line.cost_value
            trend_data[date_key]['margin'] += line.margin_value

        sorted_dates = sorted(trend_data.keys())
        return {
            'dates': sorted_dates,
            'sales': [round(float(trend_data[d]['sales']), 2) for d in sorted_dates],
            'cost': [round(float(trend_data[d]['cost']), 2) for d in sorted_dates],
            'margin': [round(float(trend_data[d]['margin']), 2) for d in sorted_dates],
        }

    def _get_margin_by_outlet(self, lines):
        """Get margin percentage by outlet"""
        outlet_data = {}
        for line in lines:
            outlet = line.pos_source_id.name
            if outlet not in outlet_data:
                outlet_data[outlet] = {'sales': 0, 'margin': 0}
            outlet_data[outlet]['sales'] += line.sales_value
            outlet_data[outlet]['margin'] += line.margin_value

        result = []
        for outlet, data in outlet_data.items():
            margin_pct = (data['margin'] / data['sales'] * 100) if data['sales'] else 0
            result.append({
                'outlet': outlet,
                'margin_pct': round(float(margin_pct), 1),
                'sales': round(float(data['sales']), 2),
            })

        return sorted(result, key=lambda x: x['margin_pct'], reverse=True)

    def _get_high_movers(self, lines):
        """Get top 10 high moving products"""
        product_data = {}
        for line in lines:
            product = line.product_id.name if line.product_id else 'Unknown'
            product_id = line.product_id.id if line.product_id else 0
            if product not in product_data:
                product_data[product] = {
                    'qty': 0,
                    'sales': 0,
                    'margin': 0,
                    'cost': 0,
                    'product_id': product_id,
                }
            product_data[product]['qty'] += line.quantity
            product_data[product]['sales'] += line.sales_value
            product_data[product]['margin'] += line.margin_value
            product_data[product]['cost'] += line.cost_value

        result = []
        for product, data in product_data.items():
            margin_pct = (data['margin'] / data['sales'] * 100) if data['sales'] else 0
            result.append({
                'product': product,
                'qty': int(data['qty']),
                'sales': round(float(data['sales']), 2),
                'cost': round(float(data['cost']), 2),
                'margin': round(float(data['margin']), 2),
                'margin_pct': round(float(margin_pct), 1),
                'product_id': data['product_id'],
            })

        return sorted(result, key=lambda x: x['qty'], reverse=True)[:10]

    def _get_slow_movers(self, lines):
        """Get slow moving products (lowest qty)"""
        product_data = {}
        for line in lines:
            product = line.product_id.name if line.product_id else 'Unknown'
            product_id = line.product_id.id if line.product_id else 0
            if product not in product_data:
                product_data[product] = {
                    'qty': 0,
                    'sales': 0,
                    'cost': 0,
                    'margin': 0,
                    'product_id': product_id,
                }
            product_data[product]['qty'] += line.sales_value
            product_data[product]['sales'] += line.sales_value
            product_data[product]['cost'] += line.cost_value
            product_data[product]['margin'] += line.margin_value

        result = []
        for product, data in product_data.items():
            if data['qty'] > 0:
                margin_pct = (data['margin'] / data['sales'] * 100) if data['sales'] else 0
                result.append({
                    'product': product,
                    'qty': int(data['qty']),
                    'sales': round(float(data['sales']), 2),
                    'cost': round(float(data['cost']), 2),
                    'margin': round(float(data['margin']), 2),
                    'margin_pct': round(float(margin_pct), 1),
                    'product_id': data['product_id'],
                })

        return sorted(result, key=lambda x: x['qty'])[:10]

    def _get_flag_distribution(self, lines):
        """Get distribution of flags"""
        flags = {}
        for line in lines:
            flag = line.flag
            flags[flag] = flags.get(flag, 0) + 1

        flag_labels = {
            'ok': 'OK',
            'negative_margin': 'Negative Margin',
            'low_margin': 'Low Margin',
            'product_missing': 'Missing Product',
            'price_anomaly': 'Price Anomaly',
        }

        return [
            {
                'flag': flag_labels.get(k, k),
                'count': v,
                'percentage': round((v / len(lines) * 100), 1) if lines else 0,
            }
            for k, v in flags.items()
        ]

    def _get_category_performance(self, lines):
        """Get performance by product category"""
        category_data = {}
        for line in lines:
            if not line.product_id:
                continue
            category = line.product_id.categ_id.name or 'Uncategorized'
            if category not in category_data:
                category_data[category] = {'sales': 0, 'margin': 0, 'qty': 0}
            category_data[category]['sales'] += line.sales_value
            category_data[category]['margin'] += line.margin_value
            category_data[category]['qty'] += line.quantity

        result = []
        for category, data in category_data.items():
            margin_pct = (data['margin'] / data['sales'] * 100) if data['sales'] else 0
            result.append({
                'category': category,
                'sales': round(float(data['sales']), 2),
                'margin_pct': round(float(margin_pct), 1),
                'qty': int(data['qty']),
            })

        return sorted(result, key=lambda x: x['sales'], reverse=True)

    def _get_profit_loss_analysis(self, lines):
        """Get profit/loss analysis"""
        profitable = len(lines.filtered(lambda l: l.margin_value > 0))
        loss = len(lines.filtered(lambda l: l.margin_value < 0))
        break_even = len(lines.filtered(lambda l: l.margin_value == 0))

        return {
            'profitable': profitable,
            'loss': loss,
            'break_even': break_even,
            'total': len(lines),
            'profitable_pct': round((profitable / len(lines) * 100), 1) if lines else 0,
            'loss_pct': round((loss / len(lines) * 100), 1) if lines else 0,
        }

    def _get_low_margin_items(self, lines):
        """Get items with low margin (below 30%)"""
        result = []
        for line in lines:
            if line.margin_pct < 30:  # Low margin threshold
                result.append({
                    'product': line.product_id.name if line.product_id else 'Unknown',
                    'unit_price': round(float(line.avg_price), 2),
                    'cost': round(float(line.cost_value), 2),# need to beck checked
                    'margin_pct': round(float(line.margin_pct), 1),
                    'qty': int(line.quantity),
                    'sales': round(float(line.sales_value), 2),
                })

        return sorted(result, key=lambda x: x['margin_pct'])[:15]

    def _get_pos_sources(self):
        """Get list of POS sources"""
        sources = request.env['bk.pos.source'].search([])
        return [
            {'id': s.id, 'name': s.name}
            for s in sources
        ]

    def _get_categories(self):
        """Get list of product categories"""
        categories = request.env['product.category'].search([])
        return [
            {'id': c.id, 'name': c.name}
            for c in categories
        ]
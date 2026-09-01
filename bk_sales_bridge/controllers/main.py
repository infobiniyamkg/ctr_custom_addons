# -*- coding: utf-8 -*-
"""
Main Controllers - Reporting & Webhooks
CHANGE LOG (v2.0):
- Added HMAC-SHA256 signature verification to receive_sales() webhook
- All other functionality unchanged from v1.0
"""
import io
import json
import logging
import hmac
import hashlib
from datetime import date

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class BkProfitabilityReportController(http.Controller):
    """Generate and download profitability reports in Excel format"""

    @http.route('/bk_sales_bridge/profitability_report/<int:order_id>', type='http', auth='user')
    def profitability_report_single(self, order_id, **kw):
        return self._build_report(request.env['bk.sales.order'].browse(order_id))

    @http.route('/bk_sales_bridge/profitability_report', type='http', auth='user')
    def profitability_report_multi(self, ids=None, **kw):
        if not ids:
            return request.not_found()
        id_list = [int(i) for i in ids.split(',') if i.isdigit()]
        orders = request.env['bk.sales.order'].browse(id_list).exists()
        if not orders:
            return request.not_found()
        return self._build_report(orders)

    def _build_report(self, orders):
        """Generate Excel report with 3 sheets"""
        import xlsxwriter

        if not orders:
            return request.not_found()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        fmt_title = workbook.add_format({'bold': True, 'font_size': 14})
        fmt_sub = workbook.add_format({'italic': True, 'font_color': '#555555'})
        fmt_header = workbook.add_format({
            'bold': True, 'bg_color': '#2F5496', 'font_color': 'white',
            'border': 1, 'align': 'center', 'valign': 'vcenter'
        })
        fmt_cell = workbook.add_format({'border': 1})
        fmt_money = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})
        fmt_pct = workbook.add_format({'border': 1, 'num_format': '0.0%'})
        fmt_qty = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})
        fmt_flag_ok = workbook.add_format({'border': 1, 'bg_color': '#C6EFCE', 'font_color': '#006100'})
        fmt_flag_low = workbook.add_format({'border': 1, 'bg_color': '#FFEB9C', 'font_color': '#9C6500'})
        fmt_flag_bad = workbook.add_format({'border': 1, 'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        fmt_total_label = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D9E1F2'})
        fmt_total_money = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D9E1F2',
                                                'num_format': '#,##0.00'})
        fmt_total_pct = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D9E1F2',
                                              'num_format': '0.0%'})

        all_lines = orders.mapped('line_ids')
        flag_labels = dict(all_lines._fields['flag'].selection) if all_lines else dict(
            request.env['bk.sales.order.line']._fields['flag'].selection)
        flag_format = {
            'ok': fmt_flag_ok, 'low_margin': fmt_flag_low, 'negative_margin': fmt_flag_bad,
            'product_missing': fmt_flag_bad, 'price_anomaly': fmt_flag_bad,
        }

        # ============================================================
        # SHEET 0: Batches Overview
        # ============================================================
        ws0 = workbook.add_worksheet('Batches Overview')
        ws0.set_column('A:A', 16)
        ws0.set_column('B:B', 22)
        ws0.set_column('C:D', 12)
        ws0.set_column('E:I', 15)
        ws0.merge_range('A1:I1', 'Profitability Report - Batches Overview', fmt_title)
        headers0 = ['Batch Ref', 'POS Source', 'Start Date', 'End Date', 'Total Sales',
                    'Total Cost', 'Margin Value', 'Margin %', 'Flagged Lines']
        for col, h in enumerate(headers0):
            ws0.write(2, col, h, fmt_header)
        row = 3
        for order in orders:
            ws0.write(row, 0, order.name, fmt_cell)
            ws0.write(row, 1, order.pos_source_id.name, fmt_cell)
            ws0.write(row, 2, str(order.start_date or ''), fmt_cell)
            ws0.write(row, 3, str(order.end_date or ''), fmt_cell)
            ws0.write(row, 4, order.total_sales, fmt_money)
            ws0.write(row, 5, order.total_cost, fmt_money)
            ws0.write(row, 6, order.total_margin_value, fmt_money)
            ws0.write(row, 7, (order.margin_pct or 0.0) / 100.0, fmt_pct)
            ws0.write(row, 8, order.flagged_line_count, fmt_cell)
            row += 1
        ws0.write(row, 0, 'GRAND TOTAL', fmt_total_label)
        ws0.write(row, 4, sum(orders.mapped('total_sales')), fmt_total_money)
        ws0.write(row, 5, sum(orders.mapped('total_cost')), fmt_total_money)
        ws0.write(row, 6, sum(orders.mapped('total_margin_value')), fmt_total_money)
        total_sales_all = sum(orders.mapped('total_sales'))
        total_margin_all = sum(orders.mapped('total_margin_value'))
        ws0.write(row, 7, (total_margin_all / total_sales_all) if total_sales_all else 0.0,
                  fmt_total_pct)
        ws0.write(row, 8, sum(orders.mapped('flagged_line_count')), fmt_total_money)

        # ============================================================
        # SHEET 1: Sold Items Detail
        # ============================================================
        ws1 = workbook.add_worksheet('Sold Items')
        ws1.set_column('A:A', 14)
        ws1.set_column('B:B', 12)
        ws1.set_column('C:C', 14)
        ws1.set_column('D:E', 26)
        ws1.set_column('F:F', 10)
        ws1.set_column('G:I', 13)
        ws1.set_column('J:K', 13)
        ws1.set_column('L:N', 13)
        ws1.set_column('O:O', 16)

        ws1.merge_range('A1:O1', 'Sold Items Report', fmt_title)
        label = orders[0].name if len(orders) == 1 else '%d batches selected' % len(orders)
        ws1.merge_range('A2:O2', label, fmt_sub)

        headers = ['Batch', 'Date', 'External Code', 'External Name', 'Odoo Product', 'Sold Qty',
                   'Unit Price', 'Discount', 'Net Sales', 'Unit Cost', 'Total Cost',
                   'Margin Value', 'Margin %', 'Tax Type', 'Flag']
        row = 3
        for col, h in enumerate(headers):
            ws1.write(row, col, h, fmt_header)
        row += 1

        for order in orders:
            for line in order.line_ids.sorted(key=lambda l: (l.date, l.external_code)):
                ws1.write(row, 0, order.name, fmt_cell)
                ws1.write(row, 1, str(line.date or ''), fmt_cell)
                ws1.write(row, 2, line.external_code or '', fmt_cell)
                ws1.write(row, 3, line.external_name or '', fmt_cell)
                ws1.write(row, 4, line.product_id.display_name or 'NOT MAPPED', fmt_cell)
                ws1.write(row, 5, line.sold_qty, fmt_qty)
                ws1.write(row, 6, line.unit_price, fmt_money)
                ws1.write(row, 7, line.discount_amount, fmt_money)
                ws1.write(row, 8, line.net_sales_value, fmt_money)
                ws1.write(row, 9, line.current_cost, fmt_money)
                ws1.write(row, 10, line.total_cost, fmt_money)
                ws1.write(row, 11, line.margin_value, fmt_money)
                ws1.write(row, 12, (line.margin_pct or 0.0) / 100.0, fmt_pct)
                ws1.write(row, 13, line.tax_type or '', fmt_cell)
                ws1.write(row, 14, flag_labels.get(line.flag, line.flag or ''),
                          flag_format.get(line.flag, fmt_cell))
                row += 1

        ws1.write(row, 4, 'TOTAL', fmt_total_label)
        ws1.write(row, 5, sum(all_lines.mapped('sold_qty')), fmt_total_money)
        ws1.write(row, 8, sum(all_lines.mapped('net_sales_value')), fmt_total_money)
        ws1.write(row, 10, sum(all_lines.mapped('total_cost')), fmt_total_money)
        ws1.write(row, 11, sum(all_lines.mapped('margin_value')), fmt_total_money)
        total_sales = sum(all_lines.mapped('net_sales_value'))
        total_margin = sum(all_lines.mapped('margin_value'))
        ws1.write(row, 12, (total_margin / total_sales) if total_sales else 0.0, fmt_total_pct)
        ws1.freeze_panes(4, 0)

        # ============================================================
        # SHEET 2: Profitability Summary by Product
        # ============================================================
        ws2 = workbook.add_worksheet('Profitability Summary')
        ws2.set_column('A:A', 30)
        ws2.set_column('B:G', 15)
        ws2.merge_range('A1:G1', 'Profitability Summary by Product', fmt_title)
        ws2.merge_range('A2:G2', label, fmt_sub)

        headers2 = ['Product', 'Qty Sold', 'Net Sales Value', 'Total Cost',
                    'Margin Value', 'Margin %', 'Flag Summary']
        row = 3
        for col, h in enumerate(headers2):
            ws2.write(row, col, h, fmt_header)
        row += 1

        grouped = {}
        for line in all_lines:
            key = line.product_id.id or 0
            grp_label = line.product_id.display_name or (line.external_name or 'NOT MAPPED')
            g = grouped.setdefault(key, {'label': grp_label, 'qty': 0.0, 'sales': 0.0,
                                          'cost': 0.0, 'margin': 0.0, 'flags': set()})
            g['qty'] += line.sold_qty
            g['sales'] += line.net_sales_value
            g['cost'] += line.total_cost
            g['margin'] += line.margin_value
            g['flags'].add(flag_labels.get(line.flag, line.flag))

        for g in sorted(grouped.values(), key=lambda x: x['margin']):
            margin_pct = (g['margin'] / g['sales']) if g['sales'] else 0.0
            worst_flag = 'ok'
            if 'Product Not Found' in g['flags']:
                worst_flag = 'product_missing'
            elif 'Negative Margin' in g['flags']:
                worst_flag = 'negative_margin'
            elif 'Below Threshold Margin' in g['flags']:
                worst_flag = 'low_margin'
            ws2.write(row, 0, g['label'], fmt_cell)
            ws2.write(row, 1, g['qty'], fmt_qty)
            ws2.write(row, 2, g['sales'], fmt_money)
            ws2.write(row, 3, g['cost'], fmt_money)
            ws2.write(row, 4, g['margin'], fmt_money)
            ws2.write(row, 5, margin_pct, fmt_pct)
            ws2.write(row, 6, ', '.join(g['flags']), flag_format.get(worst_flag, fmt_cell))
            row += 1

        ws2.write(row, 0, 'GRAND TOTAL', fmt_total_label)
        ws2.write(row, 1, sum(all_lines.mapped('sold_qty')), fmt_total_money)
        ws2.write(row, 2, total_sales, fmt_total_money)
        ws2.write(row, 3, sum(all_lines.mapped('total_cost')), fmt_total_money)
        ws2.write(row, 4, total_margin, fmt_total_money)
        ws2.write(row, 5, (total_margin / total_sales) if total_sales else 0.0, fmt_total_pct)
        ws2.freeze_panes(4, 0)

        workbook.close()
        output.seek(0)
        if len(orders) == 1:
            filename = 'Profitability_Report_%s.xlsx' % orders[0].name
        else:
            filename = 'Profitability_Report_%d_batches.xlsx' % len(orders)

        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument'
                                  '.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="%s"' % filename),
            ]
        )


class BkPosWebhookController(http.Controller):
    """
    Inbound webhook: POS can PUSH sales transactions to Odoo
    
    CHANGE v2.0: Added HMAC-SHA256 signature verification
    """

    @http.route('/bk_sales_bridge/api/sales/push', type='json', auth='none', methods=['POST'],
                csrf=False)
    def receive_sales(self, **payload):
        env = request.env(su=True)
        
        try:
            data = payload or json.loads(request.httprequest.data or '{}')
        except:
            return {'status': 'error', 'message': 'Invalid JSON payload'}

        source_id = data.get('pos_source_id')
        source = env['bk.pos.source'].browse(source_id) if source_id else env['bk.pos.source']
        if not source.exists():
            return {'status': 'error', 'message': 'Unknown pos_source_id'}

        # Verify API key
        api_key = request.httprequest.headers.get('X-POS-API-Key')
        expected_key = source._get_api_key()
        if not expected_key or (api_key != expected_key):
            return {'status': 'error', 'message': 'Invalid or missing API key'}

        # CHANGE v2.0: Verify HMAC signature if provided
        signature = request.httprequest.headers.get('X-Signature')
        if signature and expected_key:
            body = request.httprequest.data
            expected_sig = hmac.new(
                expected_key.encode(),
                body,
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_sig):
                _logger.warning('Webhook signature mismatch from %s', source.name)
                return {'status': 'error', 'message': 'Unauthorized: signature mismatch'}

        transactions = data.get('transactions', [])
        if not transactions:
            return {'status': 'error', 'message': 'No transactions provided'}

        # Find or create an open batch covering today
        today = date.today()
        batch = env['bk.sales.order'].search([
            ('pos_source_id', '=', source.id),
            ('state', 'in', ('draft', 'review')),
            ('start_date', '<=', today),
            ('end_date', '>=', today),
        ], limit=1)
        if not batch:
            batch = env['bk.sales.order'].create({
                'pos_source_id': source.id,
                'start_date': today,
                'end_date': today,
            })

        map_obj = env['bk.pos.product.map']
        line_obj = env['bk.sales.order.line']
        created, skipped, errors = 0, 0, []

        for tx in transactions:
            ext_ref = tx.get('transaction_id')
            if not ext_ref:
                errors.append('Missing transaction_id, skipped')
                continue
            if line_obj.search_count([('external_ref', '=', ext_ref)]):
                skipped += 1
                continue
            mapping = map_obj.search([
                ('pos_source_id', '=', source.id),
                ('external_code', '=', tx.get('product_code')),
                ('active', '=', True),
            ], limit=1)
            product = mapping.product_id if mapping else False
            try:
                line_obj.create({
                    'order_id': batch.id,
                    'date': tx.get('date') or str(today),
                    'external_code': tx.get('product_code'),
                    'external_name': tx.get('product_name'),
                    'external_ref': ext_ref,
                    'product_id': product.id if product else False,
                    'product_type': ('recipe' if mapping and mapping.is_recipe else 'direct')
                                     if mapping else False,
                    'sold_qty': tx.get('qty') or 0.0,
                    'unit_price': tx.get('unit_price') or 0.0,
                    'discount_amount': tx.get('discount') or 0.0,
                    'tax_type': tx.get('tax_type', 'VAT'),
                    'tax_amount': tx.get('tax_amount', 0),
                    'customer_name': tx.get('customer_name'),
                    'customer_code': tx.get('customer_code'),
                })
                created += 1
            except Exception as e:
                errors.append('%s: %s' % (ext_ref, str(e)))

        env['bk.pos.sync.log'].create({
            'pos_source_id': source.id,
            'direction': 'inbound',
            'operation': 'receive_sales',
            'status': 'error' if errors else 'success',
            'endpoint': '/bk_sales_bridge/api/sales/push',
            'request_payload': json.dumps(data)[:5000],
            'response_payload': json.dumps({'created': created, 'skipped': skipped}),
            'error_message': '; '.join(errors) if errors else False,
            'sales_order_id': batch.id,
        })

        _logger.info('Webhook: created=%d, skipped=%d, errors=%d for source %s',
                    created, skipped, len(errors), source.name)

        return {'status': 'ok', 'batch': batch.name, 'created': created,
                'skipped': skipped, 'errors': errors}

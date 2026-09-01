{
    'name': 'BK Sales Bridge',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'POS-to-Odoo middleware',
    'description': """POS Integraiton with CNET    """,
    'author': 'Biniyam K|info.biniyamkg@gmail.com',

    'depends': ['base', 'sale_management', 'stock', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/pos_source_views.xml',
        'views/pos_product_map_views.xml',
        'views/sales_order_views.xml',
        'views/bk_sales_order_line_view.xml',
        'views/bk_sales_transactions_view.xml',
        'views/menu_views.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'bk_sales_bridge/static/lib/chart/chart.umd.js',
    #         'bk_sales_bridge/static/src/css/style.css',
    #         'bk_sales_bridge/static/src/xml/dashboard.xml',
    #         'bk_sales_bridge/static/src/js/dashboard.js',
    #     ],
    # },

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

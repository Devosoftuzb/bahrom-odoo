{
    'name': 'UIC POST',
    'version': '1.0',
    'website': 'https://www.bahromnajmiddinov.com',
    'author': 'Bahrom Najmiddinov',
    'description': """
         UIC POST management system.
    """,
    'category': 'Website',
    'depends': ['base', 'mail', 'stock', 'delivery', 'sale'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/security_groups.xml',

        'views/menu_items.xml',

        # 'data/eduhub.week.day.csv',
        # 'data/eduhub_invoicing_sequence.xml',

        'views/search_order.xml',
        'views/custom_navbar_link.xml',

        'views/promocode_view.xml',
        'views/stock_picking_view.xml',
        'views/custom_product_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
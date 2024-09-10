{
    'name': 'Custom Ecom',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Customizations for eCommerce Product Details',
    'depends': ['website_sale'],
    'data': [
        # 'static/xml/product_template_views.xml',
        'views/product_template_views.xml',
        'views/most_sold_products_template.xml',
    ],
    'installable': True,
    'application': False,
}

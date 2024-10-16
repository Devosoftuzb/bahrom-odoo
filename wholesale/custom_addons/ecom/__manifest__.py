{
    'name': 'Custom Ecom',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Customizations for eCommerce Product Details',
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        # 'static/xml/product_template_views.xml',
        'views/product_template_views.xml',
        'views/most_sold_products_template.xml',
        'views/brands.xml',
    ],
    'installable': True,
    'application': True,
}

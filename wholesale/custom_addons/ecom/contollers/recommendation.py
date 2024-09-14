from odoo import http
from odoo.http import request


class ProductController(http.Controller):
    @http.route(['/shop/shop/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product_recommendation(self, product, **kwargs):
        # Get recommended products (e.g., products in the same category)
        recommended_products = request.env['product.template'].search([
            ('id', '!=', product.id),  # Exclude the current product
            ('categ_id', '=', product.categ_id.id)  # Filter by the same category
        ], limit=3)  # Limit the number of recommended products

        values = {
            'product': product,
            'recommended_products': recommended_products,
        }
        print(product, recommended_products)

        return request.render("ecom.custom_product_detail", values)

    @http.route('/shop/most_sold_products', type='http', auth='public', website=True)
    def most_sold_products(self, **kwargs):
        categories = request.env['product.public.category'].search([])

        category = request.httprequest.args.get('category')
        category_id = request.env['product.public.category'].search([('name', '=', category)], limit=1)

        if not category and not bool(category_id):
            current_category_id = 'all'
            search_domain = [('state', 'in', ['sale', 'done'])]
        else:
            current_category_id = category_id.id
            search_domain = [
                ('state', 'in', ['sale', 'done']),
                ('product_id.product_tmpl_id.categ_id', '=', current_category_id)
            ]

        products_data = request.env['sale.order.line'].read_group(
            search_domain,
            ['product_id', 'product_uom_qty'],
            ['product_id'],
            orderby='product_uom_qty desc',
            limit=10
        )

        product_sales = []
        for data in products_data:
            product = request.env['product.product'].browse(data['product_id'][0])
            product_sales.append({
                'product': product,
                'sales_count': data['product_uom_qty'],  # Total quantity sold
            })

        return request.render('ecom.most_sold_products', {
            'product_sales': product_sales,
            'test_value': 'test',
            'recommended_products': True,
            'categories': categories,
            'current_category_id': current_category_id,
        })

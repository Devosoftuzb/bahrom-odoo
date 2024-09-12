from odoo import http
from odoo.http import request


class ReviewController(http.Controller):
    @http.route('/submit-review', type='http', auth='user', website='True', methods=['POST'])
    def submit_review(self, product_id, comment, **kwargs):
        product = request.env['product.template'].browse(int(product_id))
        partner = request.env.user.partner_id

        if partner.has_bought_product(product_id):
            request.env['product.review'].create({
                'product_id': product.id,
                'partner_id': partner.id,
                'rating': kwargs.get('rating', 5),  # default rating to 5
                'comment': comment,
            })
            print(request.env['product.review'].search([]))
            print('hello world')
            return request.redirect('/shop/product/%s' % product.id)
        else:
            return request.redirect('/shop/product/%s?error=not_purchased' % product.id)

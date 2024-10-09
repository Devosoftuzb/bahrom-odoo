from odoo import http
from odoo.http import request


class SearchOrder(http.Controller):
    @http.route('/search-order/', type='http', auth='public', website=True)
    def search_order(self):
        order_status = None
        track_id = request.params.get('track_id')

        # Check if the tracking ID is provided
        if track_id:
            # Search for stock.picking records with the given track ID
            order_status = request.env['stock.picking'].search([('name', '=', track_id)], limit=1)

        context = {
            'results': order_status,
            'search': track_id,
        }

        return request.render('post.search_order_template', context)

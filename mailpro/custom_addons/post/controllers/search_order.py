from odoo import http
from odoo.http import request


class SearchOrder(http.Controller):
    @http.route('/search-order/', type='http', auth='public', website=True)
    def search_order(self):
        # Initialize variables
        order_status = None
        track_id = request.params.get('track_id')

        # Check if the tracking ID is provided
        if track_id:
            # Search for stock.picking records with the given track ID
            order_status = request.env['stock.picking'].search([('name', '=', track_id)], limit=1)

        # If no records were found, order_status will be an empty recordset
        context = {
            'results': order_status,  # Pass the recordset directly
            'search': track_id,        # Set the search value for the template
        }

        return request.render('post.search_order_template', context)

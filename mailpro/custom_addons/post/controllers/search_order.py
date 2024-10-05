from odoo import http
from odoo.http import request


class SearchOrder(http.Controller):
    @http.route('/search-order/', type='http', auth='public', website=True)
    def search_order(self):
        order_status = self.env['stock.picking'].search((
            [('priority', '=', request.params['priority'])],
        ), limit=1)

        context = {
            'results': order_status.read(['name', 'state', 'priority']),
            'search': request.params,
            'fuzzy_search': [],
        }

        return request.render('post.search_order_template', context)

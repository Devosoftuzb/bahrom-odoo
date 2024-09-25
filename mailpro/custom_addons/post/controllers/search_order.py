from odoo import http
from odoo.http import request


class SearchOrder(http.Controller):
    @http.route('/search-order/', type='http', auth='public', website=True)
    def search_order(self):

        context = {
            'results': [],
            'search': [],
            'fuzzy_search': [],
        }

        return request.render('post.search_order_template', context)

from odoo import http
from odoo.http import request


class CurrentLocation(http.Controller):
    @http.route(['/get-current-location/'], type='http', auth="public", website=True)
    def get_current_location(self, **kwargs):
        pass


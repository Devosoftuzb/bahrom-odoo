from odoo import http


class QwebTutorials(http.Controller):
    @http.route('/qweb-tutorials', type='http', auth='public', website=True)
    def qweb_tutorials(self):
        """
        Qweb tutorials
        """

        def some_function():
            return 'returning string from function'

        some_model = http.request.env['sale.order'].search([])

        data = {
            'string': 'QWEB Tutorial',
            'integer': 1000,
            'some_float': 10.05,
            'boolean': True,
            'some_list': [1, 2, 3, 4, 5],
            'some_dict': {'any_key': 'any_value'},
            'some_function': some_function(),
            'model': some_model,
        }

        return http.request.render('learn_qweb.somePythonTemplate', data)

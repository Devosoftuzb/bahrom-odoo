{
    'name': 'QWEB Tutorial',
    'version': '1.0.0',
    'summary': 'QWEB Tutorial',
    'sequence': -1,
    'description': '''QWEB Tutorial''',
    'category': 'Website',
    'depends': ['web', 'website'],
    'data': [
        'views/for_python_templates.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            'learn_qweb/static/src/*',
        ],
    },
}
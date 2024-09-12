{
    "name": "ToDo APP",
    "version": "1.0",
    "website": "https://www.bahromnajmiddinov.com",
    "author": "Bahrom Najmiddinov",
    "description": """
         Do things in time.
    """,
    "category": "Productivity",
    'depends': ['base', 'web', 'mail'],
    "data": [
        'security/ir.model.access.csv',

        'views/tasks.xml',
        'views/menu_items.xml',

        'views/map_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'todoapp/static/src/css/calendar_custom.css',
            # 'todoapp/static/src/js/calendar_custom.js',

            # 'todoapp/static/src/js/map_widget.js',
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
{
    'name': 'EduHUB CRM',
    'version': '1.0',
    'website': 'https://www.bahromnajmiddinov.com',
    'author': 'Bahrom Najmiddinov',
    'description': """
         EduHUB management system.
    """,
    'category': '',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',

        'views/tasks.xml',
        'views/menu_items.xml',

        'views/map_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
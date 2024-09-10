{
    'name': 'Hospital Management System',
    'version': '1.0.0',
    'author': 'Bahrom Najmiddinov',
    'category': 'Services',
    'summary': 'A comprehensive hospital management system for managing patients, appointments, and medical records.',
    'description': """
        This module provides a full-fledged hospital management system. 
        It includes features for managing patient records, appointments, doctors, 
        departments, and more.
    """,
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/hospital_doctor_sequence.xml',
        'views/menu.xml',
        'views/patient.xml',
        'views/doctors.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
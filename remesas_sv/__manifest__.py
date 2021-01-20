# -*- coding: utf-8 -*-

{
    'name': 'Remesas en El Salvador',
    'version': '0.01',
    'category': 'Contabilidad',
    'description': '''
Modulo para hacer registros de remesas en El Salvador
==========================================
    -	Crea un formulario para el registro de la informacion de cada
    remesa realizada.
''',
    'author': 'SewingSolution',
    'website': '',
    'price': 50.00,
    'currency': 'USD',
    'license': 'GPL-3',
    'data': [
        'views/remesa_view.xml',
        'views/graficos_view.xml',
        'data/remesa_sv_sequence_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/remesa_workflow.xml',
    ],
    'depends': [
        'base',
        'mail',
        'account'
    ],
    'installable': True,
    'auto_install': False
}

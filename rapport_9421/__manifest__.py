{
    'name': 'Rapport Etat 9421 Maroc',
    'version': '18.0.2.0.0',
    'author': 'nikouri',
    'category': 'Payroll',
    'summary': 'Generation du rapport annuel 9421 pour la DGI Maroc',
    'license': 'LGPL-3',
    'depends': ['hr', 'payroll', 'infos_employe'],
    'data': [
        'security/ir.model.access.csv',
        'data/rapport_9421_config.xml',
        'views/wizard_9421_views.xml',
        'views/historique_9421_views.xml',
        'report/report_9421_template.xml',
    ],
    'installable': True,
    'auto_install': False,
}
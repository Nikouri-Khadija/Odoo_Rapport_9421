# Module provisoire (instance de test balance_doosys) : remplace le vrai
# module infos_employe, absent du dépôt. Seuls les champs lus par rapport_9421.
{
    'name': 'Infos employé (provisoire)',
    'version': '18.0.0.1',
    'depends': ['hr'],
    'data': ['views/hr_employee_views.xml'],
    'license': 'LGPL-3',
}

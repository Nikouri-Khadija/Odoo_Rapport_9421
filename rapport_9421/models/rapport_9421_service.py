from odoo import models
from odoo.exceptions import UserError


class Rapport9421Service(models.AbstractModel):
    _name = 'rapport.9421.service'
    _description = 'Service metier Rapport 9421'

    def calculer_donnees_rapport(self, annee, company_id):
        config = self.env['rapport.9421.config'].get_for_company(
            self.env, company_id
        )
        company = self.env['res.company'].browse(company_id)
        payslips = self._rechercher_bulletins(annee, company_id, config)
        employees = self._regrouper_par_employe(payslips, config)

        return {
            'annee': annee,
            'company_name': company.name,
            'company_if': company.identifiant_fiscal or '',
            'company_vat': company.vat or '',
            'company_street': company.street or '',
            'company_city': company.city or '',
            'taux_frais_pro': config.taux_frais_pro,
            'employees': employees,
        }

    def _rechercher_bulletins(self, annee, company_id, config):
        """Recherche les bulletins de Ma Structure Salariale uniquement."""
        payslips = self.env['hr.payslip'].search([
            ('date_from', '>=', '%s-01-01' % annee),
            ('date_to',   '<=', '%s-12-31' % annee),
            ('state', 'in', ['done', 'paid']),
            ('company_id', '=', company_id),
            ('struct_id.code', '=', config.code_structure),  # ← filtre structure
        ])
        if not payslips:
            raise UserError(
                'Aucun bulletin confirme trouve pour l\'annee %s '
                'avec la structure "%s".' % (annee, config.code_structure)
            )
        return payslips

    def _regrouper_par_employe(self, payslips, config):
        codes = config.get_codes()
        # Inverse : code_rubrique -> clé interne
        code_vers_cle = {v: k for k, v in codes.items()}

        employes = {}
        for slip in payslips:
            emp = slip.employee_id
            if emp.id not in employes:
                employes[emp.id] = self._init_employe(emp)
            self._accumuler_rubriques(employes[emp.id], slip, code_vers_cle)
            self._accumuler_jours(employes[emp.id], slip, config.jours_defaut)

        return list(employes.values())

    def _init_employe(self, emp):
        return {
            'emp_matricule': emp.barcode or '',
            'emp_name':      emp.name,
            'emp_address':   ' '.join(filter(None, [
                emp.private_street or '',
                emp.private_city or '',
            ])),
            'emp_cin':       emp.x_num_cin or '',
            'emp_fiscal':    emp.x_num_fiscal or '',
            'emp_cnss':      emp.x_num_cnss or '',
            'emp_marital':   emp.marital,
            'emp_children':  emp.children or 0,
            # Montants
            'sbrut':     0.0,
            'transport': 0.0,
            'exonere':   0.0,
            'sbi':       0.0,
            'cnss':      0.0,
            'amo':       0.0,
            'cimr':      0.0,
            'frais_pro': 0.0,
            'sni':       0.0,
            'irs_net':   0.0,
            'sn':        0.0,
            'jours':     0.0,
            'avantage': 0.0,
        }

    def _accumuler_rubriques(self, emp_data, slip, code_vers_cle):
        # Ces rubriques sont négatives dans le bulletin → on prend abs()
        valeur_absolue = {'CNSS', 'AMO', 'CIMR', 'IRS_NET', 'FRAIS_PRO'}

        cle_vers_champ = {
            'SBRUT':     'sbrut',
            'TRANSPORT': 'transport',
            'EXONERE':   'exonere',
            'AVANTAGE':  'avantage',
            'SBI':       'sbi',
            'CNSS':      'cnss',
            'AMO':       'amo',
            'CIMR':      'cimr',
            'FRAIS_PRO': 'frais_pro',
            'SNI':       'sni',
            'IRS_NET':   'irs_net',
            'SN':        'sn',
        }

        for line in slip.line_ids:
            cle = code_vers_cle.get(line.code)
            if not cle:
                continue
            champ = cle_vers_champ.get(cle)
            if not champ:
                continue
            valeur = abs(line.total) if cle in valeur_absolue else line.total
            emp_data[champ] += valeur

    def _accumuler_jours(self, emp_data, slip, jours_defaut):
        jours = sum(
            line.number_of_days
            for line in slip.worked_days_line_ids
        )
        emp_data['jours'] += jours if jours > 0 else jours_defaut
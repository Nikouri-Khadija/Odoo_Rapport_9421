# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrCotisation(models.Model):
    _name = 'hr.cotisation'
    _description = 'Cotisations Sociales'
    _order = 'code asc'

    code = fields.Char(string='Code', required=True)
    designation = fields.Char(string='Désignation', required=True)
    taux_salarial = fields.Float(string='Taux Salarial (%)', digits=(16, 2))
    cotisation_plafonnee = fields.Boolean(string='Cotisation Plafonnée')
    plafond = fields.Float(string='Plafond', digits=(16, 2))

    @api.constrains('cotisation_plafonnee', 'plafond')
    def _check_plafond(self):
        for rec in self:
            if rec.cotisation_plafonnee and rec.plafond <= 0:
                raise ValidationError(
                    "Le plafond doit être supérieur à 0 si la cotisation est plafonnée."
                )

    @api.model
    def get_cotisation(self, code, base):
        """
        Retourne le montant de la cotisation calculée.
        - code : le code de la cotisation (ex: 'CNSS', 'AMO', 'CIMR')
        - base : la base de calcul
        Usage dans les règles salariales :
            result = -payslip.env['hr.cotisation'].get_cotisation('CNSS', base)
        """
        cotisation = self.search([('code', '=', code)], limit=1)
        if not cotisation:
            return 0.0

        # Appliquer le plafond si la cotisation est plafonnée
        montant = base * (cotisation.taux_salarial / 100.0)
        if cotisation.cotisation_plafonnee and cotisation.plafond > 0:
          montant = min(montant, cotisation.plafond)
        return montant  
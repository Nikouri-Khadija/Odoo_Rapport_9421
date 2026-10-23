# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrAnciennete(models.Model):
    _name = 'hr.anciennete'
    _description = 'Barème Ancienneté'
    _order = 'debut_tranche asc'

    debut_tranche = fields.Float(
        string='Début Tranche',
        required=True,
        digits=(16, 2),
        help="Nombre d'années (début de la tranche, inclus)"
    )
    fin_tranche = fields.Float(
        string='Fin Tranche',
        required=True,
        digits=(16, 2),
        help="Nombre d'années (fin de la tranche, exclus)"
    )
    taux = fields.Float(
        string='Taux (%)',
        required=True,
        digits=(16, 2),
        help="Taux d'ancienneté en pourcentage (ex: 5 pour 5%)"
    )

    @api.constrains('debut_tranche', 'fin_tranche')
    def _check_tranches(self):
        for rec in self:
            if rec.fin_tranche <= rec.debut_tranche:
                raise ValidationError(
                    "La Fin Tranche doit être supérieure au Début Tranche."
                )

    @api.constrains('taux')
    def _check_taux(self):
        for rec in self:
            if rec.taux < 0:
                raise ValidationError("Le taux ne peut pas être négatif.")

    @api.model
    def get_taux_for_anciennete(self, anciennete_annees):
        """
        Retourne le taux (en décimal, ex: 0.05) correspondant
        au nombre d'années d'ancienneté passé en paramètre.
        Usage dans les règles salariales :
            taux = env['hr.anciennete'].get_taux_for_anciennete(anciennete)
            result = contract.wage * taux
        """
        bareme = self.search([
            ('debut_tranche', '<=', anciennete_annees),
            ('fin_tranche', '>', anciennete_annees),
        ], limit=1)
        if bareme:
            return bareme.taux / 100.0
        # Si ancienneté dépasse toutes les tranches, prendre la dernière
        last = self.search([], order='debut_tranche desc', limit=1)
        if last and anciennete_annees >= last.debut_tranche:
            return last.taux / 100.0
        return 0.0

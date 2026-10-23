# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrIr(models.Model):
    _name = 'hr.ir'
    _description = 'Barème IR'
    _order = 'debut_tranche asc'

    debut_tranche = fields.Float(string='Début de Tranche', required=True, digits=(16,2))
    fin_tranche = fields.Float(string='Fin de tranche', required=True, digits=(16,2))
    taux = fields.Float(string='Taux (%)', required=True, digits=(16,2))
    somme_a_deduire = fields.Float(string='Somme à déduire', required=True, digits=(16,2))

    @api.constrains('debut_tranche', 'fin_tranche')
    def _check_tranches(self):
        for rec in self:
            if rec.fin_tranche <= rec.debut_tranche:
                raise ValidationError("La fin de tranche doit être supérieure au début.")

    @api.model
    def get_ir(self, sni_mensuel):
        """
        Calcule l'IR mensuel selon le barème.
        - sni_mensuel : SNI du mois
        Retourne l'IR mensuel (positif).
        Usage dans les règles salariales :
            result = -payslip.env['hr.ir'].get_ir(categories.SNI)
        """
        bareme = self.search([
            ('debut_tranche', '<=', sni_mensuel),
            ('fin_tranche', '>=', sni_mensuel),
        ], limit=1)

        if not bareme:
            # Si SNI dépasse toutes les tranches, prendre la dernière
            bareme = self.search([], order='debut_tranche desc', limit=1)
            if not bareme:
                return 0.0

        ir = (sni_mensuel * (bareme.taux / 100.0)) - bareme.somme_a_deduire
        return max(ir, 0.0)
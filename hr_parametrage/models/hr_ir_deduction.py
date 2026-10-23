# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrIrDeduction(models.Model):
    _name = 'hr.ir.deduction'
    _description = 'Configuration Déductions IR'

    deduction_epouse = fields.Float(
        string='Déduction Épouse (MAD)',
        required=True,
        digits=(16, 2),
    )
    deduction_enfant = fields.Float(
        string='Déduction par Enfant (MAD)',
        required=True,
        digits=(16, 2),
    )
    plafond = fields.Float(
        string='Plafond Total (MAD)',
        required=True,
        digits=(16, 2),
    )

    @api.constrains('deduction_epouse', 'deduction_enfant', 'plafond')
    def _check_valeurs(self):
        for rec in self:
            if rec.deduction_epouse < 0:
                raise ValidationError("La déduction épouse ne peut pas être négative.")
            if rec.deduction_enfant < 0:
                raise ValidationError("La déduction par enfant ne peut pas être négative.")
            if rec.plafond < 0:
                raise ValidationError("Le plafond ne peut pas être négatif.")

    @api.model
    def get_config(self):
        config = self.search([], limit=1)
        if config:
            return {
                'deduction_epouse': config.deduction_epouse,
                'deduction_enfant': config.deduction_enfant,
                'plafond':          config.plafond,
            }
        return {'deduction_epouse': 0.0, 'deduction_enfant': 0.0, 'plafond': 0.0}
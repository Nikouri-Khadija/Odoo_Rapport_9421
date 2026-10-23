from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    x_num_cin = fields.Char('N° CIN')
    x_num_fiscal = fields.Char('N° identification fiscale')
    x_num_cnss = fields.Char('N° CNSS')

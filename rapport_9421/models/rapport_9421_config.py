from odoo import models, fields


class Rapport9421Config(models.Model):
    _name = 'rapport.9421.config'
    _description = 'Configuration Rapport 9421'
    _rec_name = 'company_id'

    company_id = fields.Many2one(
        'res.company',
        string='Societe',
        required=True,
        default=lambda self: self.env.company,
    )

    # Codes des rubriques salariales — adaptés à "Ma Structure Salariale"
    code_salaire_brut = fields.Char(
        string='Code Salaire Brut',
        default='SBrut',          # ← corrigé
        required=True,
    )
    code_transport = fields.Char(
        string='Code Transport',
        default='TRANSPORT',
        required=True,
    )
    code_sbi = fields.Char(
        string='Code SBI',
        default='SBI',
        required=True,
    )
    code_cnss = fields.Char(
        string='Code CNSS',
        default='CNSS',
        required=True,
    )
    code_amo = fields.Char(
        string='Code AMO',
        default='AMO',
        required=True,
    )
    code_cimr = fields.Char(
        string='Code CIMR',
        default='CIMR',
        required=True,
    )
    code_frais_pro = fields.Char(
        string='Code Frais Professionnels',
        default='FRAIS_PROF',     # ← corrigé
        required=True,
    )
    code_sni = fields.Char(
        string='Code SNI',
        default='SNI',
        required=True,
    )
    code_irs_net = fields.Char(
        string='Code IR Net',
        default='IRS_NET',
        required=True,
    )
    code_sn = fields.Char(
        string='Code Salaire Net',
        default='SN',
        required=True,
    )
    code_exonere = fields.Char(
        string='Code Éléments Exonérés',
        default='EXONERE',
        required=True,
    )

    # Paramètres
    taux_frais_pro = fields.Float(
        string='Taux Frais Professionnels (%)',
        default=20.0,
        required=True,
    )
    jours_defaut = fields.Integer(
        string='Jours par defaut',
        default=26,
        required=True,
    )
    code_avantage = fields.Char(
    string='Code Avantages en Nature',
    default='AVANTAGE',
    required=True,
)

    # Code de la structure salariale ciblée
    code_structure = fields.Char(
        string='Code Structure Salariale',
        default='Ref_001',        # ← nouveau : filtre sur "Ma Structure Salariale"
        required=True,
        help='Code de la structure salariale à utiliser pour ce rapport',
    )

    def get_codes(self):
        self.ensure_one()
        return {
            'SBRUT':     self.code_salaire_brut,
            'TRANSPORT': self.code_transport,
            'SBI':       self.code_sbi,
            'CNSS':      self.code_cnss,
            'AMO':       self.code_amo,
            'CIMR':      self.code_cimr,
            'FRAIS_PRO': self.code_frais_pro,
            'SNI':       self.code_sni,
            'IRS_NET':   self.code_irs_net,
            'SN':        self.code_sn,
            'EXONERE':   self.code_exonere,
            'AVANTAGE':  self.code_avantage,
        }

    @classmethod
    def get_for_company(cls, env, company_id):
        config = env['rapport.9421.config'].search(
            [('company_id', '=', company_id)], limit=1
        )
        if not config:
            config = env['rapport.9421.config'].new({
                'company_id': company_id,
            })
        return config
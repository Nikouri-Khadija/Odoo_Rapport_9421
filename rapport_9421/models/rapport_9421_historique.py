from odoo import models, fields, api


class Rapport9421Historique(models.Model):
    """
    Historique des generations du rapport 9421.
    Chaque generation est tracee avec son auteur, sa date et le PDF produit.
    """
    _name = 'rapport.9421.historique'
    _description = 'Historique Rapport 9421'
    _order = 'date_generation desc'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
    )
    annee = fields.Integer(string='Annee', required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Societe',
        required=True,
    )
    date_generation = fields.Datetime(
        string='Date de generation',
        default=fields.Datetime.now,
        readonly=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Genere par',
        default=lambda self: self.env.user,
        readonly=True,
    )
    nb_employes = fields.Integer(
        string='Nombre d\'employes',
        readonly=True,
    )
    attachment_id = fields.Many2one(
        'ir.attachment',
        string='Fichier PDF',
        readonly=True,
        ondelete='set null',
    )
    state = fields.Selection(
        [('ok', 'Succes'), ('error', 'Erreur')],
        string='Statut',
        default='ok',
        readonly=True,
    )
    error_message = fields.Text(
        string='Message d\'erreur',
        readonly=True,
    )

    @api.depends('annee', 'company_id')
    def _compute_name(self):
        for rec in self:
            rec.name = 'Etat 9421 - %s - %s' % (
                rec.annee or '', rec.company_id.name or ''
            )

    def action_telecharger(self):
        """Ouvre le PDF genere."""
        self.ensure_one()
        if not self.attachment_id:
            return
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%d?download=true' % self.attachment_id.id,
            'target': 'new',
        }

    @api.model
    def enregistrer_generation(self, annee, company_id, nb_employes, attachment_id):
        """Cree une entree d'historique apres une generation reussie."""
        return self.create({
            'annee': annee,
            'company_id': company_id,
            'nb_employes': nb_employes,
            'attachment_id': attachment_id,
            'state': 'ok',
        })

    @api.model
    def enregistrer_erreur(self, annee, company_id, message):
        """Cree une entree d'historique pour une generation en echec."""
        return self.create({
            'annee': annee,
            'company_id': company_id,
            'state': 'error',
            'error_message': message,
        })

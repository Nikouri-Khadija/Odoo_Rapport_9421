import base64
from odoo import models, fields
from odoo.exceptions import UserError


class Wizard9421(models.TransientModel):
    _name = 'wizard.rapport.9421'
    _description = 'Assistant Generation Rapport 9421'

    annee = fields.Integer(
        string='Annee',
        required=True,
        default=lambda self: fields.Date.today().year,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Societe',
        required=True,
        default=lambda self: self.env.company,
    )

    def action_generer_rapport(self):
        self.ensure_one()

        # --- 1. Calcul des donnees metier ---
        try:
            data = self.env['rapport.9421.service'].calculer_donnees_rapport(
                annee=self.annee,
                company_id=self.company_id.id,
            )
        except UserError:
            raise
        except Exception as e:
            self.env['rapport.9421.historique'].enregistrer_erreur(
                self.annee, self.company_id.id, str(e)
            )
            raise UserError('Erreur lors du calcul des donnees : %s' % str(e))

        # --- 2. Rendu HTML via ir.qweb (Odoo 18) ---
        try:
            html_bytes = self.env['ir.qweb']._render(
                'rapport_9421.report_9421_template',
                {'data': data},
            )
            html_content = html_bytes if isinstance(html_bytes, str) else html_bytes.decode('utf-8')
        except Exception as e:
            self.env['rapport.9421.historique'].enregistrer_erreur(
                self.annee, self.company_id.id, str(e)
            )
            raise UserError('Erreur lors du rendu HTML : %s' % str(e))

        # --- 3. Conversion HTML -> PDF ---
        # En Odoo 18, _run_wkhtmltopdf retourne directement les bytes (pas un tuple)
        try:
            result = self.env['ir.actions.report']._run_wkhtmltopdf([html_content])
            pdf_content = result[0] if isinstance(result, (list, tuple)) else result
        except Exception as e:
            self.env['rapport.9421.historique'].enregistrer_erreur(
                self.annee, self.company_id.id, str(e)
            )
            raise UserError('Erreur lors de la conversion PDF : %s' % str(e))

        # --- 4. Stockage en piece jointe ---
        filename = 'etat_9421_%s_%s.pdf' % (self.annee, self.company_id.id)
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        # --- 5. Historique ---
        self.env['rapport.9421.historique'].enregistrer_generation(
            annee=self.annee,
            company_id=self.company_id.id,
            nb_employes=len(data['employees']),
            attachment_id=attachment.id,
        )

        # --- 6. Telechargement ---
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%d?download=true' % attachment.id,
            'target': 'new',
        }
from odoo import models, fields, api
class AnnulerRenderVousWizards(models.TransientModel):
      _name = "cancel.rendervous.wizard"
      _description = "Annuler Render-vous"

      patient_id = fields.Many2one('clinique.patient', string='Patient')

      def action_annuler(self):
            return
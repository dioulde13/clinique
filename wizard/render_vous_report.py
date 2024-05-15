from odoo import api, fields, models


class RenderVousReportWizard(models.TransientModel):
    _name = "render_vous.report.wizard"
    _description = "Print Rendez-vous Wizard"

    patient_id = fields.Many2one('clinique.patient', string="Patient")
    date_debut = fields.Date(string="Date debut")
    date_fin = fields.Date(string="Date fin")

    def action_report(self):
        appointements = self.env['clinique.rendez_vous'].search([
            ('patient_id', '=', self.patient_id.id),
            ('date', '>=', self.date_debut),
            ('date', '<=', self.date_fin)
        ])
        appointment_list = []
        for appointement in appointements:
            vals = {
                'patient_name': appointement.patient_id.name,
                'ref_patient': appointement.patient_id.reference,
                'date_rendez_vous': appointement.date,
                'ref_rendez_vous': appointement.reference,
                'date_debut': self.date_debut,
                'date_fin': self.date_fin
            }
            appointment_list.append(vals)

        data = {
            'form_data': self.read()[0],
            'appointements': appointment_list
        }
        print(data)
        return self.env.ref('clinique.action_report_appointement').report_action(self, data=data)

# def action_report(self):
#     domain = []
#     if self.patient_id:
#         domain.append(('patient_id', '=', self.patient_id.id))
#     if self.date_debut and self.date_fin:
#         domain.append(('date', '>=', self.date_debut))
#         domain.append(('date', '<=', self.date_fin))
#     elif self.date_debut:
#         domain.append(('date', '>=', self.date_debut))
#     elif self.date_fin:
#         domain.append(('date', '<=', self.date_fin))
#
#     appointments = self.env['clinique.rendez_vous'].search(domain)
#
#     appointment_list = []
#     for appointment in appointments:
#         vals = {
#             'name': appointment.name
#         }
#         appointment_list.append(vals)
#
#     data = {
#         'form_data': self.read()[0],
#         'appointments': appointment_list
#     }
#
#     print(data)

# return self.env.ref('clinique.action_report_appointement').report_action(self, data=data)

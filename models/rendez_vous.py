# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CLiniqueRendezVous(models.Model):
    _name = 'clinique.rendez_vous'
    _description = 'Patient Rendez-vous'
    _inherit = ['mail.thread']


    name = fields.Char(string='Rendez-vous', tracking=True)
    patient_id = fields.Many2one('clinique.patient', string='Patient')
    date = fields.Datetime(string='Date')
    reference = fields.Char(string='Reference')
    duree = fields.Integer(string='Durée (en heures)')
    user_id = fields.Many2one('res.users', string='Médecin', default=lambda self: self.env.user.id, readonly=True)
    motif = fields.Text(string='Motif')
    remarques = fields.Text(string='Remarques')
    code = fields.Char(string='Code de sécurité')



    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('clinique.rendez_vous')
        return super(CLiniqueRendezVous, self).create(vals)
    #
    # def action_send_email(self):
    #     template = self.env.ref('clinique.rendez_vous_mail_templete')
    #     res_id = self.id
    #     print(res_id)
    #     email_values = {
    #         'subject': 'Test',
    #         'email_from': 'baldedioulde992@gmail.com',
    #         'email_to': 'baldedioulde992@gmail.com',
    #     }
    #     template.send_mail(res_id, force_send=True, email_values=email_values)

    # def action_send_email(self):
    #     users = self.env['clinique.rendez_vous'].sudo().search([]).mapped('user_id')
    #     for user in users:
    #         appointments = self.env['clinique.rendez_vous'].sudo().search([('user_id', '=', user.id)])
    #         template_id = self.env.ref('clinique.rendez_vous_mail_templete')
    #         for appointment in appointments:
    #             template_id.send_mail(appointment.id, force_send=True)
    # def action_send_email(self):
    #     users = self.env['clinique.rendez_vous'].sudo().search([]).mapped('user_id')
    #     print(users)
    #     template_id = self.env.ref('clinique.rendez_vous_mail_templete')
    #     for user in users:
    #         appointments = self.env['clinique.rendez_vous'].search([('user_id', '=', user.id)])
    #         for appointment in appointments:
    #                 template_id.send_mail(appointment.id, force_send=True)
    def action_send_email(self):
        users = self.env['clinique.rendez_vous'].sudo().search([]).mapped('user_id')
        template_id = self.env.ref('clinique.rendez_vous_mail_templete')
        for user in users:
            appointments = self.env['clinique.rendez_vous'].search([('user_id', '=', user.id)])
            for appointment in appointments:
                # Send the email using the template
                mail_id = template_id.send_mail(appointment.id, force_send=True)
                # Add custom headers to the mail
                mail = self.env['mail.mail'].browse(mail_id)
                mail.write({
                    'headers': {
                        'X-Confidentiality': 'Confidential'  # Custom header
                    }
                })
                mail.send()


    # def action_send_email(self):
    #     template_id = self.env.ref('clinique.rendez_vous_mail_templete')
    #     sender_email = self.user_id.email
    #     print(sender_email)
    #     recipient_emails = 'baldedioulde992@gmail.com'
    #
    #     # Envoyer l'e-mail avec les adresses définies
    #     template_id.send_mail(self.id, force_send=True, email_values={'email_to': ','.join(recipient_emails), 'email_from': sender_email})

    # def action_send_email(self):
    #         template = self.env.ref('clinique.rendez_vous_mail_templete')
    #         res_id = self.id<
    #         email_values = {
    #             'subject': 'Test',
    #             'email_from': self.env.user.email,
    #             'email_to': self.patient_id.email,
    #         }
    #         template.send_mail(res_id, force_send=True, email_values=email_values)

    # def action_send_email(self):
    #         print("ddd 1")
    #         for attendee in self.user_id:
    #             print("ddd 1")
    #             ctx = {}
    #             email_list = [attendee.email]
    #             if email_list:
    #                 print("ddd 2")
    #                 ctx['email_to'] = ','.join([email for email in email_list if email])
    #                 print("ddd 3")
    #                 ctx['email_from'] = self.env.user.email
    #                 print("ddd 4")
    #                 ctx['attendee'] = attendee.name
    #                 print("ddd 5")
    #                 template = self.env.ref('clinique.rendez_vous_mail_templete')
    #                 print("ddd 6")
    #                 template.with_context(ctx).send_mail(self.id, force_send=True, raise_exception=False)
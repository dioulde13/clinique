# -*- coding: utf-8 -*-
from odoo import _, http
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request
from werkzeug.utils import redirect
from odoo.osv.expression import AND, OR


class WeblearnsPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        rtn = super(WeblearnsPortal, self)._prepare_home_portal_values(counters)
        current_user = request.env.user
        patient_count = request.env['clinique.patient'].search_count([('create_uid', '=', current_user.id)])
        rtn['patient_count'] = patient_count
        return rtn

    @http.route('/create/webpatient', website=True, auth='user')
    def create_patient(self, **kw):
        name = kw.get('name')
        adresse = kw.get('adresse')
        telephone = kw.get('telephone')
        email = kw.get('email')
        genre = kw.get('genre')
        date_naissance = kw.get('date_naissance')
        patient_vals = {
            'name': name,
            'genre': genre,
            'adresse': adresse,
            'telephone': telephone,
            'email': email,
            'date_naissance': date_naissance,
        }
        request.env['clinique.patient'].sudo().create(patient_vals)
        vals = {
            'page_name': 'patient_enregister',
        }
        return request.render("clinique.new_patient_form_portal", vals)

    @http.route('/modify/webpatient', type='http', auth='user', methods=['POST'], website=True)
    def modify_patient(self, **kw):
        vals = {'page_name': 'patient_list_view'}
        patient_id = kw.get('patient_id')
        if patient_id:
            patient = request.env['clinique.patient'].sudo().browse(int(patient_id))
            if patient.exists():
                patient.write({
                    'name': kw.get('name'),
                    'genre': kw.get('genre'),
                    'adresse': kw.get('adresse'),
                    'telephone': kw.get('telephone'),
                    'email': kw.get('email'),
                    'date_naissance': kw.get('date_naissance'),
                })
                vals.update({'patient': patient})
                vals['success_message'] = "Le patient a été modifié avec succès."
        return redirect('/my/patient')

    @http.route('/new/patient', website=True, auth='user')
    def enregistrerPatient(self, **kw):
        vals = {
            'page_name': 'patient_enregister',
        }
        return request.render("clinique.new_patient_form_portal", vals)

    @http.route(['/my/patient', '/my/patient/page/<int:page>'], type='http', auth="user", website=True)
    def patient_list(self, search=None, search_in=None, **kw):

        searchbar_inputs = self._ticket_get_searchbar_inputs()

        if not search_in:
            search_in = "all"
        if search:
           domain += self._ticket_get_search_domain(search_in, search)

        domain = AND(
            [
                domain,
                request.env["ir.rule"]._compute_domain(helpdesk_ticket._name, "read"),
            ]
        )

        recruitment = request.env['clinique.patient'].sudo().search(search_domain)
        return request.render('clinique.wb_patient_list_view_portal', {
            'patients': recruitment,
            'page_name': 'patient_list_view',
            'search': search,
            'search_in': search_in,
        })

    def _ticket_get_searchbar_inputs(self):
        values = {
            "all": {"input": "all", "label": _("Rechercher dans tout"), "order": 1},
            "number": {
                "input": "reference",
                "label": _("Recherche par reference"),
                "order": 2,
            },
            "name": {
                "input": "name",
                "label": _("Recherche par titre"),
                "order": 3,
            },
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))


    # @http.route(['/my/patient', '/my/patient/page/<int:page>'], type='http', auth="user", website=True)
    # def patient_list(self, page=1, **kw):
    #     patient_obj = request.env['clinique.patient']
    #     total_patient = patient_obj.search_count([])
    #     page_detail = pager(
    #         url='my/patient',
    #         total = total_patient,
    #         page=page,
    #         step=2
    #     )
    #     patient = patient_obj.search([], limit=2, offset=page_detail['offset'])
    #     vals = {'patient': patient, 'page_name':'patient_list_view', 'pager':page_detail}
    #     return request.render("clinique.wb_patient_list_view_portal", vals)

    # @http.route(['/my/patient', '/my/patient/page/<int:page>'], type='http', auth="user", website=True)
    # def list_patients(self, page=1, sortby='id', search='', search_in='All', **kw):
    #     sorted_list = {
    #         'id': {'label': 'ID Desc', 'order': 'id desc'},
    #         'name': {'label': 'Name', 'order': 'name asc'},
    #     }
    #
    #     search_list = {
    #         'All': {'label': 'All', 'input': 'all', 'domain': []},
    #         'name': {'label': 'Name', 'input': 'name', 'domain': [('name', 'ilike', search)]},
    #     }
    #     search_domain = search_list[search_in]['domain']
    #     default_order_by = sorted_list[sortby]['order']
    #
    #     patient_obj = request.env['clinique.patient']
    #     current_user = request.env.user
    #     domain = [('create_uid', '=', current_user.id)]
    #     total_patient = patient_obj.search_count(search_domain)
    #
    #     # Pagination details
    #     pager = request.website.pager(
    #         url='/my/patient',
    #         total=total_patient,
    #         page=page,
    #         url_args={'sortby': sortby},
    #     )
    #     patients = patient_obj.search(domain, order=default_order_by, offset=pager['offset'])
    #     vals = {
    #         'patients': patients,
    #         'page_name': 'patient_list_view',
    #         'pager': pager,
    #         'sortby': sortby,
    #         'searchbar_sortings': sorted_list,
    #         'search_in': search_in,
    #         'search': search,
    #     }
    #     return request.render("clinique.wb_patient_list_view_portal", vals)

    @http.route(['/my/patient/<model("clinique.patient"):patient_id>'], type='http', website=True)
    def patientsFormView(self, patient_id, **kw):
        vals = {"patient": patient_id, 'page_name': 'patient_form_view'}
        patient_records = request.env['clinique.patient'].search([]).ids
        patient_ids = patient_records
        patient_index = patient_ids.index(patient_id.id)

        if patient_index > 0:  # Assurez-vous que l'index est supérieur à 0
            vals['prev_record'] = '/my/patient/{}'.format(patient_ids[patient_index - 1])
        if patient_index < len(patient_ids) - 1:  # Assurez-vous que l'index est dans les limites
            vals['next_record'] = '/my/patient/{}'.format(patient_ids[patient_index + 1])

        return request.render("clinique.wb_patient_form_view_portal", vals)

# class Clinique(http.Controller):
#     @http.route('/hospital/patient', website=True, auth='user')
#     def hospital_patient(self, **kw):
#         return request.render("clinique.patient_page", {})
#
#     @http.route('/create/webpatient', website=True, auth='user')
#     def create_patient(self, **kw):
#         request.env['clinique.patient'].sudo().create(kw)
#         return request.render("clinique.patient_confirmation_page", {})

from crypt import methods

from odoo import http
from odoo.http import request, Controller, route
import json
import logging

from odoo.odoo import fields

_logger = logging.getLogger(__name__)

class Controller(http.Controller):

    @route('/mon/school/liste_classe', auth='public', website=True)
    def listes_classes(self, **kwargs):
        classes = request.env['school.classe'].search([])
        classes_list = []
        for classe in classes:
            classes_list.append({
                'id': classe.id,
                'Niveau': classe.vcClasse,
            })
        return request.make_response(json.dumps(classes_list), headers={'Content-Type': 'application/json'})

    @http.route('/api/school/supprimer_classe', type='json', auth='public', methods=['POST'], csrf=False)
    def supprimer_classe(self, **kwargs):
        classe_id = kwargs.get('id')
        if not classe_id:
            return {
                "success": 400,
                "message": "ID de la classe manquant"
            }
        classe = request.env['school.classe'].sudo().search([('id', '=', classe_id)])
        if not classe:
            return {
                "success": 404,
                "message": "La classe avec l'ID {} n'a pas été trouvée".format(classe_id)
            }
        classe_name = classe.vcClasse
        print(classe_name)
        classe.sudo().unlink()
        return {
            "success": 200,
            "id": classe_id,
            "message": "La classe {} a été supprimée avec succès".format(classe_name)
        }

    @http.route('/api/school/classe', type='json', auth='public', methods=['POST'], csrf=False)
    def create_classe(self, **kwargs):
        try:
            vcClasse = kwargs.get('vcClasse')
            classe = request.env['school.classe'].sudo().create({'vcClasse': vcClasse,})
            return {
                'status': 200,
                'Classe_id': classe.id,
                'Classe_nom': classe.vcClasse,
                'Compagny': classe.company_id.name,
                'message': 'Classe créé avec succès'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    @http.route('/api/school/create_parent', type='json', auth='public', method=['POST'], csrt=False)
    def create_parent(self, **kwargs):
        try:
            vcNom = kwargs.get('vcNom')
            vcPrenom = kwargs.get('vcPrenom')
            vcAdresse = kwargs.get('vcAdresse')
            vcTelephone = kwargs.get('vcTelephone')
            vcCodeParent = kwargs.get('vcCodeParent')

            parent = request.env['school.parent'].sudo().create({
                'vcNom': vcNom,
                'vcPrenom': vcPrenom,
                'vcAdresse': vcAdresse,
                'vcTelephone': vcTelephone,
                'vcCodeParent': vcCodeParent,
            })
            return {
                "status": 200,
                "Id": parent.id,
                "Nom": parent.vcNom,
                "Prenom": parent.vcPrenom,
            }
        except Exception as e:
          return {
            'status': 'error',
            'message': str(e)
           }
    @route('/api/school/liste_parent', auth='public', website=True)
    def liste_parent(self, **kwargs):
        parents = request.env['school.parent'].search([])
        liste_parent = []
        for parent in parents:
            liste_parent.append({
                'id': parent.id,
                'Nom': parent.vcNom,
                'Prenom': parent.vcPrenom,
                'Adresse': parent.vcAdresse,
                'Telephone': parent.vcTelephone,
                'Code parent': parent.vcCodeParent,
                'Etablissement': parent.company_id.name,
            })
        return request.make_response(json.dumps(liste_parent), headers={'Content-Type': 'application/json'})

    @http.route('/api/school/liste_facture', auth='public', website=True)
    def liste_facture(self):
        factures = request.env['account.move'].sudo().search([])
        print(factures)
        liste_facture = []
        for facture in factures:
            liste_facture.append({
                'id': facture.id,
                'name': facture.name,
                'amount_total': facture.amount_total,
                'state': facture.state,
                'date': str(facture.invoice_date)
            })

        return request.make_response(
            json.dumps(liste_facture),
            headers={'Content-Type': 'application/json'}
        )

    @http.route('/api/school/liste_produit', auth='public', website=True)
    def liste_produit(self):
        produits = request.env['product.template'].search([])
        produit_data = [
            {
                'id': produit.id,
                'name': produit.name,
                "Prix d'achat": produit.standard_price,
                'Prix de vente': produit.list_price,
            }
            for produit in produits
        ]
        print(produit_data)
        return request.make_response(json.dumps(produit_data), headers=[('Content-Type', 'application/json')])

    @http.route('/api/school/create_facture', type='json', auth='user', methods=['POST'], csrf=False)
    def create_facture(self, **kwargs):
        try:
            if not request.session.uid:
                return {'error': 'Session expirée. Veuillez vous reconnecter.'}

            user_id = request.env.user.id
            partner_id = kwargs.get('partner_id')
            invoice_date = kwargs.get('invoice_date')
            line_items = kwargs.get('line_items', [])

            if not partner_id or not line_items:
                return {'error': 'Les champs "partner_id" et "line_items" sont obligatoires.'}

            nouveau_facture = request.env['account.move'].sudo().create({
                'partner_id': partner_id,
                'move_type': 'out_invoice',
                'invoice_date': invoice_date,
                'invoice_user_id': user_id,
                'invoice_line_ids': [(0, 0, {
                    'product_id': line.get('product_id'),
                    'quantity': line.get('quantity', 1),
                    # 'price_unit': line.get('price_unit', 0.0),
                    # 'name': line.get('name', 'Description par défaut'),
                }) for line in line_items]
            })

            nouveau_facture.sudo().action_post()

            return {'success': True, 'facture_id': nouveau_facture.id}

        except http.SessionExpiredException:
            return {'error': 'Session expirée. Veuillez vous reconnecter.'}
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/school/supprimer_facture', type='json', auth='user', methods=['POST'], csrf=False)
    def supprimer_facture(self, **kwargs):
        facture_id = kwargs.get('id')
        if not facture_id:
            return {
                "success": 400,
                "message": "ID de la facture manquant"
            }

        facture = request.env['account.move'].sudo().search([('id', '=', facture_id)])
        if not facture.exists():
            return {
                "success": 404,
                "message": f"La facture avec l'ID {facture_id} n'a pas été trouvée"
            }

        facture_name = facture.name
        facture.sudo().unlink()

        return {
            "success": 200,
            "id": facture_id,
            "message": f"La facture {facture_name} a été supprimée avec succès"
        }

    @http.route('/api/school/pay_facture', type='json', auth='user', methods=['POST'], csrf=False)
    def pay_facture(self, **kwargs):
        try:
            if not request.session.uid:
                return {'error': 'Session expirée. Veuillez vous reconnecter.'}

            facture_reference = kwargs.get('facture_reference')
            montant = float(kwargs.get('montant', 0))

            if not facture_reference or montant <= 0:
                return {
                    'error': 'Les champs "facture reference" et "montant" sont obligatoires et doivent être valides.'
                }
            facture = request.env['account.move'].sudo().search(
                [('name', '=', facture_reference), ('state', '=', 'posted')], limit=1)

            if not facture:
                return {'error': 'Facture introuvable ou déjà payée.'}

            paiement_vals = {
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': facture.partner_id.id,
                'amount': montant,
                'date': fields.Date.today(),
                'journal_id': request.env['account.journal'].sudo().search([('type', '=', 'bank')], limit=1).id,
                'payment_method_id': request.env.ref('account.account_payment_method_manual_in').id,
            }

            paiement = request.env['account.payment'].sudo().create(paiement_vals)

            # Valider le paiement
            paiement.action_post()

            # Réconciliation : Associer les bonnes lignes comptables
            # Sélectionner les lignes de facture non réconciliées et appartenant aux comptes clients
            facture_moves = facture.line_ids.filtered(
                lambda l: l.account_id.user_type_id.name in ['Receivable'] and not l.reconciled
            )

            # Sélectionner les lignes du paiement qui sont associées au compte client
            paiement_moves = paiement.move_id.line_ids.filtered(
                lambda l: l.account_id.user_type_id.name in ['Receivable'] and not l.reconciled
            )

            # Réconcilier les lignes sélectionnées
            (facture_moves + paiement_moves).reconcile()

            return {'success': True, 'payment_id': paiement.id, 'facture_id': facture.id}

        except http.SessionExpiredException:
            return {'error': 'Session expirée. Veuillez vous reconnecter.'}
        except Exception as e:
            return {'error': str(e)}

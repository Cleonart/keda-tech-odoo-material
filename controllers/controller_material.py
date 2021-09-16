# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import requests


class ControllerApiMaterial(http.Controller):
    """Material API Controller"""

    @http.route(['/api/v1/materials',
                '/api/v1/materials/id/<int:id>',
                 '/api/v1/materials/type/<string:type>'], type="http", auth="public")
    def api_material_list(self, id=False, type=False):
        """ Return the list of materials 
            @endpoint /api/v1/materials - Getting all materials
            @endpoint /api/v1/materials/id/{id} - Getting specific material with id
            @endpoint /api/v1/materials/type/{type} - Getting materials with specifik material type """

        # Filter Data
        filter = []
        record = []

        # Filtering Material according to material type
        if not id and type:
            filter.append(('type', '=', type))

        # Filtering Material accodring to id
        if id and not type:
            filter.append(('id', '=', id))

        # Return all record when there's no filter
        res = request.env['materials.material'].sudo().search(filter)
        record = [{
            'id': data.id,
            'name': data.name,
            'type': data.type,
            'buy_price': data.buy_price,
            'supplier': data.supplier.id,
            'supplier_name': data.supplier.name
        } for data in res]

        return json.dumps(record)

    @http.route(['/api/v1/materials/mutation'], csrf=False, type="http", auth="public")
    def api_material_mutation(self, **kwargs):
        """ Do a mutation to database 
            only root and administrator is allowed """
        print("**************** MUTATING ELEMEN *****************")

        # Mutate Edit
        if not kwargs.get("id") == "":
            res = request.env['materials.material'].sudo()
            res = res.api_update({
                'id': int(kwargs.get('id')),
                'name': kwargs.get('name'),
                'type': kwargs.get('type'),
                'buy_price': int(kwargs.get('buy_price')),
                'supplier': int(kwargs.get('supplier'))
            })
            return json.dumps(res)

        res = request.env['materials.material'].api_create({
            'name': kwargs.get('name'),
            'type': kwargs.get('type'),
            'buy_price': int(kwargs.get('buy_price')),
            'supplier': int(kwargs.get('supplier'))
        })

        return json.dumps(res)

class ControllerActionMaterial(ControllerApiMaterial):
    """ Controlling Button Action in Material """

    def material_action_update(self, **kwargs):
        res = (self.api_material_mutation(**kwargs))
        return res
        
    def material_action_delete(self, **kwargs):
        return (self.api_material_mutation(**kwargs))

class ControllerUiMaterial(ControllerActionMaterial):

    @http.route(['/materials/new',
                 '/materials/edit/<int:id>'], csrf=False, methods=['GET', 'POST'], website=True, auth="public")
    def material_form(self, **kwargs):
            
        # All of this fields will be ignored
        ignore_fields = ['display_name', 'create_uid',
                         'create_date', 'write_uid', 'write_date', '__last_update']
        error = []
        method = str(request.httprequest.method)
        print(method)

        if method == 'POST':        
            trs = self.material_action_update(**kwargs)
            print(json.loads(trs.data))
            error = json.loads(trs.data)
        
        id = kwargs.get('id')

        # Map Fields to new dictionary
        material = request.env['materials.material'].sudo()
        fields = {
            field: "" for field in material._fields if field not in ignore_fields}

        # Get corresponding data if id is exists
        if id:
            material = material.search([('id', '=', id)])
            if material:
                fields['id'] = material.id
                fields['name'] = material.name
                fields['type'] = material.type
                fields['buy_price'] = material.buy_price
                fields['supplier'] = material.supplier.id
            else:
                error.append({
                    'msg': "Data with corresponding id of {} is not exists".format(id),
                    "code": "MATERIAL_NOT_EXISTS"
                })

        # Get supplier data for the dropdown
        supplier = request.env['materials.supplier'].sudo().search([])

        # Return the website pages [views/material/form.xml]
        return request.render("material_management_module.material_form",
                              {'material': fields,
                               'supplier': supplier,
                               'error': error})


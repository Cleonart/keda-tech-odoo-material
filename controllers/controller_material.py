# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class Material(http.Controller):
    
    @http.route('/materials', website=True, auth='public')
    def material_route(self, **kw):
        record = request.env['materials.material'].search([])
        record_json = []
        for row in record:
            record_json.append({
                'id' : row.id,
                'name' : row.name,
                'type' : row.type,
                'supplier' : row.supplier.id
            })
        return json.dumps(record_json)
    
    @http.route('/materials/new', website=True, auth="public")
    def material_create(self, **kwargs):
        return "tes"
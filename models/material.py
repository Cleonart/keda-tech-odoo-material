# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MaterialData(models.Model):
    _name = "materials.material"
    _description = "Material Detail"

    name = fields.Char(string="Material Name",
                       required=True)

    type = fields.Selection(string="Material Type",
                            required=True,
                            selection=[("fabric", "Fabric"),
                                       ("jeans", "Jeans"),
                                       ("cotton", "Cotton")])

    buy_price = fields.Integer(string="Material Buy Price",
                               required=True)

    supplier = fields.Many2one("materials.supplier",
                               string="Choose Supplier",
                               required=True)

    # Check if buy_price is more
    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError("Buy price should beyond 100")
    
    def validate(self, vals):
        error = []
        
        if not vals.get('name'):
            error.append({'msg': "Material Name is not exists",
                         "code": "MATERIAL_NAME_NOT_FOUND"})
        if not vals.get('type'):
            error.append({'msg': "Material Type is not exists",
                         "code": "MATERIAL_TYPE_NOT_FOUND"})
        if not vals.get('buy_price'):
            error.append({'msg': "Buy Price is not exists",
                         "code": "MATERIAL_BUY_PRICE_NOT_FOUND"})
        elif vals.get('buy_price') <= 100:
            error.append({'msg': "Buy Price should more than 100",
                         "code": "MATERIAL_BUY_PRICE_LESS_THAN_100"})
        if not vals.get('supplier'):
            error.append({'msg': "Supplier is not exists",
                         "code": "SUPPLIER_NOT_FOUND"})
        return error
        
    def api_create(self, vals):
        """ Creating Data via API endpoint """
        error = super(MaterialData, self).validate()
        if len(error):
            return error
        res = super(MaterialData, self).create(vals)
        error.append({'msg': "Data Successfully Added", "code":"SUCCESS"})
        return error

    def api_update(self, vals):
        """ Creating Data via API endpoint """

        error = super(MaterialData, self).validate()
        if len(error):
            return error
        res = super(MaterialData, self).search([('id','=',vals.get('id'))])
        for record in res:
            record.write(vals)
            error.append({'msg': "Data Successfully Updated", "code":"SUCCESS"})
            return error

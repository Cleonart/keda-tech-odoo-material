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
    
    def go_to_material_controllers(self):
        print("tessss")
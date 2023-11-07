from odoo import fields, models, api, exceptions

class InheritEstateProperty(models.Model):
    _inherit = 'estate.property'

    def sell_prop(self):
        print("It works!")
        return super().sell_prop()
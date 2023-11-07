from odoo import fields, models, api, exceptions

class InheritEstateProperty(models.Model):
    _inherit = 'estate.property'

    def sell_prop(self):
        raise exceptions.UserError("Works")
        return super().sell_prop()
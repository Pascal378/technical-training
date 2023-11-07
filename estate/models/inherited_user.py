from odoo import fields, models


class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesmen_id",
                                   domain="[('state', '!=', 'sold'),('state','!=','cancelled')]")

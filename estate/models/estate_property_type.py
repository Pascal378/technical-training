from odoo import fields, models


class PropertyType(models.Model):
    _name ='estate.property.type'

    name = fields.Char()
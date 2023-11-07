from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Types of properties'
    _sql_constraints = [
        ('unique_type_name',
         'unique(name)',
         'Type name must be unique'
         )
    ]
    _order = "name"

    name = fields.Char()
    property_ids = fields.One2many("estate.property", "property_type_id")

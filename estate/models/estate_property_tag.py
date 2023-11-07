from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for properties"
    _sql_constraints = [
        ('unique_tag_name',
         'unique(name)',
         'Tag name must be unique'
         )
    ]

    name = fields.Char()

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property Management"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=3),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'),
                                                     ('south', 'South'),
                                                     ('west', 'West'),
                                                     ('east', 'East')])
    active = fields.Boolean(default=True)

    state = fields.Selection(selection=[('new', 'New'),
                                        ('offer received', 'Offer received'),
                                        ('offer accepted', 'Offer accepted'),
                                        ('sold', 'Sold')
                                        ])



from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property Management"
    _sql_constraints = [
        (
            'positive_expected_price',
            'CHECK(expected_price >= 0)',
            'Only positive values are allowed for expected price'
        ),
        ('positive_selling_price',
         'CHECK(selling_price >= 0)',
         'Only positive values are allowed for selling price'
         )
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('north', 'North'),
                                                                                  ('south', 'South'),
                                                                                  ('west', 'West'),
                                                                                  ('east', 'East')])
    active = fields.Boolean(string="Active", default=True)

    state = fields.Selection(selection=[('new', 'New'),
                                        ('offer received', 'Offer received'),
                                        ('offer accepted', 'Offer accepted'),
                                        ('sold', 'Sold'),
                                        ('cancelled', 'Cancelled')
                                        ], string="Status")

    property_type_id = fields.Many2one("estate.property.type")

    salesmen_id = fields.Many2one('res.users', string="Salesmen", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_total_area")
    best_offer = fields.Float(compute="_best_offer")

    @api.depends("garden_area", "living_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _best_offer(self):
        best = 0
        for record in self:
            for offer in record.offer_ids:
                if best < offer.price:
                    best = offer.price
            record.best_offer = best

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = False

    def sell_prop(self):
        if self.state == 'cancelled':
            raise exceptions.UserError("Can't sell a cancelled property.")
        else:
            self.state = 'sold'

    def cancel_prop(self):
        if self.state == 'sold':
            raise exceptions.UserError("Can't cancel a sold property.")
        else:
            self.state = 'cancelled'

    @api.ondelete(at_uninstall=False)
    def _unlink_if_NewOrCancelled(self):
        for record in self:
            if record.state != "new" and record.state != "cancelled":
                raise exceptions.UserError("You can only delete new or cancelled properties")

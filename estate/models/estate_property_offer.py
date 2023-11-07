from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for properties"
    _sql_constraints = [
        ('positive_selling_price',
         'CHECK(price >= 0)',
         'Only positive values are allowed for offer price'
         )
    ]

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'),
                                                     ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_validity", inverse="_inverse_validity")

    @api.depends("create_date", "validity")
    def _validity(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)


    def _inverse_validity(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def accept_offer(self):
        if not self.property_id.buyer_id:
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
        else:
            raise exceptions.UserError("You can only accept one offer per property")

        return True

    def refuse_offer(self):
        if self.status == 'accepted':
            self.status = 'refused'
            self.property_id.selling_price = False
            self.property_id.buyer_id = False
        else:
            self.status = 'refused'

        return True

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for properties"

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
                record.validity = (record.create_date.date() - record.date_deadline).days
            else:
                record.validity = (fields.Date.today() - record.date_deadline).days

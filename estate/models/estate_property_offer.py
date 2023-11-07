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
    date_deadline = fields.Date(compute="_validity",inverse="_inverse_validity")

    @api.depends("create_date", "validity")
    def _validity(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    @api.depends("create_date", "validity")
    def _inverse_validity(self):
        for record in self:
            if record.create_date:
                d1 = fields.datetime.strptime(str(self.create_date), '%Y-%m-%d')
                d2 = fields.datetime.strptime(str(self.date_deadline), '%Y-%m-%d')
                self.validity = int((d2-d1).days)
            else:
                d1 = fields.datetime.strptime(str(fields.Date.today), '%Y-%m-%d')
                d2 = fields.datetime.strptime(str(self.date_deadline), '%Y-%m-%d')
                self.validity = int((d2 - d1).days)
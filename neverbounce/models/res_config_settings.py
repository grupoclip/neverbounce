from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    neverbounce_api_key = fields.Char(string='NeverBounce API Key')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('partner_email_verification.neverbounce_api_key',
                                                         self.neverbounce_api_key)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['neverbounce_api_key'] = self.env['ir.config_parameter'].sudo().get_param(
            'partner_email_verification.neverbounce_api_key', default='')
        return res

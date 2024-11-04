from odoo import fields, models


class VerifiedEmail(models.Model):
    _name = 'verified.email'
    _description = 'Verified Email'

    email = fields.Char(required=True, unique=True)
    verification_status = fields.Selection(
        [('valid', 'Valid'), ('invalid', 'Invalid'), ('unknown', 'Unknown')],
        required=True
    )
    verification_date = fields.Datetime(string='Verification Date', default=fields.Datetime.now)
    flags = fields.Char(string='Flags')  # Stores flags as a comma-separated string
    suggested_correction = fields.Char(string='Suggested Correction')
    retry_token = fields.Char(string='Retry Token')
    execution_time = fields.Integer(string='Execution Time (ms)')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

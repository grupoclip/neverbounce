import requests
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_email_verified = fields.Boolean(string='Is Email Verified', default=False)

    def verify_email(self):
        verified_email_model = self.env['verified.email']

        for record in self:
            # Check if email is already verified
            verified_record = verified_email_model.search([('email', '=', record.email)], limit=1)
            if verified_record:
                record.is_email_verified = verified_record.verification_status == 'valid'
                continue

            # Retrieve the API key from the configuration
            api_key = self.env['ir.config_parameter'].sudo().get_param('partner_email_verification.neverbounce_api_key')
            if not api_key:
                raise ValueError("Please configure the NeverBounce API Key in the settings.")

            # Call the NeverBounce API
            url = f'https://api.neverbounce.com/v4/single/check?key={api_key}&email={record.email}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                verification_status = 'unknown'

                if data.get('result') == 'valid':
                    verification_status = 'valid'
                elif data.get('result') == 'invalid':
                    verification_status = 'invalid'

                # Save verification status with additional fields
                verified_email_model.create({
                    'email': record.email,
                    'verification_status': verification_status,
                    'flags': ', '.join(data.get('flags', [])),
                    'suggested_correction': data.get('suggested_correction', ''),
                    'retry_token': data.get('retry_token', ''),
                    'execution_time': data.get('execution_time', 0),
                })

                # Update the partner based on new verification status
                record.is_email_verified = verification_status == 'valid'
            else:
                record.is_email_verified = False

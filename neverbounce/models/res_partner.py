import requests
from odoo import fields, models
from odoo.exceptions import UserError

API_BASEURL = 'https://api.neverbounce.com/'
API_VERSION = 'v4.2'

API_URL = f'{API_BASEURL}{API_VERSION}'

API_ENDPOINT_SINGLE_CHECK = f'{API_URL}/single/check'
API_ENDPOINT_ACCOUNT_INFO = f'{API_URL}/account/info'


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
                if verified_record.verification_status == 'valid':
                    continue

            # Retrieve the API key from the configuration
            API_KEY = self.env['ir.config_parameter'].sudo().get_param('partner_email_verification.neverbounce_api_key')
            neverbounce = self.env['ir.config_parameter'].sudo().get_param('partner_email_verification.neverbounce')
            if not neverbounce:
                raise UserError("Please enable the NeverBounce Integration in the settings.")
            if not API_KEY:
                raise UserError("Please configure the NeverBounce API Key in the settings.")

            auth = requests.get(f'{API_ENDPOINT_ACCOUNT_INFO}?key={API_KEY}')
            if auth.status_code == 200:
                auth_data = auth.json()
                if auth_data.get('status') == 'auth_failure':
                    raise UserError("Invalid API Key - Authentication Failure")
            else:
                raise UserError("Invalid API Key - Unknown Error")

            # Call the NeverBounce API
            response = requests.get(f'{API_ENDPOINT_SINGLE_CHECK}?key={API_KEY}&email={record.email}')

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

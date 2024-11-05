import requests
from odoo import fields, models, _
from odoo.exceptions import UserError

API_BASEURL = 'https://api.neverbounce.com/'

API_ENDPOINT_SINGLE_CHECK = f'/single/check'
API_ENDPOINT_ACCOUNT_INFO = f'/account/info'


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
            neverbounce = self.env['ir.config_parameter'].sudo().get_param('partner_email_verification.neverbounce')
            neverbounce_api_key = self.env['ir.config_parameter'].sudo().get_param(
                'partner_email_verification.neverbounce_api_key')
            neverbounce_version = self.env['ir.config_parameter'].sudo().get_param(
                'partner_email_verification.neverbounce_version') or 'v4.2'
            if not neverbounce:
                raise UserError(_("Please enable the NeverBounce Integration in the settings."))
            if not neverbounce_api_key:
                raise UserError(_("Please configure the NeverBounce API Key in the settings."))

            account_info = requests.get(
                f'{API_BASEURL}{neverbounce_version}{API_ENDPOINT_ACCOUNT_INFO}?key={neverbounce_api_key}')
            if account_info.status_code == 200:
                account_info_data = account_info.json()
                if account_info_data.get('status') == 'auth_failure':
                    raise UserError(_("Invalid API Key - Authentication Failure"))
            else:
                raise UserError(_("Invalid API Key - Unknown Error"))

            # Call the NeverBounce API
            single_check = requests.get(
                f'{API_BASEURL}{neverbounce_version}{API_ENDPOINT_SINGLE_CHECK}?key={neverbounce_api_key}&email={record.email}')

            if single_check.status_code == 200:
                single_check_data = single_check.json()
                verification_status = 'unknown'

                if single_check_data.get('result') == 'valid':
                    verification_status = 'valid'
                elif single_check_data.get('result') == 'invalid':
                    verification_status = 'invalid'

                # Save verification status with additional fields
                verified_email_model.create({
                    'email': record.email,
                    'verification_status': verification_status,
                    'flags': ', '.join(single_check_data.get('flags', [])),
                    'suggested_correction': single_check_data.get('suggested_correction', ''),
                    'retry_token': single_check_data.get('retry_token', ''),
                    'execution_time': single_check_data.get('execution_time', 0),
                })

                # Update the partner based on new verification status
                record.is_email_verified = verification_status == 'valid'
            else:
                record.is_email_verified = False

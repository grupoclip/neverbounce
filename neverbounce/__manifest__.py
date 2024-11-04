{
    'name': 'NeverBounce - Partner Email Verification',
    'summary': """
       Partner Email Verification for Odoo integrates with NeverBounce to streamline email validation, helping businesses maintain clean, accurate customer data. With an easy-to-use verification button and configurable settings, this module reduces email bounce rates and enhances communication reliability by verifying customer emails directly in Odoo. Ideal for businesses seeking to improve data integrity and email deliverability.
   """,
    'description': """
    •	Email Verification Button: Verify customer emails directly on the res.partner form.
	•	NeverBounce Integration: Connects with NeverBounce API for real-time email validation.
	•	Cache Verified Emails: Saves verified email records to reduce redundant checks.
	•	Email Status Indicator: Shows email verification status in res.partner.
	•	Configurable API Key: Easily set the NeverBounce API key in Odoo settings.
	•	Bounce Rate Reduction: Helps maintain a clean, accurate customer email list.
   """,
    "author": "Victor Serrano",
    "website": "https://victor.lat",
    'category': 'Productivity',
    'version': '16.0.0.1',
    'depends': ['base', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/res_config_settings_view.xml',
    ],
    "images": ["static/description/banner.png"],
    "application": True,
    "installable": True,

    "license": "LGPL-3",
}

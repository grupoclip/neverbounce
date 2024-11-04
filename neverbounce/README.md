# Partner Email Verification with NeverBounce Integration

This Odoo 16 module integrates with the NeverBounce email verification service to validate customer email addresses directly from the Odoo platform. With this module, users can check the validity of emails, helping ensure accuracy and reduce bounce rates. The module stores verification details to avoid redundant API calls for previously checked addresses.

## Features

- **Email Verification**: Adds a "Verify Email" button on the `res.partner` form view to validate an email address through the NeverBounce API.
- **Cache Verified Emails**: Stores verified emails with their status and additional details in an internal model to reduce API calls.
- **Automatic Field Updates**: The module adds a field in `res.partner` to indicate whether the email has been verified. If the email is verified, the "Verify Email" button is hidden.
- **Configurable API Key**: The NeverBounce API key can be managed directly from Odoo's settings for easy configuration and updates.

## Technical Details

1. **Verification Status Storage**: Creates a new model, `verified.email`, which stores:
   - Email address
   - Verification status (valid, invalid, or unknown)
   - Verification flags (e.g., DNS checks)
   - Suggested correction, retry token, and execution time from the API response
2. **NeverBounce API Key Configuration**: The API key is configurable in `Settings` under a dedicated section, allowing easy updates without code changes.

## Installation

1. Place the module folder (`partner_email_verification`) into your Odoo custom addons directory.
2. Update the module list and install the module from the Apps menu.
3. Configure the NeverBounce API key in **Settings > General Settings > NeverBounce API Integration**.

## Usage

1. Go to **Contacts** and open any contact form.
2. If the email has not been verified, click the "Verify Email" button.
3. The email verification status and other details will be saved and can be referenced for future verification attempts.

## Dependencies

- Odoo 16
- An active NeverBounce API account and key

## License

This module is open for customization and distribution as per the terms specified in the license file.

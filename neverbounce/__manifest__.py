{
    'name': 'NeverBounce - Partner Email Verification',
    'summary': """
       Conexión con impresoras punto matriz/Forma Libre
   """,

    'description': """
       - Permite la conexión con impresoras punto matriz.
       - Permite la impresión de facturas.
       - Permite la division de facturas basado en el limite de lineas que permite una factura .
       - Permite la auto publicación de facturas.
   """,
    "author": "Konix C.A",
    "company": "Grupo Clip",
    "website": "https://victor.lat",
    'category': 'Accounting/Accounting',
    'version': '16.0.0.1',
    'depends': ['base'],
    'data': [
        'views/res_partner_view.xml',
        'views/res_config_settings_view.xml',
    ],
    "application": True,
    "installable": True,

    "license": "LGPL-3",
}

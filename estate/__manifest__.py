{
    "name": "Real Estate",  # The name that will appear in the App list
    "version": "17.0.0.4",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'views/inherited_user_views.xml'
    ],
    "installable": True,
    'license': 'LGPL-3',
}

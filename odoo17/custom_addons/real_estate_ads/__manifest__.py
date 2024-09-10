{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "https://www.bahromnajmiddinov.com",
    "author": "Bahrom Najmiddinov",
    "description": """
         Transform your real estate business with the Real Estate Ads app for Odoo. Designed to streamline the creation,
          management, and publication of property advertisements, this app integrates seamlessly with your existing 
          Odoo setup to enhance your property marketing efforts. Whether you’re handling residential, commercial, 
          or rental properties, our app offers the tools you need to efficiently manage and promote your listings.
    """,
    "category": "Sales",
    'depends': ['mail'],
    "data": [
        # groups
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "security/model_access.xml",

        "views/menu_items.xml",
        "views/properties.xml",
        "views/property_type.xml",
        "views/property_type_tag.xml",
        "views/property_offer.xml",

        # Data Files
        "data/property_type.xml",
        # "data/estate.property.type.csv"
    ],
    "demo": [
        "demo/property_tag.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
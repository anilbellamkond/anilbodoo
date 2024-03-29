# Copyright (C) 2018 - TODAY, Open Source Integrators
# Copyright (C) 2021 Serpent Consulting Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Warranty Date on Lot/Serial Numbers",
    "summary": "Add warranty date to stock production lot",
    "version": "15.0.1.1.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "category": "Stock",
    "website": "https://github.com/OCA/rma",
    "depends": ["product_warranty", "stock"],
    "data": ["views/stock_production_lot.xml"],
    "installable": True,
    "development_status": "Beta",
    "maintainers": ["osi-scampbell", "max3903"],
}

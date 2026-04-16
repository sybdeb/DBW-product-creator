from odoo import models, fields, api

class CatalogDashboard(models.Model):
    _inherit = 'catalog.dashboard'

    missing_products_count = fields.Integer(
        compute='_compute_missing_products', 
        string='Ontbrekende Producten'
    )

    @api.model
    def _get_open_missing_product_domain(self):
        domain = [('error_type', '=', 'product_not_found')]
        error_model = self.env['supplier.import.error']

        if 'resolved' in error_model._fields and 'state' in error_model._fields:
            domain += ['|', ('resolved', '=', False), ('state', '=', 'unresolved')]
        elif 'resolved' in error_model._fields:
            domain += [('resolved', '=', False)]
        elif 'state' in error_model._fields:
            domain += [('state', '=', 'unresolved')]

        return domain

    @api.depends_context('uid')
    def _compute_missing_products(self):
        for rec in self:
            # Check of supplier_pricelist_sync module geïnstalleerd is
            if 'supplier.import.error' in self.env:
                SupplierError = self.env['supplier.import.error']
                rec.missing_products_count = SupplierError.search_count(
                    rec._get_open_missing_product_domain()
                )
            else:
                rec.missing_products_count = 0

    def action_view_missing_products(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ontbrekende Producten',
            'res_model': 'supplier.import.error',
            'view_mode': 'list,form',
            'domain': self._get_open_missing_product_domain(),
            'context': {'create': False},
        }

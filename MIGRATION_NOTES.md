# Migration Notes: dbw_odoo_base_v2 Hub Integration

## Wijziging in Dependencies

### Oude situatie:
- `depends`: `product_supplier_sync` (bevatte supplier.import.error)

### Nieuwe situatie:
- supplier.import.error is verhuisd naar dbw_odoo_base_v2 hub
- product_supplier_sync depends nu op dbw_odoo_base_v2

## Benodigde Aanpassingen

### __manifest__.py
```python
# OUD:
'depends': ['purchase', 'product', 'website_sale', 'product_supplier_sync', 'webshop_catalog_dashboard'],

# NIEUW:
'depends': ['purchase', 'product', 'website_sale', 'dbw_odoo_base_v2', 'product_supplier_sync', 'webshop_catalog_dashboard'],
```

**Optie A - Expliciete dependency:**
- Voeg `dbw_odoo_base_v2` toe aan depends
- Garantie dat supplier.import.error beschikbaar is

**Optie B - Impliciete dependency:**
- Laat zoals het is
- product_supplier_sync depends al op dbw_odoo_base_v2
- Indirecte toegang tot supplier.import.error

## Aanbeveling

Voeg `dbw_odoo_base_v2` toe voor **duidelijkheid en stabiliteit**:
- Expliciete dependency = betere documentatie
- Voorkomt problemen als product_supplier_sync niet geïnstalleerd is
- Module kan standalone werken met alleen dbw_odoo_base_v2

## Code aanpassingen
GEEN - Code gebruikt al correct `self.env['supplier.import.error']`

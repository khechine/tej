import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_tej_custom_fields():
	custom_fields = {
		"Supplier": [
			{
				"fieldname": "custom_rs_rate",
				"label": "RS Rate (%)",
				"fieldtype": "Percent",
				"insert_after": "tax_id"
			},
			{
				"fieldname": "custom_type_identifiant",
				"label": "Type Identifiant",
				"fieldtype": "Select",
				"options": "\n1: Matricule Fiscal\n2: CIN\n3: Passport\n5: Carte Séjour",
				"insert_after": "custom_rs_rate"
			}
		]
	}
	create_custom_fields(custom_fields)

import frappe
import json
from tej.tej.utils.xml_generator import generate_rs_xml
from frappe.utils import getdate

@frappe.whitelist()
def export_invoice(invoice):
	"""
	Export a single Purchase Invoice to TEJ XML
	"""
	doc = frappe.get_doc("Purchase Invoice", invoice)
	
	# Find related RS Certificate
	certificates = frappe.get_all("Tej RS Certificate", filters={
		"purchase_invoice": invoice,
		"docstatus": 1
	})
	
	if not certificates:
		frappe.throw(frappe._("Aucun certificat de retenue à la source (RS) soumis n'a été trouvé pour cette facture."))
	
	# Use posting date of the invoice for period
	posting_date = getdate(doc.posting_date)
	year = posting_date.year
	month = posting_date.month
	
	xml_content = generate_rs_xml(doc.company, year, month, [certificates[0].name])
	
	file_name = f"TEJ_{doc.name}.xml"
	
	# Create a temporary file to download
	frappe.response['filename'] = file_name
	frappe.response['filecontent'] = xml_content
	frappe.response['type'] = 'download'

@frappe.whitelist()
def export_bulk(invoices):
	"""
	Export multiple Purchase Invoices to a single TEJ XML
	"""
	if isinstance(invoices, str):
		invoices = json.loads(invoices)
	
	certificate_names = []
	companies = set()
	years = set()
	months = set()
	
	for inv_name in invoices:
		inv_doc = frappe.get_doc("Purchase Invoice", inv_name)
		certs = frappe.get_all("Tej RS Certificate", filters={
			"purchase_invoice": inv_name,
			"docstatus": 1
		})
		
		if certs:
			certificate_names.append(certs[0].name)
			companies.add(inv_doc.company)
			
			posting_date = getdate(inv_doc.posting_date)
			years.add(posting_date.year)
			months.add(posting_date.month)
	
	if not certificate_names:
		frappe.throw(frappe._("Aucun certificat de retenue à la source (RS) soumis n'a été trouvé pour les factures sélectionnées."))
	
	if len(companies) > 1:
		frappe.throw(frappe._("Toutes les factures sélectionnées doivent appartenir à la même société."))
	
	# For bulk, we might have multiple months/years, which might be an issue for TEJ format
	# But we'll use the first one found or current if mixed?
	# Better to warn if mixed.
	if len(years) > 1 or len(months) > 1:
		frappe.msgprint(frappe._("Attention: Les factures sélectionnées couvrent plusieurs périodes. La période du premier certificat sera utilisée dans l'entête XML."))

	company = list(companies)[0]
	year = list(years)[0]
	month = list(months)[0]
	
	xml_content = generate_rs_xml(company, year, month, certificate_names)
	
	file_name = f"TEJ_Bulk_{company}_{year}_{month}.xml"
	
	frappe.response['filename'] = file_name
	frappe.response['filecontent'] = xml_content
	frappe.response['type'] = 'download'

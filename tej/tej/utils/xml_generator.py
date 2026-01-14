import frappe
from frappe.utils import get_first_day, get_last_day, flt
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_rs_xml(doc):
	"""
	Generates the XML for Tej Retenue à la Source (RS) Declaration
	"""
	root = ET.Element("DeclarationRS")
	
	# Identifiant Fiscal
	company = frappe.get_doc("Company", doc.company)
	identifiant = ET.SubElement(root, "IdentifiantFiscal")
	
	# Assuming tax_id is formatted as '1234567A/P/M/000'
	tax_id = company.tax_id or ""
	matricule = tax_id.split('/')[0] if '/' in tax_id else tax_id
	code_tva = tax_id.split('/')[1] if '/' in tax_id and len(tax_id.split('/')) > 1 else ""
	code_cat = tax_id.split('/')[2] if '/' in tax_id and len(tax_id.split('/')) > 2 else ""
	etab_sec = tax_id.split('/')[3] if '/' in tax_id and len(tax_id.split('/')) > 3 else "000"

	ET.SubElement(identifiant, "MatriculeFiscal").text = matricule
	ET.SubElement(identifiant, "CodeTVA").text = code_tva
	ET.SubElement(identifiant, "CodeCategorie").text = code_cat
	ET.SubElement(identifiant, "EtablissementSecondaire").text = etab_sec

	# Periode
	periode = ET.SubElement(root, "Periode")
	ET.SubElement(periode, "Annee").text = str(doc.year)
	ET.SubElement(periode, "Mois").text = doc.month

	# Certificats
	certificats_node = ET.SubElement(root, "Certificats")
	
	for row in doc.certificates:
		cert_doc = frappe.get_doc("Tej RS Certificate", row.rs_certificate)
		supplier = frappe.get_doc("Supplier", cert_doc.supplier)
		
		cert_node = ET.SubElement(certificats_node, "Certificat")
		
		# Beneficiaire
		beneficiaire = ET.SubElement(cert_node, "IdentifiantBeneficiaire")
		# Logic to determine type identifiant (1: Matricule, 2: CIN, 3: Passport, 5: Carte Sejour)
		type_identifiant = "1" 
		if supplier.get("custom_type_identifiant"):
			type_identifiant = supplier.custom_type_identifiant
		
		ET.SubElement(beneficiaire, "TypeIdentifiant").text = type_identifiant
		ET.SubElement(beneficiaire, "Identifiant").text = supplier.tax_id or ""

		# Retenues
		retenues_node = ET.SubElement(cert_node, "Retenues")
		retenue_node = ET.SubElement(retenues_node, "Retenue")
		
		ET.SubElement(retenue_node, "CodeRetenue").text = cert_doc.rs_code
		ET.SubElement(retenue_node, "MontantBrut").text = str(cert_doc.gross_amount)
		ET.SubElement(retenue_node, "TauxRetenue").text = str(cert_doc.rs_rate)
		ET.SubElement(retenue_node, "MontantRetenue").text = str(cert_doc.rs_amount)
		ET.SubElement(retenue_node, "MontantNet").text = str(cert_doc.net_amount)

	# Pretty print
	xml_str = ET.tostring(root, encoding='utf-8')
	reparsed = minidom.parseString(xml_str)
	return reparsed.toprettyxml(indent="  ")

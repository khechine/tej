import frappe
from frappe.model.document import Document
from tej.tej.utils.xml_generator import generate_rs_xml

class TejRSDeclaration(Document):
	@frappe.whitelist()
	def get_certificates(self):
		self.set("certificates", [])
		certificates = frappe.get_all("Tej RS Certificate", filters={
			"docstatus": 1,
			"posting_date": ["between", [
				frappe.utils.get_first_day(f"{self.year}-{self.month}-01"),
				frappe.utils.get_last_day(f"{self.year}-{self.month}-01")
			]]
		})

		for cert in certificates:
			self.append("certificates", {
				"rs_certificate": cert.name
			})
		
		self.save()

	@frappe.whitelist()
	def generate_xml_file(self):
		xml_content = generate_rs_xml(self)
		
		file_name = f"RS_Declaration_{self.company}_{self.year}_{self.month}.xml"
		_file = frappe.get_doc({
			"doctype": "File",
			"file_name": file_name,
			"attached_to_doctype": self.doctype,
			"attached_to_name": self.name,
			"content": xml_content,
			"is_private": 1
		})
		_file.save()
		
		self.xml_file = _file.file_url
		self.status = "Generated"
		self.save()
		
		return _file.file_url

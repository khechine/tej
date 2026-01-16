import frappe
from frappe.model.document import Document
from frappe.utils import flt

class TejRSCertificate(Document):
	def validate(self):
		self.calculate_amounts()

	def calculate_amounts(self):
		if self.gross_amount and self.rs_rate:
			self.rs_amount = flt(self.gross_amount * self.rs_rate / 100, 3)
			self.net_amount = flt(self.gross_amount - self.rs_amount, 3)
		elif self.gross_amount:
			self.net_amount = flt(self.gross_amount, 3)
			self.rs_amount = 0

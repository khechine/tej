frappe.ui.form.on('Tej RS Declaration', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Get Certificates'), function() {
				frm.call('get_certificates').then(() => {
					frm.refresh();
				});
			});
		}
		
		if (frm.doc.certificates && frm.doc.certificates.length > 0) {
			frm.add_custom_button(__('Generate XML'), function() {
				frm.call('generate_xml_file').then((r) => {
					if (r.message) {
						frappe.msgprint(__('XML file generated: {0}', [r.message]));
						frm.refresh();
					}
				});
			});
		}
	}
});

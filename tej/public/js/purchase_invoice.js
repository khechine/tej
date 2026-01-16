frappe.ui.form.on('Purchase Invoice', {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Créer Certificat RS'), () => {
                frappe.model.with_doctype('Tej RS Certificate', () => {
                    let cert = frappe.model.get_new_doc('Tej RS Certificate');
                    cert.purchase_invoice = frm.doc.name;
                    frappe.set_route('Form', 'Tej RS Certificate', cert.name);
                });
            }, __("Actions"));

            frm.add_custom_button(__('Exporter TEJ'), () => {
                const url = frappe.urllib.get_full_url(
                    "/api/method/tej.api.export_invoice?invoice=" + encodeURIComponent(frm.doc.name)
                );
                window.open(url, '_blank');
            }, __("Actions"));
        }
    }
});

frappe.ui.form.on('Purchase Invoice', {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Exporter TEJ'), () => {
                const url = frappe.urllib.get_full_url(
                    "/api/method/tej.api.export_invoice?invoice=" + encodeURIComponent(frm.doc.name)
                );
                window.open(url, '_blank');
            }, __("Actions"));
        }
    }
});

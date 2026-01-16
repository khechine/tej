frappe.listview_settings['Purchase Invoice'] = {
    onload(listview) {
        listview.page.add_actions_menu_item(__('Exporter TEJ'), () => {
            const selected = listview.get_checked_items();
            if (!selected.length) {
                frappe.msgprint(__('Veuillez sélectionner au moins une facture.'));
                return;
            }

            const invoices = selected.map(i => i.name);
            const url = frappe.urllib.get_full_url(
                "/api/method/tej.api.export_bulk?invoices=" + encodeURIComponent(JSON.stringify(invoices))
            );
            window.open(url, '_blank');
        });
    }
};

frappe.ui.form.on('Tej RS Certificate', {
    purchase_invoice: function (frm) {
        if (frm.doc.purchase_invoice) {
            frappe.db.get_value('Purchase Invoice', frm.doc.purchase_invoice, ['supplier', 'grand_total', 'base_grand_total'], (r) => {
                if (r) {
                    frm.set_value('supplier', r.supplier);
                    frm.set_value('gross_amount', r.base_grand_total || r.grand_total);

                    // Fetch default RS rate from Supplier
                    frappe.db.get_value('Supplier', r.supplier, 'custom_rs_rate', (s) => {
                        if (s && s.custom_rs_rate) {
                            frm.set_value('rs_rate', s.custom_rs_rate);
                        }
                    });
                }
            });
        }
    },
    gross_amount: function (frm) {
        frm.trigger('calculate_amounts');
    },
    rs_rate: function (frm) {
        frm.trigger('calculate_amounts');
    },
    calculate_amounts: function (frm) {
        if (frm.doc.gross_amount && frm.doc.rs_rate) {
            let rs_amount = frappe.utils.round(frm.doc.gross_amount * frm.doc.rs_rate / 100, 3);
            let net_amount = frappe.utils.round(frm.doc.gross_amount - rs_amount, 3);
            frm.set_value('rs_amount', rs_amount);
            frm.set_value('net_amount', net_amount);
        }
    }
});

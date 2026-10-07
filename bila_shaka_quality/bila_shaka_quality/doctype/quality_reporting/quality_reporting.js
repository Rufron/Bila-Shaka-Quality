// Copyright (c) 2026, Upande and contributors
// For license information, please see license.txt

// NOTE: the fetch below assumes "Bucket Traceability" exposes the fieldnames
// `greenhouse`, `harvester` and `harvest_timestamp`. Adjust them here (and the
// read-only fields in the DocType) if that DocType uses different names.
const BUCKET_DOCTYPE = "Bucket Traceability";
const BUCKET_FETCH_MAP = {
	greenhouse: "greenhouse",
	harvester: "harvester",
	harvest_timestamp: "harvest_timestamp",
};

frappe.ui.form.on("Quality Reporting", {
	bucket_code(frm) {
		fetch_bucket_details(frm);
	},

	total_stems_received(frm) {
		recalculate_stems(frm);
	},
});

frappe.ui.form.on("Quality Reporting Rejection Item", {
	rejected_quantity(frm) {
		recalculate_stems(frm);
	},
	rejections_add(frm) {
		recalculate_stems(frm);
	},
	rejections_remove(frm) {
		recalculate_stems(frm);
	},
});

function fetch_bucket_details(frm) {
	const fetch_fields = Object.values(BUCKET_FETCH_MAP);

	if (!frm.doc.bucket_code) {
		fetch_fields.forEach((f) => frm.set_value(f, null));
		return;
	}

	frappe.db
		.get_value(BUCKET_DOCTYPE, frm.doc.bucket_code, fetch_fields)
		.then((r) => {
			const data = (r && r.message) || {};
			Object.entries(BUCKET_FETCH_MAP).forEach(([target, source]) => {
				frm.set_value(target, data[source] ?? null);
			});
		});
}

function recalculate_stems(frm) {
	const rejected = (frm.doc.rejections || []).reduce(
		(total, row) => total + (row.rejected_quantity || 0),
		0
	);
	const accepted = (frm.doc.total_stems_received || 0) - rejected;

	frm.set_value("rejected_stems", rejected);
	frm.set_value("accepted_stems", accepted);
}

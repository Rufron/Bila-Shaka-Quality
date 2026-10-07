# Copyright (c) 2026, Upande and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document

#: DocType that ``bucket_code`` links to. Not yet implemented — the submit
#: hook degrades gracefully until this DocType (and its ``status`` field) exist.
BUCKET_DOCTYPE = "Bucket Traceability"
INSPECTED_STATUS = "Inspected"


class QualityReporting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from bila_shaka_quality.bila_shaka_quality.doctype.quality_reporting_rejection_item.quality_reporting_rejection_item import (
			QualityReportingRejectionItem,
		)

		accepted_stems: DF.Int
		amended_from: DF.Link | None
		bucket_code: DF.Link
		greenhouse: DF.Link | None
		harvest_timestamp: DF.Datetime | None
		harvester: DF.Link | None
		inspection_station: DF.Data | None
		output_bunch_batch: DF.Link | None
		overall_status: DF.Literal["Draft", "Passed", "Partial Reject", "Rejected"]
		rejected_stems: DF.Int
		rejections: DF.Table[QualityReportingRejectionItem]
		total_stems_received: DF.Int
	# end: auto-generated types

	def validate(self) -> None:
		self.calculate_totals()
		self.set_overall_status()

	def calculate_totals(self) -> None:
		"""Recompute accepted/rejected on the server so the figures are
		authoritative regardless of what the client submitted."""
		self.rejected_stems = sum(
			(row.rejected_quantity or 0) for row in self.rejections
		)
		self.accepted_stems = (self.total_stems_received or 0) - self.rejected_stems

		if self.rejected_stems > (self.total_stems_received or 0):
			frappe.throw(
				_("Rejected Stems ({0}) cannot exceed Total Stems Received ({1}).").format(
					self.rejected_stems, self.total_stems_received or 0
				)
			)

	def set_overall_status(self) -> None:
		"""Derive the business status from the stem counts. Left untouched
		once the document is submitted/cancelled so it reflects the outcome."""
		if self.docstatus != 0:
			return

		total = self.total_stems_received or 0
		if not total:
			self.overall_status = "Draft"
		elif self.rejected_stems == 0:
			self.overall_status = "Passed"
		elif self.rejected_stems >= total:
			self.overall_status = "Rejected"
		else:
			self.overall_status = "Partial Reject"

	def before_submit(self) -> None:
		total = self.total_stems_received or 0
		if (self.accepted_stems + self.rejected_stems) != total:
			frappe.throw(
				_(
					"Accepted Stems ({0}) + Rejected Stems ({1}) must equal "
					"Total Stems Received ({2})."
				).format(self.accepted_stems, self.rejected_stems, total)
			)

	def on_submit(self) -> None:
		self.update_bucket_status(INSPECTED_STATUS)

	def update_bucket_status(self, status: str) -> None:
		"""Flag the source bucket as inspected. Degrades to a warning while
		``Bucket Traceability`` (or its ``status`` field) does not yet exist,
		so Quality Reporting stays usable on its own."""
		if not self.bucket_code:
			return

		if not frappe.db.exists("DocType", BUCKET_DOCTYPE):
			frappe.msgprint(
				_("DocType {0} does not exist yet — skipped updating bucket status.").format(
					BUCKET_DOCTYPE
				),
				alert=True,
				indicator="orange",
			)
			return

		if not frappe.get_meta(BUCKET_DOCTYPE).has_field("status"):
			frappe.msgprint(
				_("{0} has no 'status' field — skipped updating bucket status.").format(
					BUCKET_DOCTYPE
				),
				alert=True,
				indicator="orange",
			)
			return

		frappe.db.set_value(BUCKET_DOCTYPE, self.bucket_code, "status", status)

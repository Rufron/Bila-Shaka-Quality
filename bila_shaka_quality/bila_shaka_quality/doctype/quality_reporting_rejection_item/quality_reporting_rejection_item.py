# Copyright (c) 2026, Upande and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class QualityReportingRejectionItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		defect_category: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		rejected_quantity: DF.Int
		remarks: DF.SmallText | None
	# end: auto-generated types

	pass

# Copyright (c) 2026, Upande and contributors
# For license information, please see license.txt

from __future__ import annotations

from frappe.model.document import Document


class QualityParameter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.SmallText | None
		is_active: DF.Check
		parameter_name: DF.Data
		tolerance_percentage: DF.Percent
	# end: auto-generated types

	pass

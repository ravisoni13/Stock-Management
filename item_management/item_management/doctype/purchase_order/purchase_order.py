# Copyright (c) 2024, ravi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PurchaseOrder(Document):
    
    def validate(self):
        total_amount = 0
        for item in self.items:
            item.amount = item.quantity * item.rate
            total_amount += item.amount
        self.total_amount = total_amount

    def on_submit(self):
        for item in self.items:
            self.update_stock(item.item, item.quantity)

    def update_stock(self, item_code, qty):
        item = frappe.get_doc("Item", item_code)
        item.stock_quantity += qty
        item.save()

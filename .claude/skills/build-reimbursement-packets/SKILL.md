---
name: build-reimbursement-packets
description: Extract, reconcile, and package lab receipts, invoices, purchase orders, travel expenses, and grant-expenditure evidence into checked spreadsheets and ordered PDF packets. Use for University of Toronto reimbursements, vendor reconciliation, expense reports, PO matching, missing-document audits, and expenditure reporting.
---

# Build reimbursement packets

1. Confirm claimant, trip or purchase purpose, date range, funding source, currency policy, and required institutional template.
2. Inventory source files without mixing `60_Personal_Legal_Finance` into lab expenses.
3. Extract vendor, date, description, subtotal, tax, total, currency, payment method, invoice or receipt number, PO, and source filename.
4. Never guess unreadable amounts. Flag OCR uncertainty and duplicate-looking charges.
5. Match PO, invoice, proof of payment, and reimbursement row. Identify missing links.
6. Use the spreadsheet skill to build a ledger with formulas and subtotals. Use the PDF skill to order source documents to match ledger rows.
7. Verify arithmetic, currency conversion source and date, tax treatment, duplicates, and packet completeness.
8. Deliver the ledger, ordered packet, exception list, and totals by funding source.

Read `references/ledger-schema.md` before creating the workbook.

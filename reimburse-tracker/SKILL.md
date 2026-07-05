---
name: reimburse-tracker
description: Extract, tabulate, and package receipts/invoices for expense reimbursement and grant expenditure reporting. Use to pull amounts/dates/vendors from receipt PDFs into a spreadsheet, match invoices to POs, and assemble reimbursement packets. Triggers on "reimbursement", "expense report", "receipts", "invoice", "expenditure report", "PO matching".
---

# Reimburse Tracker — Receipts → Reimbursement Packet

Turns the pile of receipts/invoices in `~/Downloads/50_Lab_Admin_Procurement/` into clean reimbursement and grant-expenditure reports for UofT.

## Workflow
1. Gather the relevant receipts/invoices (PDFs) — use the PDF read tools (`read_pdf_content` / Nutrient `read_text`) to extract text.
2. For each, extract: **date, vendor, description, amount, currency, tax, PO#/invoice#, funding source/grant*. Note foreign-currency items (some are USD/EUR — flag for FX conversion).
3. Build a spreadsheet (xlsx skill) with one row per item, subtotals per funding source, and a grand total. Include a column linking to the source PDF filename.
4. Match invoices to POs where a PO# is present (VWR, Bio-Rad, Eve Technologies, etc.).
5. Assemble the packet: merge receipts into a single PDF in the same order as the spreadsheet (PDF merge tool), name it `Reimbursement_<name>_<YYYY-MM>.pdf`.
6. Flag anything missing an amount or date to `90_Archive_To_Review` and list it for the user.

## Notes
- Grant expenditure reports (e.g. CFF "Report of Expenditures") have their own templates — reuse existing xlsx templates in the grants/admin folders.
- Never guess an amount; if OCR is ambiguous, surface it for confirmation.
- Keep personal receipts (`60_Personal_Legal_Finance`) separate from lab reimbursements.

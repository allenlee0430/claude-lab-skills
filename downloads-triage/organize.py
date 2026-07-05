#!/usr/bin/env python3
"""Classify and organize ~/Downloads into a numbered scheme mirroring the Desktop.
Every move is logged to a manifest CSV and an undo script for full reversibility.
Dry-run by default; pass --apply to actually move."""
import os, sys, csv, re, shutil, time

HOME = os.path.expanduser("~")
DL = os.path.join(HOME, "Downloads")
APPLY = "--apply" in sys.argv

CATS = {
    "10_Research_Manuscripts": "papers, manuscript drafts, reviews, figures, SI",
    "20_Grants_Awards": "grant apps, LOIs, budgets, fellowships, awards",
    "30_Presentations": "slide decks",
    "40_Data_Protocols_Images": "data, screenshots, images, protocols, raw exports",
    "50_Lab_Admin_Procurement": "invoices, quotes, POs, receipts, reimbursements",
    "60_Personal_Legal_Finance": "visa, PR, SIN, tax, personal id, insurance",
    "70_Code_Automation": "scripts and code",
    "80_Software_Installers": "dmg, app, installers",
    "90_Archive_To_Review": "unclassified / ambiguous",
}

def cat_for(name, is_dir):
    n = name.lower()
    # ---- 60 Personal / Legal / Finance (check first: sensitive) ----
    if any(k in n for k in ["visa","evisa","pr card","sin ","sin.","sin_","permanent resident",
        "passport","nonimmigrant","immigrant","wellness","medical report","tax","rakuten",
        "credit card","member id","personal statement","pr_card","prcard","los ",
        "police","citizenship","insurance","5106","5257"]):
        return "60_Personal_Legal_Finance"
    # ---- 50 Lab Admin / Procurement / Receipts ----
    if any(k in n for k in ["invoice","receipt","reimburse","quote","quotation","po#","po ",
        "purchase order","emailreceipt","billing","expenditure","vwr","bio-rad","biorad",
        "eve technologies","statement","folio","refund","order w","packing","cc statement"]):
        return "50_Lab_Admin_Procurement"
    # ---- 20 Grants / Awards / Fellowships ----
    if any(k in n for k in ["grant","cihr","cff","cfi","nserc","discovery","fellowship","award",
        "cdmrp","dod","dmd","loi","letter of intent","ogs","usra","proposal","cbrf","oicr",
        "nmin","crc ","incentive","dossier","budget","synopsis","pioneer","emerging scientist",
        "mcdonald","other support","othersupport","personal statement","support letter",
        "dean's support","registration","peer review","scoring","application scoring"]):
        return "20_Grants_Awards"
    # ---- 30 Presentations ----
    if n.endswith((".pptx",".ppt",".key")):
        return "30_Presentations"
    # ---- 70 Code / Automation ----
    if n.endswith((".py",".ipynb",".r",".sh",".js",".ts",".m",".cdxml",".tex")):
        return "70_Code_Automation"
    # ---- 80 Software / Installers ----
    if n.endswith((".dmg",".pkg",".exe",".aso")) or n.endswith(".app"):
        return "80_Software_Installers"
    # ---- 40 Data / Protocols / Images ----
    if n.endswith((".png",".jpg",".jpeg",".heic",".tif",".tiff",".gif",".mp4",".mov",".svg")):
        return "40_Data_Protocols_Images"
    if any(k in n for k in ["protocol","raw data","raw_data","_export","spreadsheet","heatmap",
        "formulation","gantt","dataset","flow","spectral","screenshot","img_","image_","figure",
        "prism","western","gel","facs","in vitro","in vivo"]):
        return "40_Data_Protocols_Images"
    if n.endswith((".xlsx",".xls",".csv")):
        return "40_Data_Protocols_Images"
    if n.endswith(".zip"):
        return "40_Data_Protocols_Images"
    # ---- 10 Research / Manuscripts / Papers ----
    if any(k in n for k in ["manuscript","revision","review","abstract","supplementary","supporting",
        "nature","cell","molecular therapy","acs","nbt","nano","paper","et al","-et-al-","review comments",
        "review_","cover letter","publication","reporting summary","bnab","mrna","lnp","crispr","editing",
        "vaccine","delivery","therapy","cancer","dystrophy","tp53","p53","assay","binding","corona"]):
        return "10_Research_Manuscripts"
    if n.endswith((".docx",".doc",".pdf",".rtf",".md",".txt",".html",".enl")):
        return "10_Research_Manuscripts"  # default: research context dominates this drive
    return "90_Archive_To_Review"

def main():
    entries = [e for e in os.listdir(DL) if not e.startswith(".")
               and e not in CATS and e != "_ORGANIZE_MANIFEST.csv" and e != "_UNDO.sh"]
    plan = []
    for e in entries:
        p = os.path.join(DL, e)
        is_dir = os.path.isdir(p)
        c = cat_for(e, is_dir)
        plan.append((e, c, is_dir))

    # summary
    from collections import Counter
    counts = Counter(c for _, c, _ in plan)
    print(f"{'APPLY' if APPLY else 'DRY-RUN'} — {len(plan)} top-level items\n")
    for c in CATS:
        print(f"  {c:32s} {counts.get(c,0)}")
    print()

    if not APPLY:
        for c in CATS:
            samples = [e for e,cc,_ in plan if cc==c][:6]
            if samples:
                print(f"## {c}")
                for s in samples: print(f"   - {s}")
        return

    manifest = os.path.join(DL, "_ORGANIZE_MANIFEST.csv")
    undo = os.path.join(DL, "_UNDO.sh")
    for c in CATS:
        os.makedirs(os.path.join(DL, c), exist_ok=True)
    with open(manifest, "w", newline="") as mf, open(undo, "w") as uf:
        w = csv.writer(mf); w.writerow(["original","moved_to","is_dir"])
        uf.write("#!/bin/bash\n# Undo Downloads organization. Run: bash _UNDO.sh\ncd \"$(dirname \"$0\")\"\n")
        moved = 0
        for e, c, is_dir in plan:
            src = os.path.join(DL, e)
            dstdir = os.path.join(DL, c)
            dst = os.path.join(dstdir, e)
            if os.path.exists(dst):
                base, ext = os.path.splitext(e)
                dst = os.path.join(dstdir, f"{base}__dup{int(time.time()*1000)%100000}{ext}")
            try:
                shutil.move(src, dst)
                w.writerow([src, dst, is_dir])
                uf.write(f'mv -n {shell_quote(dst)} {shell_quote(src)}\n')
                moved += 1
            except Exception as ex:
                print(f"SKIP {e}: {ex}")
    print(f"\nMoved {moved} items. Manifest: {manifest}  Undo: {undo}")

def shell_quote(s):
    return "'" + s.replace("'", "'\\''") + "'"

if __name__ == "__main__":
    main()

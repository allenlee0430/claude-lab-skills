#!/usr/bin/env python3
"""Safely organize loose files and obvious misclassifications.

Dry-run is the default. Each applied run writes a CSV manifest and shell undo script.
Only direct children are considered, so project folders remain intact.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
import re
import shlex
import shutil


CATEGORIES = (
    "00_Active_Now",
    "10_Research_Manuscripts",
    "20_Grants_Awards",
    "30_Presentations",
    "40_Data_Protocols_Images",
    "50_Lab_Admin_Procurement",
    "60_Personal_Legal_Finance",
    "70_Code_Automation",
    "80_Software_Installers",
    "90_Archive_To_Review",
)

PROTECTED_PREFIXES = ("_ORGANIZE_", "_RECLASSIFY_", "_UNDO")


def contains_any(name: str, terms: tuple[str, ...]) -> bool:
    return any(term in name for term in terms)


def contains_token(name: str, token: str) -> bool:
    return re.search(rf"(^|[^a-z0-9]){re.escape(token)}([^a-z0-9]|$)", name) is not None


def classify(name: str, *, allow_fallback: bool) -> str | None:
    n = name.lower().strip()
    suffix = Path(n).suffix

    # User-confirmed historical files whose names are otherwise opaque.
    exact = {
        "2022-01-12.docx": "10_Research_Manuscripts",
        "biab.docx": "20_Grants_Awards",
        "3752686_bowen_li_uoft_1260_bioinert_preplc_nov_13_2021_rsp.pdf": "50_Lab_Admin_Procurement",
        "3752689_bowen_li_uoft_1260_bioinert_preplc_nov_13_2021_rsp_foc.pdf": "50_Lab_Admin_Procurement",
        "unknown.pdf": "50_Lab_Admin_Procurement",
        "yong.docx": "50_Lab_Admin_Procurement",
        "yong.pdf": "50_Lab_Admin_Procurement",
        "3ecfb1a63d8e9fa.pdf": "60_Personal_Legal_Finance",
        "note.pdf": "60_Personal_Legal_Finance",
    }
    if n in exact:
        return exact[n]

    if n in {"sin.png", "sin.pdf", "bowen li.jpg", "bowen li.jpeg"} or contains_any(n, (
        "passport", "nonimmigrant", "evisa", " visa", "visa_", "visa-", "pr card",
        "permanent resident", "sin confirmation", "social insurance", "citizenship",
        "medical report", "health card", "insurance policy", "credit report",
        "tax slip", "t4a", " t4 ", "bank statement", "bankstatement", "credit card statement",
        "pay statement", "questrade", "amex statement", "chase.com", "member id",
        "mail-in-application-courier-label-request",
    )):
        return "60_Personal_Legal_Finance"

    if contains_any(n, (
        "invoice", "receipt", "reimburse", "quotation", "purchase order", "packing slip",
        "po#", " po ", "order w", "expenditure", "refund", "shipping", "courier",
        "employment letter", "offer letter", "access card", "facilityaccess", "animal invoice",
        "mcda", "confidential disclosure", "grant agreement", "certificate of expenditures",
    )) or contains_token(n, "nda"):
        return "50_Lab_Admin_Procurement"

    if contains_any(n, (
        "grant", "fellowship", "award", "proposal", "letter of intent", " loi ", "cihr",
        "nserc", " cfi", "cystic fibrosis foundation", " cff", "cdmrp", "oicr", "jelf",
        "canada research chair", "emerging scientist", "mcdonald", "biosketch", "other support",
        "support letter", "budget", "application scoring", "dossier", "usra",
    )):
        return "20_Grants_Awards"

    if suffix in {".ppt", ".pptx", ".key"}:
        return "30_Presentations"
    if suffix in {".py", ".ipynb", ".r", ".sh", ".js", ".ts", ".tex", ".cdxml"}:
        return "70_Code_Automation"
    if suffix in {".dmg", ".pkg", ".exe", ".aso"} or n.endswith(".app"):
        return "80_Software_Installers"
    if suffix in {".png", ".jpg", ".jpeg", ".heic", ".tif", ".tiff", ".gif", ".svg", ".mov", ".mp4"}:
        return "40_Data_Protocols_Images"
    if contains_any(n, ("protocol", "raw data", "dataset", "heatmap", "formulation", "screenshot", "figure")):
        return "40_Data_Protocols_Images"
    if suffix in {".xlsx", ".xls", ".csv", ".zip"}:
        return "40_Data_Protocols_Images"

    if contains_any(n, (
        "manuscript", "revision", "rebuttal", "reviewer", "supporting information", "supplementary",
        "cover letter", "reporting summary", "nature biotechnology", "nature communications",
        "molecular therapy", "acs nano", "mrna", "lnp", "lipid nanoparticle", "crispr",
        "gene editing", "vaccine", "nanomedicine", "assay",
    )):
        return "10_Research_Manuscripts"

    if allow_fallback:
        if suffix in {".doc", ".docx", ".pdf", ".rtf", ".md", ".txt", ".html", ".enl"}:
            return "10_Research_Manuscripts"
        return "90_Archive_To_Review"
    return None


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination
    stamp = datetime.now().strftime("%H%M%S")
    return destination.with_name(f"{destination.stem}__dup_{stamp}{destination.suffix}")


def plan_for(base: Path) -> list[tuple[Path, Path, str]]:
    moves: list[tuple[Path, Path, str]] = []
    for item in base.iterdir():
        if item.name.startswith(".") or item.name.startswith(PROTECTED_PREFIXES):
            continue
        if item.name in CATEGORIES:
            continue
        category = classify(item.name, allow_fallback=True)
        if category:
            moves.append((item, base / category / item.name, "loose"))

    for category in CATEGORIES:
        source_dir = base / category
        if not source_dir.is_dir() or category == "00_Active_Now":
            continue
        for item in source_dir.iterdir():
            if item.name.startswith(".") or item.name.startswith(PROTECTED_PREFIXES):
                continue
            desired = classify(item.name, allow_fallback=False)
            permitted = desired in {
                "60_Personal_Legal_Finance",
                "50_Lab_Admin_Procurement",
                "20_Grants_Awards",
            }
            # Papers commonly landed in image/data or personal folders because their
            # titles contained phrases such as "in vivo". Correct only those cases.
            if desired == "10_Research_Manuscripts" and category in {
                "40_Data_Protocols_Images",
                "60_Personal_Legal_Finance",
            }:
                permitted = True
            # In Archive, any explicit rule is acceptable; ambiguous files stay put.
            if category == "90_Archive_To_Review" and desired:
                permitted = True
            if desired and desired != category and permitted:
                moves.append((item, base / desired / item.name, "high-confidence reclassification"))
    return moves


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, default=[Path.home() / "Desktop", Path.home() / "Downloads"])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    all_moves: list[tuple[Path, Path, str]] = []
    for base in args.paths:
        if base.is_dir():
            all_moves.extend(plan_for(base.expanduser().resolve()))

    print(f"{'APPLY' if args.apply else 'DRY-RUN'}: {len(all_moves)} proposed moves")
    for source, destination, reason in all_moves:
        print(f"[{reason}] {source} -> {destination}")
    if not args.apply or not all_moves:
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    by_base: dict[Path, list[tuple[Path, Path, str]]] = {}
    for move in all_moves:
        source = move[0]
        base = next(path.expanduser().resolve() for path in args.paths if source.is_relative_to(path.expanduser().resolve()))
        by_base.setdefault(base, []).append(move)

    for base, moves in by_base.items():
        log_dir = base / "70_Code_Automation" / "Organization_Logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        manifest = log_dir / f"_RECLASSIFY_MANIFEST_{stamp}.csv"
        undo = log_dir / f"_UNDO_RECLASSIFY_{stamp}.sh"
        completed: list[tuple[Path, Path, str]] = []
        for source, destination, reason in moves:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination = unique_destination(destination)
            shutil.move(str(source), str(destination))
            completed.append((source, destination, reason))
        with manifest.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(("original", "moved_to", "reason"))
            writer.writerows(completed)
        with undo.open("w", encoding="utf-8") as handle:
            handle.write("#!/bin/sh\nset -e\n")
            for source, destination, _ in reversed(completed):
                handle.write(f"mkdir -p {shlex.quote(str(source.parent))}\n")
                handle.write(f"mv -n {shlex.quote(str(destination))} {shlex.quote(str(source))}\n")
        undo.chmod(0o700)
        print(f"Wrote {manifest} and {undo}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prueft alle planung/kw*.md gegen den echten Dashboard-Parser.

Nutzt parse_kw_plan() aus generate.py, damit die Pruefung nicht vom
Parser abdriften kann. Exit 1 wenn eine Datei leer geparst wird.

    python3 validate_plans.py
"""
import importlib.util
import re
import sys
from pathlib import Path


def load_generator():
    spec = importlib.util.spec_from_file_location("gen", "generate.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen"] = mod
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    return mod


def main() -> int:
    gen = load_generator()
    files = sorted(Path("planung").glob("kw*.md"))
    if not files:
        print("Keine planung/kw*.md gefunden.")
        return 1

    problems = []
    for path in files:
        kw = int(re.search(r"kw(\d+)", path.name).group(1))
        plan = gen.parse_kw_plan(kw)
        days = plan.get("days", [])
        filled = [d for d in days if d.get("workout") not in ("", "-", "–", None)]

        issues = []
        text = path.read_text(encoding="utf-8")
        if not re.search(r"^##\s+Wochenplan\b", text, re.MULTILINE):
            issues.append("kein '## Wochenplan'-Abschnitt")
        if not filled:
            issues.append("KEIN Tag geparst -> Dashboard bleibt leer")
        if not re.search(r"^\|\s*\*\*Total\*\*\s*\|", text, re.MULTILINE):
            issues.append("keine **Total**-Zeile -> 0 TSS im Ausblick")

        # Datumsangaben in der Tag-Spalte sind die haeufigste Ursache
        bad = re.findall(r"^\|\s*\*{0,2}(Mo|Di|Mi|Do|Fr|Sa|So)[^|]*\d[^|]*\|",
                         text, re.MULTILINE)
        if bad:
            issues.append(f"Datum/Zusatz in Tag-Spalte ({len(bad)}x) -> matcht nicht")

        status = "OK " if not issues else "FEHLER"
        print(f"[{status}] {path.name:12s} Tage={len(filled)}/7  TSS={plan.get('tss_plan', 0):4d}  {plan.get('theme','')[:34]}")
        for i in issues:
            print(f"          -> {i}")
            problems.append((path.name, i))

    print()
    if problems:
        print(f"{len(problems)} Problem(e) in {len({p[0] for p in problems})} Datei(en).")
        return 1
    print(f"Alle {len(files)} Dateien werden vom Dashboard-Parser korrekt gelesen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

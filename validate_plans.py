#!/usr/bin/env python3
"""Prueft planung/kw*.md und planung/periodisierung.md gegen die echten Parser.

Nutzt parse_kw_plan() und parse_periodisierung() aus generate.py, damit die
Pruefung nicht vom Parser abdriften kann. Dazu der Fueling-Check (fueling_check.py):
⛽-Angaben gegen Dauer + Intensitaet des geplanten intervals.icu-Workouts. Exit 1 wenn eine
Datei leer geparst wird oder eine ⛽-Angabe nicht passt – bei der Periodisierung faellt das sonst erst auf, wenn die Saisonleiste
im Dashboard "offen" zeigt.

    python3 validate_plans.py
"""
import importlib.util
import re
import sys
from datetime import date
from pathlib import Path

import fueling_check


def load_generator():
    spec = importlib.util.spec_from_file_location("gen", "generate.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen"] = mod
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    return mod


def fueling_problems(files, fetch, today):
    """⛽-Angaben gegen die geplanten intervals.icu-Workouts pruefen (fueling_check.py).

    Liefert (probleme, hinweise): probleme blockieren wie Parser-Fehler, hinweise
    (intervals.icu nicht erreichbar) werden nur angezeigt.
    """
    probleme, hinweise = [], []
    for path in files:
        kw = int(re.search(r"kw(\d+)", path.name).group(1))
        befunde, skip = fueling_check.check_plan(path.read_text(encoding="utf-8"), kw, fetch, today)
        probleme += [(path.name, f"Fueling {b}") for b in befunde]
        if skip:
            hinweise.append(f"{path.name}: {skip}")
    return probleme, hinweise


def check_periodisierung(gen) -> list[tuple[str, str]]:
    """Saisonplan gegen parse_periodisierung() pruefen."""
    problems: list[tuple[str, str]] = []
    phases = gen.parse_periodisierung()
    if not phases:
        print("[FEHLER] periodisierung.md  keine Phase geparst")
        print("          -> Gueltigkeitszeile 'KW40 2026 - KW09 2027' oder "
              "Abschnitt '## Phasenuebersicht' fehlt/abweichend")
        return [("periodisierung.md", "keine Phase geparst")]

    for a, b in zip(phases, phases[1:]):
        if b["start"] <= a["end"]:
            problems.append((b["kw"], f"ueberlappt {a['kw']}"))
        elif (b["start"] - a["end"]).days > 1:
            problems.append((b["kw"], f"Luecke nach {a['kw']}"))

    status = "OK " if not problems else "FEHLER"
    print(f"[{status}] {'periodisierung.md':12s} Phasen={len(phases):2d}  "
          f"{phases[0]['start']:%d.%m.%y}-{phases[-1]['end']:%d.%m.%y}  "
          f"{phases[0]['short']} -> {phases[-1]['short']}")
    for kw, issue in problems:
        print(f"          -> {kw}: {issue}")
    return [("periodisierung.md", f"{kw}: {i}") for kw, i in problems]


def main() -> int:
    gen = load_generator()
    problems_peri = check_periodisierung(gen)
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

    problems += problems_peri

    fuel_problems, fuel_hinweise = fueling_problems(files, fueling_check.fetch_events, date.today())
    for name, issue in fuel_problems:
        print(f"[FEHLER] {name:12s} -> {issue}")
    for h in fuel_hinweise:
        print(f"[HINWEIS] {h}")
    problems += fuel_problems

    print()
    if problems:
        print(f"{len(problems)} Problem(e) in {len({p[0] for p in problems})} Datei(en).")
        return 1
    print(f"Alle {len(files)} Dateien werden vom Dashboard-Parser korrekt gelesen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

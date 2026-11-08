"""Fueling-Check: g/h im Wochenplan gegen Dauer + Intensität des ICU-Workouts.

Bänder aus coaching_science.md 10.3. Fixtures spiegeln echte intervals.icu-Events
(Felder wie get_planned_events sie liefert, Werte aus KW46).
"""
from fueling_check import check_day


def ride(name, minutes, intensity, day="2026-11-10"):
    return {
        "id": 153454098, "start_date_local": f"{day}T00:00:00", "category": "WORKOUT",
        "type": "Ride", "name": name, "moving_time": minutes * 60,
        "icu_intensity": intensity, "icu_training_load": 100, "description": "",
    }


def codes(findings):
    return sorted(code for code, _ in findings)


def note(text, day="2026-11-10"):
    # Fueling-Note wie create_planned_workout(fueling_note=...) sie anlegt
    return {
        "id": 153454100, "start_date_local": f"{day}T00:00:00", "category": "NOTE",
        "type": None, "name": "⛽ Fueling – SwSp 4x15min - 270W", "moving_time": None,
        "icu_intensity": None, "icu_training_load": None, "description": text,
    }


SWSP_105 = ride("SwSp 4x15min - 270W", 105, 80.4)


def test_heutiger_fehler_45gh_bei_swsp_ueber_90min_wird_erkannt():
    # 8.11.2026: 45g/h für 1h45 SwSp – richtig wären 70–90g/h (SwSp lang >90min)
    assert codes(check_day("🎯 Kern · ⛽ 45g/h → ~75g", [SWSP_105])) == ["band"]

LIT_165 = ride("LIT 2h45 - 180W Grundlage", 165, 59.4, day="2026-11-14")


def test_lit_lang_mit_swsp_menge_ist_zu_viel():
    # 165min LIT = "LIT lang" 30–50g/h; 70g/h wäre eine SwSp-Menge
    assert codes(check_day("⛽ 70g/h", [LIT_165])) == ["band"]


def test_kw46_vorgaben_passen():
    # echter Di 10.11.: Workout 153454098 + Fueling-Note 153454100 (dort steht das Wasser)
    di = [SWSP_105, note("⛽ 75g/h → ~130g gesamt · 2:1 Malto:Fructose · Salz ~2g\n"
                         "2 Flaschen à 500ml, je 45g Malto + 22g Fructose + 1g Salz · "
                         "dazu eine dritte Flasche reines Wasser")]
    assert check_day("⛽ 75g/h → ~130g (2:1 Malto:Fructose)", di) == []
    assert check_day("🎯 Kern · ⛽ 45g/h → ~125g, Salz ~1,9g", [LIT_165]) == []


def test_swsp_genau_90min_gehoert_noch_zur_kurzen_zeile():
    # Tabelle: "60–90min" schließt 90 ein, erst darüber gilt 70–90g/h
    assert check_day("⛽ 60g/h", [ride("SwSp 3x15min - 270W", 90, 79.0)]) == []
    assert codes(check_day("⛽ 60g/h", [ride("SwSp 3x15min - 270W", 91, 79.0)])) == ["band"]

KA_120 = ride("4x10min KA - 270W 55rpm", 120, 78.0)


def test_ka_mit_swsp_menge_wird_erkannt():
    # KA bewusst 40–60g/h (AMPK-Reiz) – 70g/h würde den Reiz dämpfen
    assert codes(check_day("⛽ 70g/h", [KA_120])) == ["band"]


def test_ka_im_bewusst_niedrigen_band_braucht_keine_begruendung():
    assert check_day("⛽ 45g/h", [KA_120]) == []


def test_kadenz_im_namen_macht_keine_ka_einheit():
    # 55g/h: LIT lang (30–50) -> Befund, KA (40–60) -> kein Befund
    assert codes(check_day("⛽ 55g/h", [ride("LIT 2h - Kadenz 70rpm", 120, 60.0)])) == ["band"]


def test_begruendung_direkt_nach_gph_erlaubt_abweichung():
    lit_100 = ride("LIT 1h40 - Grundlage", 100, 60.0)
    assert codes(check_day("⛽ 0g/h", [lit_100])) == ["band"]
    assert check_day("⛽ 0g/h (nüchtern, FatMax)", [lit_100]) == []


def test_mix_klammer_ist_keine_begruendung():
    # Klammer hinter der Gesamtmenge beschreibt den Mix, sie begründet keine Abweichung
    assert codes(check_day("⛽ 45g/h → ~75g (2:1 Malto:Fructose)", [SWSP_105])) == ["band"]


def run(name, minutes, day="2026-11-13"):
    ev = ride(name, minutes, 91.7, day)
    ev.update(type="Run", id=153146031)
    return ev


def test_hit_band_60_bis_80():
    hit = ride("HIT_EB 4x4min - 330W", 90, 85.0)
    assert codes(check_day("⛽ 45g/h", [hit])) == ["band"]
    assert check_day("⛽ 70g/h", [hit]) == []


def test_fueling_an_einem_lauftag_ist_ein_befund():
    # Läufe: kein Fueling (außer Wettkampf)
    assert codes(check_day("⛽ 30g/h", [run("Lauf-Schwelle 3x8min", 45)])) == ["run"]


def test_ab_75gh_braucht_es_die_wasserflasche():
    assert codes(check_day("⛽ 80g/h", [SWSP_105])) == ["wasser"]
    assert check_day("⛽ 80g/h", [SWSP_105, note("⛽ 80g/h · dazu eine Flasche reines Wasser")]) == []
    assert check_day("⛽ 80g/h + Wasserflasche", [SWSP_105]) == []


def test_unter_75gh_braucht_es_keine_wasserflasche():
    assert check_day("⛽ 74g/h", [SWSP_105]) == []


def test_fueling_ohne_geplantes_workout_ist_ein_befund():
    assert codes(check_day("⛽ 45g/h", [])) == ["kein_workout"]
    assert codes(check_day("⛽ 45g/h", [note("⛽ 45g/h")])) == ["kein_workout"]


def test_unbekannter_workout_typ_ist_ein_befund():
    assert codes(check_day("⛽ 45g/h", [ride("Freie Ausfahrt", 120, 65.0)])) == ["gruppe"]


def test_name_und_intensitaet_muessen_zusammenpassen():
    # LIT-Name, aber IF 0,82 -> die Einheit ist keine LIT, das Band wäre falsch gewählt
    assert codes(check_day("⛽ 45g/h", [ride("LIT 2h - Grundlage", 120, 82.0)])) == ["if"]
    assert codes(check_day("⛽ 60g/h", [ride("SwSp 3x10min - 270W", 90, 60.0)])) == ["if"]


def test_bei_mehreren_events_zaehlt_die_radeinheit():
    tag = [run("Easy 30min - Kadenz 170", 30, day="2026-11-10"), ride("LIT 2h - Grundlage", 120, 60.0)]
    assert check_day("⛽ 45g/h", tag) == []


def test_lit_kurz_unter_90min_hoechstens_30gh():
    # z.B. LIT 1h in der Entlastungswoche
    assert codes(check_day("⛽ 45g/h", [ride("LIT 1h - locker", 60, 58.0)])) == ["band"]


def test_lit_ueber_3h_braucht_50_bis_70gh():
    lit_210 = ride("LIT 3h30 - Grundlage", 210, 60.0)
    assert codes(check_day("⛽ 45g/h", [lit_210])) == ["band"]
    assert check_day("⛽ 60g/h", [lit_210]) == []


def test_lit_genau_3h_gehoert_noch_zu_lit_lang():
    # Tabelle: "90–180min" schließt 180 ein
    assert check_day("⛽ 45g/h", [ride("LIT 3h - Grundlage", 180, 60.0)]) == []


def test_rennen_braucht_90_bis_110gh():
    rennen = ride("Rennen RadRace 120", 240, 82.0)
    assert codes(check_day("⛽ 60g/h", [rennen])) == ["band"]
    assert check_day("⛽ 100g/h + Wasserflasche", [rennen]) == []


def test_ka_mit_swsp_anteil_wird_als_ka_gefuelt():
    # Bibliothek: KA_1x10_SwSp_3x12.zwo, 1:39h – als SwSp lang wären es 70–90g/h
    assert check_day("⛽ 45g/h", [ride("KA_1x10_SwSp_3x12", 99, 78.0)]) == []


def test_bei_zwei_radeinheiten_zaehlt_die_laengere():
    tag = [ride("LIT 1h - locker", 60, 58.0), ride("LIT 3h - Grundlage", 180, 60.0)]
    assert check_day("⛽ 45g/h", tag) == []


# ---- Datei-Ebene: Tabelle lesen, Woche datieren, Events holen ---------------------------
from datetime import date

from fueling_check import check_plan

PLAN = """# KW46 – Block 1 · Schwelle Woche 2

## Wochenplan

| Tag | Workout | TSS ca. | TSS Ist | Status | Notiz |
|---|---|---|---|---|---|
| Mo | 🏃 Easy 30min – Kadenz 170 + 💪 Kraft A | 42 | – | ⬜ | 4,0 km |
| Di | 🚴 SwSp 4×15min – 270W (Rolle) | 113 | – | ⬜ | 🎯 Kern · 1h45 · ⛽ {di} |
| Mi | 💪 Kraft B | 6 | – | ⬜ | |
| Do | Ruhetag | – | – | ⬜ | |
| Fr | 🏃 Lauf-Schwelle 3×8min | 63 | – | ⬜ | 🎯 Kern |
| Sa | 🚴 LIT 2h45 – 180W Grundlage (Rolle) | 97 | – | ⬜ | 🎯 Kern · ⛽ 45g/h → ~125g |
| So | 🏃 Longrun 48min progressiv | 61 | – | ⬜ | 6,5 km |
| **Total** | | **~382** | | | |
"""
TODAY = date(2026, 11, 8)


class FakeIcu:
    """Steht für intervals.icu: liefert feste Events und merkt sich den abgefragten Zeitraum."""
    def __init__(self, events):
        self.events, self.calls = events, []

    def __call__(self, oldest, newest):
        self.calls.append((oldest, newest))
        return self.events


def test_heutiger_fehler_wird_auf_dateiebene_dem_dienstag_zugeordnet():
    icu = FakeIcu([SWSP_105, LIT_165])
    befunde, uebersprungen = check_plan(PLAN.format(di="45g/h → ~75g"), 46, icu, TODAY)
    assert icu.calls == [(date(2026, 11, 9), date(2026, 11, 15))]
    assert uebersprungen is None
    assert len(befunde) == 1 and befunde[0].startswith("Di:")


def test_korrekter_kw46_plan_hat_keine_befunde():
    icu = FakeIcu([SWSP_105, note("… dazu eine dritte Flasche reines Wasser"), LIT_165])
    assert check_plan(PLAN.format(di="75g/h → ~130g"), 46, icu, TODAY) == ([], None)


def test_event_an_einem_anderen_tag_zaehlt_nicht():
    # Sa hat ⛽, aber das einzige Rad-Workout liegt am Di -> Sa ohne Workout
    icu = FakeIcu([SWSP_105, note("Wasser")])
    befunde, _ = check_plan(PLAN.format(di="75g/h"), 46, icu, TODAY)
    assert len(befunde) == 1 and befunde[0].startswith("Sa:")


def test_kw01_im_dezember_liegt_im_folgejahr():
    icu = FakeIcu([])
    check_plan(PLAN.format(di="75g/h"), 1, icu, date(2026, 12, 28))
    assert icu.calls == [(date(2027, 1, 4), date(2027, 1, 10))]


def test_stub_ohne_fueling_fragt_intervals_icu_nicht():
    stub = PLAN.replace("⛽ {di}", "").replace("⛽ 45g/h → ~125g", "")
    icu = FakeIcu([])
    assert check_plan(stub, 47, icu, TODAY) == ([], None)
    assert icu.calls == []


def test_icu_nicht_erreichbar_ueberspringt_ohne_zu_blockieren():
    def offline(oldest, newest):
        raise ConnectionError("proxy refused")
    befunde, uebersprungen = check_plan(PLAN.format(di="45g/h"), 46, offline, TODAY)
    assert befunde == []
    assert "übersprungen" in uebersprungen


# ---- Einbindung in validate_plans.py --------------------------------------------------
from validate_plans import fueling_problems


def test_validate_plans_ordnet_befund_der_datei_zu(tmp_path):
    datei = tmp_path / "kw46.md"
    datei.write_text(PLAN.format(di="45g/h → ~75g"), encoding="utf-8")
    probleme, hinweise = fueling_problems([datei], FakeIcu([SWSP_105, LIT_165]), TODAY)
    assert len(probleme) == 1
    assert probleme[0][0] == "kw46.md" and "Di:" in probleme[0][1]
    assert hinweise == []


def test_validate_plans_reicht_skip_hinweis_durch_ohne_problem(tmp_path):
    datei = tmp_path / "kw46.md"
    datei.write_text(PLAN.format(di="45g/h"), encoding="utf-8")

    def offline(oldest, newest):
        raise ConnectionError
    probleme, hinweise = fueling_problems([datei], offline, TODAY)
    assert probleme == []
    assert len(hinweise) == 1 and "kw46.md" in hinweise[0]

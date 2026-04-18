# Ernährungs-Karte — Design Spec

**Goal:** Tagestyp-basierte Ernährungshinweise direkt im Dashboard, sichtbar beim morgendlichen und abendlichen Check.

**Architecture:** Neue Funktion `get_nutrition_context()` in `generate.py` liest heutigen Tag aus dem bereits geparsten Wochenplan — kein neuer API-Call. Ergebnis fließt als `nutrition` in den Jinja2-Template-Kontext.

**Tech Stack:** Python 3.9, Jinja2 — keine neuen Dependencies.

---

## Tagestyp-Klassifikation

Basierend auf dem Workout-Typ des heutigen Tages im Wochenplan:

| Tagestyp | Workout-Erkennung | Protein (g/kg) |
|---|---|---|
| `intense` | SwSp, HIT, VO2max, KA, Intervall | 2,0 |
| `endurance_long` | LIT ≥ 2h (TSS ≥ 80) | 1,9 |
| `endurance_short` | LIT < 2h, Lauf, Schwimmen | 1,8 |
| `rest` | Ruhetag (kein Workout) | 1,7 |
| `sick` | Tag als krank markiert | 1,8 |

Protein in Gramm = Faktor × 88 kg, aufgerundet auf nächste 5g.

---

## Ausgabe-Struktur (`nutrition` dict)

```python
{
    "day_type": "intense",          # einer der 5 Typen
    "day_label": "⚡ SwSp 3×10",   # Workout-Name für Banner
    "day_sub": "Schwellenintervalle · ~72 TSS",
    "protein_g": 180,               # aufgerundet auf 5g
    "protein_gkg": 2.0,
    "protein_dist": ["~45g Frühstück", "~55g Mittagessen", "~45g Abendessen", "~30g Snacks"],
    "pre": {"emoji": "🍌", "title": "Leicht", "sub": "Banane, Toast, 90min vorher"},
    "during": {"emoji": "🍫", "title": "30–60g", "sub": "Gel oder Riegel ab 45min"},
    "post": {"emoji": "🥛", "title": "3:1", "sub": "Carbs:Protein in 30min"},
    "tips": [
        {"color": "green", "text": "Anti-entzündlich: Beeren, Omega-3 — unterstützt Anpassung"},
        {"color": "orange", "text": "Hydration: +500ml heute Abend, morgens Elektrolyte"},
    ]
}
```

---

## Karten-Layout (Variante A)

Position: **direkt nach Readiness Score**, vor Wochenplan.

```
┌─────────────────────────────────────┐
│ ERNÄHRUNG · HEUTE       [⚡ SwSp]   │
│                                     │
│ ⚡ Schwellenintervalle · ~72 TSS    │  ← Banner (orange)
│    Intensiver Tag → Carbs + Protein │
│                                     │
│ 🥚 Protein-Ziel: 180g · 2,0 g/kg  │  ← Protein-Block (grün)
│    ~45g Früh · ~55g Mittag · ...   │
│                                     │
│ [Pre: Leicht]  [30–60g]  [3:1]     │  ← Timing-Grid (3 Blöcke)
│  Banane,Toast  Gel ab 45  Quark+B  │
│                                     │
│ ● Anti-entzündlich: Beeren, Omega-3│  ← 2 Tipps
│ ● +500ml Wasser · Elektrolyte      │
└─────────────────────────────────────┘
```

**Krank-Tag:** Banner rot, Pre/During entfallen, nur Post + 2 Genesungs-Tipps (viel trinken, leicht essen, kein Druck).

**Ruhetag:** Banner grau/subtle, kein Timing-Grid (kein Training), nur Protein + 2 Tipps (Carbs reduziert, Magnesium abends).

---

## Implementierung

### Neue Funktion in `generate.py`

```python
NUTRITION_CONFIG = {
    "intense": {
        "protein_gkg": 2.0,
        "pre": {"emoji": "🍌", "title": "Leicht", "sub": "Banane, Toast, 90min vorher"},
        "during": {"emoji": "🍫", "title": "30–60g", "sub": "Gel oder Riegel ab 45min"},
        "post": {"emoji": "🥛", "title": "3:1", "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "green", "text": "Anti-entzündlich: Beeren, Omega-3 — unterstützt Anpassung"},
            {"color": "orange", "text": "Hydration: +500ml heute Abend, morgens Elektrolyte"},
        ],
    },
    "endurance_long": {
        "protein_gkg": 1.9,
        "pre": {"emoji": "🍝", "title": "Carbs", "sub": "Pasta, Reis, 2–3h vorher"},
        "during": {"emoji": "🍫", "title": "60–90g/h", "sub": "Alle 20min essen/trinken"},
        "post": {"emoji": "🥛", "title": "4:1", "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "orange", "text": "Laden: Kohlenhydratspeicher heute Abend voll auffüllen"},
            {"color": "green", "text": "Hydration: 500ml extra + Elektrolyte vor dem Start"},
        ],
    },
    "endurance_short": {
        "protein_gkg": 1.8,
        "pre": {"emoji": "🥣", "title": "Normal", "sub": "Haferbrei, 1–2h vorher"},
        "during": {"emoji": "💧", "title": "Optional", "sub": "Wasser reicht bis 90min"},
        "post": {"emoji": "🥛", "title": "3:1", "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "green", "text": "Protein-Fokus: Quark, Eier, Hülsenfrüchte nach dem Training"},
            {"color": "blue", "text": "Leichte Mahlzeiten — kein Volumen-Druck bei kurzen Einheiten"},
        ],
    },
    "rest": {
        "protein_gkg": 1.7,
        "pre": None, "during": None, "post": None,
        "tips": [
            {"color": "green", "text": "Carbs reduzieren: Mehr Gemüse, weniger Getreide heute"},
            {"color": "purple", "text": "Magnesium abends: 300–400mg unterstützt Schlafqualität"},
        ],
    },
    "sick": {
        "protein_gkg": 1.8,
        "pre": None, "during": None, "post": None,
        "tips": [
            {"color": "blue", "text": "Leicht essen — kein Druck, Appetit bestimmt die Menge"},
            {"color": "green", "text": "Viel trinken: Wasser, Tee, Brühe — Immunsystem unterstützen"},
        ],
    },
}
```

### Tagestyp-Erkennung

```python
def _classify_day_type(day: dict, sick: bool) -> str:
    if sick:
        return "sick"
    workout = day.get("workout", "").lower()
    tss = day.get("tss_plan", 0) or 0
    if not workout or workout in ("–", "-", "ruhetag", ""):
        return "rest"
    if any(k in workout for k in ("swsp", "hit", "vo2", "ka", "intervall")):
        return "intense"
    if "lit" in workout and tss >= 80:
        return "endurance_long"
    return "endurance_short"
```

### Protein-Verteilung

```python
def _protein_dist(protein_g: int) -> list[str]:
    # ~25% Früh, ~30% Mittag, ~25% Abend, ~20% Snacks
    return [
        f"~{round(protein_g * 0.25 / 5) * 5}g Frühstück",
        f"~{round(protein_g * 0.30 / 5) * 5}g Mittagessen",
        f"~{round(protein_g * 0.25 / 5) * 5}g Abendessen",
        f"~{round(protein_g * 0.20 / 5) * 5}g Snacks",
    ]
```

---

## Tests

- `test_classify_day_type`: alle 5 Typen korrekt erkannt
- `test_nutrition_protein_g`: Protein-Gramm korrekt berechnet und auf 5g gerundet
- `test_nutrition_rest_no_timing`: Ruhetag hat kein Timing-Grid
- `test_nutrition_sick`: Krank-Tag hat korrekten Typ und Tipps
- `test_get_nutrition_context_keys`: Alle Pflichtkeys im Output vorhanden

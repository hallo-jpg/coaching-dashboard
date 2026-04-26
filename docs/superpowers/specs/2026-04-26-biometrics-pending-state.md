# Biometrics Pending State Design

**Goal:** Wenn HRV, Schlaf und Ruhepuls noch nicht von der Uhr synchronisiert sind, zeigt die Readiness-Card einen Banner mit gedimmten Werten statt Fallback-Daten.

**Architecture:** Ein Flag `biometrics_pending` wird in `generate.py` gesetzt wenn `hrv` null ist. Das Template reagiert darauf mit einem visuellen Banner und Dimmen der betroffenen Bereiche.

**Tech Stack:** Python (generate.py), Jinja2 (dashboard.template.html)

---

## Änderungen in `generate.py`

### Fallback-Code entfernen

Die folgenden Fallback-Blöcke (aktuell ca. Zeilen 619–629) werden **entfernt**:

```python
# ENTFERNEN:
if not hrv:
    hrv = next((w.get("hrv") for w in reversed(wellness) if w.get("hrv")), 0)
# ...
if not sleep_s:
    sleep_s = next((w.get("sleepSecs") for w in reversed(wellness) if w.get("sleepSecs")), 0)
# ...
if not rhr:
    rhr = next((w.get("restingHR") for w in reversed(wellness) if w.get("restingHR")), 60)
```

### Flag setzen

Direkt nach dem Auslesen von `today_w`:

```python
biometrics_pending = not bool(today_w.get("hrv"))
```

HRV, Schlaf und Ruhepuls kommen immer zusammen von der Uhr — HRV als Proxy für alle drei reicht.

### Readiness Score bei fehlendem HRV

Wenn `biometrics_pending` True ist:
- `readiness_score` → `"–"` (String, kein Integer)
- `readiness_label` → `""` (leer)
- `readiness_color` → `"var(--muted)"` (grau)

### Template-Context ergänzen

```python
"biometrics_pending": biometrics_pending,
```

---

## Änderungen in `dashboard.template.html`

### Readiness Score

```html
{% if biometrics_pending %}
  <div class="readiness-score" style="color:var(--muted)">–</div>
{% else %}
  <div class="readiness-score" style="color:{{ readiness_color }}">{{ readiness_score }}</div>
  <div class="readiness-tag" style="color:{{ readiness_color }}">{{ readiness_label }}</div>
{% endif %}
```

### Banner + Dimmen

Direkt nach dem Score-Block, vor der HRV-Box:

```html
{% if biometrics_pending %}
<div style="background:rgba(15,17,23,0.7);border:1px solid rgba(99,102,241,0.3);border-radius:8px;padding:8px 12px;font-size:0.65rem;color:#94a3b8;text-align:center;margin-bottom:10px">
  ⏳ Uhr noch nicht synchronisiert – Werte folgen
</div>
{% endif %}
```

Die HRV-Box sowie die Schlaf- und Ruhepuls-Zellen werden einzeln gedimmt:

```html
<div style="...{% if biometrics_pending %}opacity:0.15;{% endif %}">
  <!-- HRV-Box -->
</div>

<!-- Mini-Grid: Schlaf | TSB | Ruhepuls -->
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;...">
  <div style="...{% if biometrics_pending %}opacity:0.15;{% endif %}"><!-- Schlaf --></div>
  <div style="..."><!-- TSB — immer voll sichtbar --></div>
  <div style="...{% if biometrics_pending %}opacity:0.15;{% endif %}"><!-- Ruhepuls --></div>
</div>
```

**TSB-Zelle bekommt kein Dimmen**, da der Wert immer aus CTL/ATL berechnet wird.

---

## Nicht ändern

- Sparkline: basiert auf 30-Tage-Historie, immer verfügbar
- Normalbereich (z.B. `52–62 ms`): bleibt in der gedimmten HRV-Box sichtbar als Kontext
- Alle anderen Karten: unberührt

---

## Scope

Nur `generate.py` und `dashboard.template.html`. Keine neuen Dateien, keine anderen Karten.

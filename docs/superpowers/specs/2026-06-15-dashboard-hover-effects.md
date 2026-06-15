# Dashboard: Hover-Effekte für CTL, Schlaf & TSS-Balken

**Datum:** 15. Juni 2026  
**Status:** Freigegeben

## Ziel

Drei Charts im Dashboard bekommen interaktive Hover-Effekte: CTL-Verlauf, Schlaf-Verlauf und TSS-Balken-Übersicht. Nutzer können so genaue Werte + Datum/Woche abrufen ohne den Chart zu verlassen.

## Ausgangslage

- **CTL-Verlauf (6 Monate):** SVG-Linienchart, ~180 Datenpunkte (täglich). Zeigt aktuell nur Endwert + Monatslabels. Kein Hover.
- **Schlaf-Verlauf (30 Tage):** SVG-Linienchart, ~30 Datenpunkte. Zeigt Ø-Wert + Tageslabels. Kein Hover.
- **TSS-Balken (8 Wochen):** HTML-Balkendiagramm, 8 Balken. TSS-Wert steht nur bei vergangenen Wochen über dem Balken. Kein Hover-Feedback.

## Technischer Ansatz

**Variante A (JS mousemove)** für CTL + Schlaf: Mausbewegung über Chart-Wrapper → JS sucht nächsten Datenpunkt → Crosshair + Tooltip folgen. Ein `bindChartHover()` Helper wird einmal definiert und für beide Charts aufgerufen.

**Inline JS hover** für TSS-Balken: `onmouseenter`/`onmouseleave` auf jeder Spalte, gleicher Pattern wie FTP-Chart-Tooltips.

## Änderungen

### 1. generate.py — get_ctl_history()

Neue Rückgabe im Dict: `"pts"` — Liste von Dicts pro Datenpunkt:

```python
{"x": x_pct, "d": "DD.MM.YY", "v": ctl_val_rounded}
```

- `x`: x-Position als Prozent des SVG_W (0.0–100.0)
- `d`: Datumsstring, Format `"DD.MM.YY"` (z.B. `"12.05.26"`)
- `v`: CTL-Wert, auf 1 Nachkommastelle gerundet

Berechnung analog zu FTP-History `x_pct`:
```python
x_pct = round((d - start).days / total_days * 100, 1)
d_fmt = f"{d.day:02d}.{d.month:02d}.{str(d.year)[2:]}"
```

### 2. generate.py — get_sleep_history()

Gleiche neue Rückgabe `"pts"`:

```python
{"x": x_pct, "d": "DD.MM.YY", "v": sleep_hours_rounded}
```

- `v`: Schlaf in Stunden, auf 1 Nachkommastelle gerundet

### 3. dashboard.template.html — CTL-Chart-Wrapper

Aktuell: SVG direkt in `ausblick-card`. Kein Wrapper-ID.

**Änderung:** SVG-Wrapper-Div bekommt `id="ctl-wrap"` und `cursor:crosshair`:

```html
<div id="ctl-wrap" style="position:relative;height:80px;cursor:crosshair">
  <svg ...>...</svg>
  <div id="ctl-ch" style="display:none;position:absolute;top:0;bottom:0;width:1px;background:rgba(255,255,255,0.18);pointer-events:none;z-index:5"></div>
  <div id="ctl-tt" style="display:none;position:absolute;top:2px;background:#1e293b;border:1px solid rgba(34,197,94,0.35);border-radius:6px;padding:5px 8px;white-space:nowrap;pointer-events:none;z-index:20;box-shadow:0 4px 12px rgba(0,0,0,0.5)"></div>
</div>
```

### 4. dashboard.template.html — Schlaf-Chart-Wrapper

Analog: `id="sl-wrap"`, `#sl-ch`, `#sl-tt`. Tooltip-Farbe: `rgba(121,134,203,0.35)` (lila, passend zur Schlaf-Farbe `#7986cb`).

```html
<div id="sl-wrap" style="position:relative;height:80px;cursor:crosshair">
  <svg ...>...</svg>
  <div id="sl-ch" style="display:none;position:absolute;top:0;bottom:0;width:1px;background:rgba(255,255,255,0.18);pointer-events:none;z-index:5"></div>
  <div id="sl-tt" style="display:none;position:absolute;top:2px;background:#1e293b;border:1px solid rgba(121,134,203,0.35);border-radius:6px;padding:5px 8px;white-space:nowrap;pointer-events:none;z-index:20;box-shadow:0 4px 12px rgba(0,0,0,0.5)"></div>
</div>
```

### 5. dashboard.template.html — JS bindChartHover

In einem `<script>`-Block (am Ende, nach allen Charts):

```javascript
(function() {
  function nearestPt(pts, xPct) {
    var best = pts[0], bd = 999;
    for (var i = 0; i < pts.length; i++) {
      var d = Math.abs(pts[i].x - xPct);
      if (d < bd) { bd = d; best = pts[i]; }
    }
    return best;
  }

  function bindChartHover(wrId, chId, ttId, pts, color, fmtVal) {
    var wr = document.getElementById(wrId);
    if (!wr) return;
    wr.addEventListener('mousemove', function(e) {
      var r = wr.getBoundingClientRect();
      var xp = (e.clientX - r.left) / r.width * 100;
      var pt = nearestPt(pts, xp);
      var ch = document.getElementById(chId);
      var tt = document.getElementById(ttId);
      ch.style.display = 'block';
      ch.style.left = pt.x + '%';
      tt.innerHTML = '<div style="font-size:0.65rem;font-weight:700;color:' + color + '">' + fmtVal(pt) + '</div>'
                   + '<div style="font-size:0.52rem;color:#94a3b8;margin-top:1px">' + pt.d + '</div>';
      tt.style.display = 'block';
      if (pt.x < 70) { tt.style.left = 'calc(' + pt.x + '% + 8px)'; tt.style.right = ''; }
      else            { tt.style.right = 'calc(' + (100 - pt.x) + '% + 8px)'; tt.style.left = ''; }
    });
    wr.addEventListener('mouseleave', function() {
      document.getElementById(chId).style.display = 'none';
      document.getElementById(ttId).style.display = 'none';
    });
  }

  var ctlPts = [{% for p in ctl_history.pts %}{"x":{{p.x}},"d":"{{p.d}}","v":{{p.v}}}{% if not loop.last %},{% endif %}{% endfor %}];
  bindChartHover('ctl-wrap','ctl-ch','ctl-tt', ctlPts, '#22c55e', function(p){ return 'CTL ' + p.v; });

  var slPts = [{% for p in sleep_history.pts %}{"x":{{p.x}},"d":"{{p.d}}","v":{{p.v}}}{% if not loop.last %},{% endif %}{% endfor %}];
  bindChartHover('sl-wrap','sl-ch','sl-tt', slPts, '#7986cb', function(p){
    return p.v + 'h ' + (p.v < 7 ? '😬' : p.v >= 8 ? '😴' : '');
  });
})();
```

### 6. dashboard.template.html — TSS-Balken

Jede Spalte im `{% for w in tss_weeks %}` Loop:

```html
<div style="flex:1;display:flex;flex-direction:column;align-items:center;height:100%;position:relative;cursor:pointer"
     onmouseenter="this.querySelector('.tw').style.opacity='1';var f=this.querySelector('.tf');if(f)f.style.filter='brightness(1.4)'"
     onmouseleave="this.querySelector('.tw').style.opacity='0';var f=this.querySelector('.tf');if(f)f.style.filter=''">
  <!-- TSS label, bar area, KW label, phase label — unverändert -->
  <!-- Fill-Balken bekommt zusätzlich class="tf" -->
  
  <!-- Tooltip -->
  <div class="tw" style="opacity:0;transition:opacity 0.12s;position:absolute;bottom:100%;
    {% if loop.first %}left:0{% elif loop.last %}right:0{% else %}left:50%;transform:translateX(-50%){% endif %};
    margin-bottom:4px;background:#1e293b;border:1px solid rgba(148,163,184,0.25);border-radius:6px;
    padding:5px 8px;white-space:nowrap;pointer-events:none;z-index:30;box-shadow:0 4px 12px rgba(0,0,0,0.5)">
    <div style="font-size:0.6rem;font-weight:700;color:#e2e8f0">KW{{ w.kw }}</div>
    {% if w.tss_ist > 0 %}<div style="font-size:0.52rem;color:#22c55e;margin-top:1px">Ist: {{ w.tss_ist }} TSS</div>{% endif %}
    {% if w.tss_plan > 0 %}<div style="font-size:0.52rem;color:#94a3b8;margin-top:1px">Plan: {{ w.tss_plan }} TSS</div>{% endif %}
  </div>
</div>
```

Fill-Balken (bisher ohne class) bekommt `class="tf"` zusätzlich zu seinem bestehenden `style`.

## Dateien

| Datei | Änderung |
|---|---|
| `generate.py` | `get_ctl_history()` + `get_sleep_history()` je um `pts`-Array erweitert |
| `dashboard.template.html` | CTL + Schlaf Wrapper-IDs + Crosshair/Tooltip-Divs + JS-Block; TSS-Spalten mit Hover-Handler + Tooltip |

## Nicht-Ziele

- Kein Touch-Support (mobile tap zeigt kein Tooltip — akzeptiert)
- Keine Highlight-Animation auf der SVG-Linie selbst
- Kein Pinned-Tooltip (Klick zum Festhalten)
- Keine Änderungen an Power/Pace-Bestwerten (separates Feature wenn gewünscht)

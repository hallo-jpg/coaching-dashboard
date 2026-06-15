# Dashboard Hover-Effekte Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add interactive hover tooltips to CTL-Verlauf, Schlaf-Verlauf, and TSS-Balken charts in the coaching dashboard.

**Architecture:** `generate.py` gets extended to emit `pts` arrays (x%, date, value) for CTL and sleep line charts. The template adds wrapper IDs + crosshair/tooltip divs to those two charts, a shared `bindChartHover()` JS helper that handles mousemove for both, and inline hover handlers on each TSS bar column.

**Tech Stack:** Python/Jinja2 (generate.py + dashboard.template.html), vanilla JS, SVG

---

### Task 1: generate.py — pts array für get_ctl_history()

**Files:**
- Modify: `generate.py:1461-1467`

Add a `pts` array to the return dict of `get_ctl_history()`. Each element: `{"x": x_pct_float, "d": "DD.MM.YY", "v": ctl_rounded}`.

The `coords` list already has `(x, y)` tuples in SVG pixels. We need matching `x_pct` values. These must be calculated from the same `(d - start).days / total_days * 100` formula used for `month_labels`.

- [ ] **Step 1: Read the current return dict (lines 1461–1467)**

```python
    return {
        "path": line_path,
        "fill_path": fill_path,
        "ctl_now": round(ctl_now, 1),
        "last_y": coords[-1][1],
        "month_labels": month_labels,
    }
```

- [ ] **Step 2: Build pts list alongside coords**

Replace the coords-building loop (lines 1443–1448) with:

```python
    coords = []
    pts = []
    for d_str, ctl in points:
        d = date.fromisoformat(d_str)
        x = round((d - start).days / total_days * SVG_W, 1)
        y = round(SVG_H - (ctl / ctl_max) * SVG_H, 1)
        coords.append((x, y))
        x_pct = round((d - start).days / total_days * 100, 1)
        d_fmt = f"{d.day:02d}.{d.month:02d}.{str(d.year)[2:]}"
        pts.append({"x": x_pct, "d": d_fmt, "v": round(ctl, 1)})
```

- [ ] **Step 3: Add pts to return dict**

```python
    return {
        "path": line_path,
        "fill_path": fill_path,
        "ctl_now": round(ctl_now, 1),
        "last_y": coords[-1][1],
        "month_labels": month_labels,
        "pts": pts,
    }
```

Also update the early-return fallback dict (line 1431) to include `"pts": []`:

```python
    except Exception:
        return {"path": "", "fill_path": "", "ctl_now": 0, "last_y": 40, "month_labels": [], "pts": []}
```

And the empty-points fallback (line 1435):

```python
    if not points:
        return {"path": "", "fill_path": "", "ctl_now": 0, "last_y": 40, "month_labels": [], "pts": []}
```

- [ ] **Step 4: Verify generate.py runs without error**

```bash
cd "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching"
python3 -c "from generate import get_ctl_history; r = get_ctl_history(); print(type(r['pts']), len(r['pts']), r['pts'][:2] if r['pts'] else 'empty')"
```

Expected: prints list type, count > 0, first two pts dicts with x/d/v keys.

- [ ] **Step 5: Commit**

```bash
git add generate.py
git commit -m "feat: add pts array to get_ctl_history() for hover support"
git push origin main
```

---

### Task 2: generate.py — pts array für get_sleep_history()

**Files:**
- Modify: `generate.py:1491-1521`

Same pattern as Task 1 but for sleep. Each element: `{"x": x_pct, "d": "DD.MM.YY", "v": sleep_hours_rounded}`.

- [ ] **Step 1: Read current sleep return dict (lines 1514–1521)**

```python
    return {
        "path": line_path,
        "fill_path": fill_path,
        "sleep_today": sleep_today,
        "avg_30d": avg_30d,
        "day_labels": day_labels,
        "last_y": coords[-1][1] if coords else 40,
    }
```

- [ ] **Step 2: Build pts alongside coords**

Replace the coords-building loop (lines 1491–1496) with:

```python
    coords = []
    pts = []
    for d_str, sleep_h in points:
        d = date.fromisoformat(d_str)
        x = round((d - start).days / total_days * SVG_W, 1)
        y = round(SVG_H - (min(sleep_h, SLEEP_MAX) / SLEEP_MAX) * SVG_H, 1)
        coords.append((x, y))
        x_pct = round((d - start).days / total_days * 100, 1)
        d_fmt = f"{d.day:02d}.{d.month:02d}.{str(d.year)[2:]}"
        pts.append({"x": x_pct, "d": d_fmt, "v": round(sleep_h, 1)})
```

- [ ] **Step 3: Add pts to return dict**

```python
    return {
        "path": line_path,
        "fill_path": fill_path,
        "sleep_today": sleep_today,
        "avg_30d": avg_30d,
        "day_labels": day_labels,
        "last_y": coords[-1][1] if coords else 40,
        "pts": pts,
    }
```

Also update the two early-return fallback dicts (lines 1477 and 1485) to include `"pts": []`:

```python
    except Exception:
        return {"path": "", "fill_path": "", "sleep_today": None, "avg_30d": 0.0, "day_labels": [], "last_y": 40, "pts": []}
```

```python
    if not points:
        return {"path": "", "fill_path": "", "sleep_today": None, "avg_30d": 0.0, "day_labels": [], "last_y": 40, "pts": []}
```

- [ ] **Step 4: Verify**

```bash
python3 -c "from generate import get_sleep_history; r = get_sleep_history(); print(type(r['pts']), len(r['pts']), r['pts'][:2] if r['pts'] else 'empty')"
```

Expected: list, ~30 items, first two with x/d/v keys.

- [ ] **Step 5: Commit**

```bash
git add generate.py
git commit -m "feat: add pts array to get_sleep_history() for hover support"
git push origin main
```

---

### Task 3: dashboard.template.html — CTL chart wrapper + Crosshair + Tooltip

**Files:**
- Modify: `dashboard.template.html:977`

The CTL chart wrapper div is at line 977:
```html
<div style="position:relative;width:100%;height:90px;margin-bottom:30px">
```

It needs `id="ctl-wrap"` and `cursor:crosshair`. Then add crosshair and tooltip divs **inside** the wrapper, between the `</svg>` and the month-labels div.

- [ ] **Step 1: Add id and cursor to wrapper (line 977)**

Old:
```html
    <div style="position:relative;width:100%;height:90px;margin-bottom:30px">
```

New:
```html
    <div id="ctl-wrap" style="position:relative;width:100%;height:90px;margin-bottom:30px;cursor:crosshair">
```

- [ ] **Step 2: Add crosshair and tooltip divs after `</svg>` (after line 991)**

The SVG closes at line 991 with `</svg>`. After it (before the month-labels div at line 992), insert:

```html
      <div id="ctl-ch" style="display:none;position:absolute;top:0;bottom:0;width:1px;background:rgba(255,255,255,0.18);pointer-events:none;z-index:5"></div>
      <div id="ctl-tt" style="display:none;position:absolute;top:2px;background:#1e293b;border:1px solid rgba(34,197,94,0.35);border-radius:6px;padding:5px 8px;white-space:nowrap;pointer-events:none;z-index:20;box-shadow:0 4px 12px rgba(0,0,0,0.5);font-size:0.65rem"></div>
```

- [ ] **Step 3: Verify the wrapper now has id and both helper divs**

```bash
grep -A 6 'id="ctl-wrap"' "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching/dashboard.template.html"
```

Expected: shows the wrapper div, then ctl-ch div, then ctl-tt div.

- [ ] **Step 4: Commit**

```bash
git add dashboard.template.html
git commit -m "feat: add ctl-wrap id + crosshair/tooltip divs to CTL chart"
git push origin main
```

---

### Task 4: dashboard.template.html — Schlaf chart wrapper + Crosshair + Tooltip

**Files:**
- Modify: `dashboard.template.html:1038-1055`

The sleep chart section (lines 1038–1055):
```html
    {% if sleep_history.path %}
    <div style="width:100%;margin-bottom:8px">
      <svg width="100%" height="80" viewBox="0 0 300 80" preserveAspectRatio="none">
        ...
      </svg>
    </div>
```

Needs `id="sl-wrap"`, `position:relative`, `height:80px`, `cursor:crosshair`. The SVG inside should not have an explicit `height="80"` attribute since the wrapper sets height via CSS (but it can stay — it doesn't break). Add crosshair + tooltip after `</svg>` inside the wrapper.

- [ ] **Step 1: Update the sleep wrapper div (line 1038)**

Old:
```html
    <div style="width:100%;margin-bottom:8px">
```

New:
```html
    <div id="sl-wrap" style="position:relative;width:100%;height:80px;margin-bottom:8px;cursor:crosshair">
```

- [ ] **Step 2: Add crosshair and tooltip divs after `</svg>` (after line 1054)**

The SVG closes at line 1054 with `</svg>`. After it (before `</div>` at line 1055), insert:

```html
      <div id="sl-ch" style="display:none;position:absolute;top:0;bottom:0;width:1px;background:rgba(255,255,255,0.18);pointer-events:none;z-index:5"></div>
      <div id="sl-tt" style="display:none;position:absolute;top:2px;background:#1e293b;border:1px solid rgba(121,134,203,0.35);border-radius:6px;padding:5px 8px;white-space:nowrap;pointer-events:none;z-index:20;box-shadow:0 4px 12px rgba(0,0,0,0.5);font-size:0.65rem"></div>
```

- [ ] **Step 3: Verify**

```bash
grep -A 4 'id="sl-wrap"' "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching/dashboard.template.html"
```

Expected: wrapper div, sl-ch, sl-tt.

- [ ] **Step 4: Commit**

```bash
git add dashboard.template.html
git commit -m "feat: add sl-wrap id + crosshair/tooltip divs to Schlaf chart"
git push origin main
```

---

### Task 5: dashboard.template.html — JS bindChartHover block

**Files:**
- Modify: `dashboard.template.html` — add `<script>` block near end of file (before the closing `</body>` or after the existing countdown JS block)

This task adds the shared `bindChartHover()` helper and wires it up for both CTL and sleep charts.

Find the existing countdown `<script>` block (search for `function setCountdown` or `function daysBetween` around line 1256) and add the new script block **after** it.

- [ ] **Step 1: Locate the end of the existing JS block**

```bash
grep -n "function daysBetween\|function setCountdown\|</script>" "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching/dashboard.template.html" | tail -20
```

Note the line number of the last `</script>` tag in the file.

- [ ] **Step 2: Add the bindChartHover script block after the last </script>**

Insert this complete block:

```html
<script>
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
    if (!wr || !pts.length) return;
    wr.addEventListener('mousemove', function(e) {
      var r = wr.getBoundingClientRect();
      var xp = (e.clientX - r.left) / r.width * 100;
      var pt = nearestPt(pts, xp);
      var ch = document.getElementById(chId);
      var tt = document.getElementById(ttId);
      ch.style.display = 'block';
      ch.style.left = pt.x + '%';
      tt.innerHTML = '<div style="font-weight:700;color:' + color + '">' + fmtVal(pt) + '</div>'
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

  {% if ctl_history.pts %}
  var ctlPts = [{% for p in ctl_history.pts %}{"x":{{p.x}},"d":"{{p.d}}","v":{{p.v}}}{% if not loop.last %},{% endif %}{% endfor %}];
  bindChartHover('ctl-wrap','ctl-ch','ctl-tt', ctlPts, '#22c55e', function(p){ return 'CTL ' + p.v; });
  {% endif %}

  {% if sleep_history.pts %}
  var slPts = [{% for p in sleep_history.pts %}{"x":{{p.x}},"d":"{{p.d}}","v":{{p.v}}}{% if not loop.last %},{% endif %}{% endfor %}];
  bindChartHover('sl-wrap','sl-ch','sl-tt', slPts, '#7986cb', function(p){
    return p.v + 'h ' + (p.v < 7 ? '😬' : p.v >= 8 ? '😴' : '');
  });
  {% endif %}
})();
</script>
```

Note: ` ` is a non-breaking space; `😬` is 😬; `😴` is 😴. This avoids raw emoji in the template which can cause encoding issues.

- [ ] **Step 3: Verify the script block landed correctly**

```bash
grep -c "bindChartHover" "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching/dashboard.template.html"
```

Expected: `3` (function definition + 2 calls).

- [ ] **Step 4: Commit**

```bash
git add dashboard.template.html
git commit -m "feat: add bindChartHover JS for CTL and Schlaf line charts"
git push origin main
```

---

### Task 6: dashboard.template.html — TSS-Balken Hover

**Files:**
- Modify: `dashboard.template.html:694-708`

The TSS bar loop is at lines 694–708. Each iteration renders one week column. The fill-bar div (line 703) needs `class="tf"`. The outer column div (line 695) needs `onmouseenter`/`onmouseleave` handlers and a tooltip div `.tw`.

Current column structure (lines 695–707):
```html
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;height:100%">
          <span ...>TSS label</span>
          <div style="flex:1;width:100%;...position:relative">
            {% if w.plan_bar_height_pct > 0 %}
            <div style="...plan outline..."></div>
            {% endif %}
            <div style="width:100%;height:{{ w.bar_height_pct }}%;background:{{ w.bar_color }};border-radius:3px 3px 0 0;position:relative;z-index:1;{% if w.is_current %}opacity:0.55{% endif %}"></div>
          </div>
          <span>KW label</span>
          <span>phase label</span>
        </div>
```

- [ ] **Step 1: Replace the outer column div opener (line 695)**

Old:
```html
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;height:100%">
```

New:
```html
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;height:100%;position:relative;cursor:pointer"
             onmouseenter="this.querySelector('.tw').style.opacity='1';var f=this.querySelector('.tf');if(f)f.style.filter='brightness(1.4)'"
             onmouseleave="this.querySelector('.tw').style.opacity='0';var f=this.querySelector('.tf');if(f)f.style.filter=''">
```

- [ ] **Step 2: Add class="tf" to the fill bar (line 703)**

Old:
```html
            <div style="width:100%;height:{{ w.bar_height_pct }}%;background:{{ w.bar_color }};border-radius:3px 3px 0 0;position:relative;z-index:1;{% if w.is_current %}opacity:0.55{% endif %}"></div>
```

New:
```html
            <div class="tf" style="width:100%;height:{{ w.bar_height_pct }}%;background:{{ w.bar_color }};border-radius:3px 3px 0 0;position:relative;z-index:1;{% if w.is_current %}opacity:0.55{% endif %}"></div>
```

- [ ] **Step 3: Add tooltip div .tw at the end of the column (before closing `</div>`, after the phase label at line 706)**

After the `<span>{{ w.phase_short }}</span>` line and before the closing `</div>`, insert:

```html
          <div class="tw" style="opacity:0;transition:opacity 0.12s;position:absolute;bottom:100%;{% if loop.first %}left:0{% elif loop.last %}right:0{% else %}left:50%;transform:translateX(-50%){% endif %};margin-bottom:4px;background:#1e293b;border:1px solid rgba(148,163,184,0.25);border-radius:6px;padding:5px 8px;white-space:nowrap;pointer-events:none;z-index:30;box-shadow:0 4px 12px rgba(0,0,0,0.5)">
            <div style="font-size:0.6rem;font-weight:700;color:#e2e8f0">KW{{ w.kw }}</div>
            {% if not w.is_future and w.tss_ist > 0 %}<div style="font-size:0.52rem;color:#22c55e;margin-top:1px">Ist: {{ w.tss_ist }} TSS</div>{% endif %}
            {% if w.tss_plan > 0 %}<div style="font-size:0.52rem;color:#94a3b8;margin-top:1px">Plan: {{ w.tss_plan }} TSS</div>{% endif %}
          </div>
```

- [ ] **Step 4: Verify tooltip is present in template**

```bash
grep -c "class=\"tw\"" "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching/dashboard.template.html"
```

Expected: `1` (inside the loop — template shows once, renders 8 times).

- [ ] **Step 5: Commit**

```bash
git add dashboard.template.html
git commit -m "feat: add hover tooltips to TSS bar columns"
git push origin main
```

---

### Task 7: End-to-End Verifikation

**Files:** No file changes — verification only.

- [ ] **Step 1: Run generate.py locally**

```bash
cd "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching"
python3 generate.py
```

Expected: no Python errors, `docs/dashboard.html` written.

- [ ] **Step 2: Check generated HTML for hover artifacts**

```bash
grep -c "ctl-wrap\|ctl-ch\|ctl-tt" docs/dashboard.html
grep -c "sl-wrap\|sl-ch\|sl-tt" docs/dashboard.html
grep -c "class=\"tw\"" docs/dashboard.html
grep -c "bindChartHover" docs/dashboard.html
```

Expected: each returns `≥1` (actual element count may vary due to Jinja rendering).

- [ ] **Step 3: Check pts arrays rendered into JS**

```bash
grep -o '"x":[0-9.]*,"d":"[0-9.]*","v":[0-9.]*' docs/dashboard.html | head -5
```

Expected: at least 5 pts entries visible in the HTML.

- [ ] **Step 4: Trigger CI rebuild and open dashboard**

```bash
# Trigger manual rebuild via GitHub Actions (if available) or wait for hourly cron
# Dashboard URL: https://hallo-jpg.github.io/coaching-dashboard/
```

Open the dashboard and verify:
1. Hovering over CTL-Verlauf shows crosshair + tooltip with CTL value + date
2. Hovering over Schlaf-Verlauf shows crosshair + tooltip with hours + emoji + date
3. Hovering over TSS bars shows tooltip with KW, Ist TSS, Plan TSS; bar brightens on hover
4. Moving mouse off any chart hides crosshair/tooltip

- [ ] **Step 5: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: dashboard hover effects verification fixes"
git push origin main
```

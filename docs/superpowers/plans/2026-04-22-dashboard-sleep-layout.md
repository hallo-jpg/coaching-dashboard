# Dashboard Sleep Chart + Layout Restructure — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a 30-day sleep duration chart to the coaching dashboard and restructure the card layout so Wochenplan+Ernährung are near the top, CTL+Sleep are side-by-side, and Readiness+TSS are side-by-side.

**Architecture:** New Python function `get_sleep_history(days=30)` in `generate.py` (modeled exactly after `get_ctl_history()`), wired into `build_context()`. Template restructured by replacing the old `main-grid` (left-col/right-col) with a series of `two-col-grid` sections in the new order.

**Tech Stack:** Python 3, Jinja2, intervals.icu REST API (`/wellness` endpoint), SVG path strings, HTML/CSS grid.

---

## File map

| File | Change |
|---|---|
| `generate.py` | Add `get_sleep_history(days=30)` after line 799; add 5 sleep keys to `build_context()` return dict |
| `dashboard.template.html` | Replace `<!-- CTL + TSS KACHELN -->` with CTL+Sleep grid; replace `<!-- MAIN GRID -->` block with Wochenplan+Ernährung grid, Readiness+TSS grid, standalone Polar |

---

## Task 1 — Add `get_sleep_history()` to `generate.py`

**Files:**
- Modify: `generate.py` (insert after line 799, end of `get_ctl_history()`)

- [ ] **Step 1.1 — Insert the function**

  Open `generate.py`. Immediately after the closing `}` of `get_ctl_history()` (line 799), insert:

  ```python
  def get_sleep_history(days: int = 30) -> dict:
      """30-day sleep duration line for SVG. Returns path strings + today + 30d avg + day labels."""
      end = date.today()
      start = end - timedelta(days=days)
      try:
          wellness = get_wellness(start.isoformat(), end.isoformat())
      except Exception:
          return {"path": "", "fill_path": "", "sleep_today": None, "avg_30d": 0.0, "day_labels": []}

      points = []
      for w in wellness:
          if w.get("sleepSecs") and w.get("id"):
              points.append((w["id"][:10], w["sleepSecs"] / 3600))

      if not points:
          return {"path": "", "fill_path": "", "sleep_today": None, "avg_30d": 0.0, "day_labels": []}

      SLEEP_MAX = 10.0  # fixed Y-axis: 0–10h so 8h target line is always at y=16
      total_days = max((end - start).days, 1)
      SVG_W, SVG_H = 300, 80

      coords = []
      for d_str, sleep_h in points:
          d = date.fromisoformat(d_str)
          x = round((d - start).days / total_days * SVG_W, 1)
          y = round(SVG_H - (min(sleep_h, SLEEP_MAX) / SLEEP_MAX) * SVG_H, 1)
          coords.append((x, y))

      line_parts = [f"M{coords[0][0]},{coords[0][1]}"] + [f"L{x},{y}" for x, y in coords[1:]]
      line_path = " ".join(line_parts)
      fill_path = line_path + f" L{SVG_W},{SVG_H} L0,{SVG_H} Z"

      all_vals = [v for _, v in points]
      sleep_today = round(points[-1][1], 1) if points else None
      avg_30d = round(sum(all_vals) / len(all_vals), 1) if all_vals else 0.0

      # 4 labels at weekly intervals
      day_labels = []
      for ld in [0, 7, 14, 21, 28]:
          d = start + timedelta(days=ld)
          if d <= end:
              x_pct = round(ld / total_days * 100, 1)
              day_labels.append({"label": f"{d.day}. {_MONTHS_DE[d.month - 1]}", "x_pct": x_pct})

      return {
          "path": line_path,
          "fill_path": fill_path,
          "sleep_today": sleep_today,
          "avg_30d": avg_30d,
          "day_labels": day_labels,
          "last_y": coords[-1][1] if coords else 40,
      }
  ```

- [ ] **Step 1.2 — Verify syntax**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && python -c "import generate; print('OK')"
  ```

  Expected: `OK` (no errors)

- [ ] **Step 1.3 — Commit**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && \
  git add generate.py && \
  git commit -m "feat(dashboard): add get_sleep_history() – 30-day sleep SVG chart data"
  ```

---

## Task 2 — Wire `get_sleep_history()` into `build_context()`

**Files:**
- Modify: `generate.py:692–729` (`build_context()` return section)

- [ ] **Step 2.1 — Call the function and add to return dict**

  In `build_context()`, find this line (currently line 692):
  ```python
      ctl_history = get_ctl_history(weeks=26)
  ```

  Replace with:
  ```python
      ctl_history = get_ctl_history(weeks=26)
      sleep_history = get_sleep_history(days=30)
  ```

  Then in the `return {` dict (currently ends around line 729), find:
  ```python
          "ctl_history": ctl_history,
          "tss_weeks": tss_weeks,
          "tss_summary": tss_summary,
  ```

  Replace with:
  ```python
          "ctl_history": ctl_history,
          "sleep_history": sleep_history,
          "tss_weeks": tss_weeks,
          "tss_summary": tss_summary,
  ```

- [ ] **Step 2.2 — Verify build_context runs without error**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && \
  python -c "
  from generate import build_context, week_date_range
  from datetime import date
  today = date.today()
  kw = today.isocalendar()[1]
  year = today.isocalendar()[0]
  mon, sun = week_date_range(kw, year)
  ctx = build_context(kw=kw, monday=mon, sunday=sun)
  sh = ctx['sleep_history']
  print('sleep_today:', sh['sleep_today'])
  print('avg_30d:', sh['avg_30d'])
  print('day_labels:', sh['day_labels'])
  print('path_ok:', bool(sh['path']))
  print('OK')
  "
  ```

  Expected output: `sleep_today`, `avg_30d`, `day_labels` printed with real values (or None/0 if no data), then `OK`.

- [ ] **Step 2.3 — Commit**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && \
  git add generate.py && \
  git commit -m "feat(dashboard): wire sleep_history into build_context()"
  ```

---

## Task 3 — Replace CTL+TSS grid with CTL+Sleep grid in template

**Files:**
- Modify: `dashboard.template.html` (lines 468–551)

The current `<!-- CTL + TSS KACHELN -->` two-col-grid has CTL on left and TSS on right. We keep CTL unchanged and replace the TSS card with the new Sleep chart. TSS will move to a later section.

- [ ] **Step 3.1 — Replace the two-col-grid block**

  Find and replace the entire block from `<!-- CTL + TSS KACHELN -->` through the closing `</div>` of that grid (currently lines 468–551):

  **Find (old block, verbatim):**
  ```html
  <!-- CTL + TSS KACHELN -->
  <div class="two-col-grid">

    <!-- CTL-VERLAUF 6 MONATE -->
    <div class="ausblick-card" style="margin-bottom:0">
  ```

  The entire block to replace ends at:
  ```html
  </div>

  </div>

  <!-- MAIN GRID -->
  ```

  **Replace with** (CTL unchanged, TSS card replaced by Sleep card):

  ```html
  <!-- CTL + SCHLAF -->
  <div class="two-col-grid">

    <!-- CTL-VERLAUF 6 MONATE -->
    <div class="ausblick-card" style="margin-bottom:0">
      <div style="margin-bottom:14px">
        <div class="card-headline">CTL-Verlauf · 6 Monate</div>
      </div>
      {% if ctl_history.path %}
      <div style="position:relative;width:100%;height:90px;margin-bottom:30px">
        <svg width="100%" height="100%" viewBox="0 0 300 80" preserveAspectRatio="none">
          <defs>
            <linearGradient id="ctlGradFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#22c55e" stop-opacity="0.25"/>
              <stop offset="100%" stop-color="#22c55e" stop-opacity="0.02"/>
            </linearGradient>
          </defs>
          <line x1="0" y1="26" x2="300" y2="26" stroke="var(--border)" stroke-width="0.5"/>
          <line x1="0" y1="53" x2="300" y2="53" stroke="var(--border)" stroke-width="0.5"/>
          <path d="{{ ctl_history.fill_path }}" fill="url(#ctlGradFill)"/>
          <path d="{{ ctl_history.path }}" fill="none" stroke="var(--green)" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
          <circle cx="300" cy="{{ ctl_history.last_y }}" r="3" fill="var(--green)"/>
          <circle cx="300" cy="{{ ctl_history.last_y }}" r="5" fill="var(--green)" opacity="0.2"/>
        </svg>
        <div style="position:absolute;bottom:-14px;left:0;right:0">
          {% for ml in ctl_history.month_labels %}
          <span style="position:absolute;left:{{ ml.x_pct }}%;transform:translateX(-50%);font-size:0.55rem;color:var(--muted)">{{ ml.label }}</span>
          {% endfor %}
        </div>
      </div>
      <div style="text-align:center;margin-top:4px;font-size:0.7rem;color:var(--muted)">
        Aktuell: <span style="color:var(--green);font-weight:700">CTL {{ ctl_history.ctl_now }}</span>
      </div>
      {% else %}
      <div style="color:var(--muted);font-size:0.75rem;padding:16px 0;text-align:center">Keine CTL-Daten verfügbar</div>
      {% endif %}
    </div>

    <!-- SCHLAF-VERLAUF 30 TAGE -->
    <div class="ausblick-card" style="margin-bottom:0">
      <div style="margin-bottom:14px">
        <div class="card-headline">😴 Schlaf-Verlauf · 30 Tage</div>
      </div>
      {% if sleep_history.path %}
      <div style="position:relative;width:100%;height:90px;margin-bottom:30px">
        <svg width="100%" height="100%" viewBox="0 0 300 80" preserveAspectRatio="none">
          <defs>
            <linearGradient id="sleepGradFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#7986cb" stop-opacity="0.4"/>
              <stop offset="100%" stop-color="#7986cb" stop-opacity="0.0"/>
            </linearGradient>
          </defs>
          <!-- 8h Ziel-Linie: fixed axis 0–10h → y = 80-(8/10)*80 = 16 -->
          <line x1="0" y1="16" x2="300" y2="16" stroke="#4fc3f7" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.6"/>
          <text x="4" y="13" font-size="7" fill="#4fc3f7" opacity="0.7">8h Ziel</text>
          <path d="{{ sleep_history.fill_path }}" fill="url(#sleepGradFill)"/>
          <path d="{{ sleep_history.path }}" fill="none" stroke="#7986cb" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
          <circle cx="300" cy="{{ sleep_history.last_y }}" r="3" fill="#7986cb"/>
        </svg>
        <div style="position:absolute;bottom:-14px;left:0;right:0">
          {% for dl in sleep_history.day_labels %}
          <span style="position:absolute;left:{{ dl.x_pct }}%;transform:translateX(-50%);font-size:0.55rem;color:var(--muted)">{{ dl.label }}</span>
          {% endfor %}
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;margin-top:4px">
        <div>
          <div style="font-size:1.1rem;font-weight:900;color:#7986cb;line-height:1">
            {% if sleep_history.sleep_today %}{{ sleep_history.sleep_today }}h{% else %}–{% endif %}
          </div>
          <div style="font-size:0.6rem;color:var(--muted)">Heute · Schlaf</div>
        </div>
        <div style="flex:1;height:1px;background:rgba(255,255,255,0.06)"></div>
        <div style="text-align:right">
          <div style="font-size:0.85rem;font-weight:700;color:{% if sleep_history.avg_30d >= 7 %}var(--green){% else %}var(--red){% endif %}">Ø {{ sleep_history.avg_30d }}h</div>
          <div style="font-size:0.6rem;color:var(--muted)">30-Tage Schnitt</div>
        </div>
      </div>
      {% else %}
      <div style="color:var(--muted);font-size:0.75rem;padding:16px 0;text-align:center">Keine Schlafdaten verfügbar</div>
      {% endif %}
    </div>

  </div>

  <!-- MAIN GRID -->
  ```

- [ ] **Step 3.2 — Verify template renders**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && python generate.py
  ```

  Expected: `✓ docs/dashboard.html generated for KW17` (no errors)

- [ ] **Step 3.3 — Commit**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && \
  git add generate.py dashboard.template.html && \
  git commit -m "feat(dashboard): CTL+Sleep side-by-side grid, sleep chart SVG"
  ```

---

## Task 4 — Restructure MAIN GRID → Wochenplan+Ernährung / Readiness+TSS / standalone Polar

**Files:**
- Modify: `dashboard.template.html` (lines 553–730, the entire `<!-- MAIN GRID -->` block)

The old `main-grid` (left-col: Wochenplan + Polar; right-col: Readiness + Ernährung) gets replaced with three sequential blocks:
1. `two-col-grid`: Wochenplan | Ernährung
2. `two-col-grid`: Readiness | TSS-Übersicht 8 Wochen
3. Standalone `polar-card`

- [ ] **Step 4.1 — Replace the entire MAIN GRID block**

  Find the section that starts with:
  ```html
  <!-- MAIN GRID -->
  <div class="main-grid">
  ```
  and ends just before:
  ```html
  <!-- 4-WOCHEN AUSBLICK -->
  ```

  Replace the entire `<!-- MAIN GRID -->…</div>` block with:

  ```html
  <!-- WOCHENPLAN + ERNÄHRUNG -->
  <div class="two-col-grid">

    <!-- WOCHENPLAN -->
    <div class="week-card">
      <div class="week-header">
        <span class="card-headline">Wochenplan</span>
        <span class="kw-pill">KW{{ kw }}</span>
        <span class="tss-pill">{{ tss_ist }} / ~{{ tss_plan }} TSS</span>
      </div>

      {% if sick_notice %}
      <div class="sick-notice">🤒 <div><strong>{{ sick_notice }}</strong></div></div>
      {% endif %}

      {% for day in days %}
      <div class="day-row {{ day.row_class }}">
        <span class="day-name">{{ day.tag }}</span>
        <span class="day-dot {{ day.dot_class }}"></span>
        <div>
          {% if day.rest %}
          <div class="day-workout" style="color:var(--subtle);font-weight:400;">Ruhetag</div>
          {% else %}
          <div class="day-workout">{% if day.is_run %}🏃{% elif day.is_kraft %}🏋️{% else %}🚴{% endif %} {{ day.workout }}</div>
          {% endif %}
        </div>
        {% if day.rest %}
        <span class="day-tss" style="color:var(--subtle)">–</span>
        {% elif day.done %}
        <span class="day-tss" style="color:var(--green)">✅ {{ day.tss_ist }} TSS</span>
        {% else %}
        <span class="day-tss">{% if day.tss_plan > 0 %}❌ 0 TSS{% else %}–{% endif %}</span>
        {% endif %}
      </div>
      {% endfor %}
    </div>

    <!-- ERNÄHRUNG -->
    {% if nutrition %}
    <div class="nutr-card" style="margin-bottom:0">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
        <div class="card-headline">Ernährung · Heute</div>
        <span class="kw-pill" style="margin-left:auto">{{ nutrition.day_type }}</span>
      </div>

      <div class="nutr-banner nutr-banner-{{ nutrition.banner_color }}">
        <div>
          <div class="nutr-banner-text">{{ nutrition.day_label }}</div>
          <div class="nutr-banner-sub">{{ nutrition.day_sub }}</div>
        </div>
      </div>

      <div class="nutr-protein">
        <div class="nutr-protein-left">
          <div>
            <div class="nutr-protein-lbl">Protein-Ziel heute</div>
            <div><span class="nutr-protein-val">{{ nutrition.protein_g }}</span><span class="nutr-protein-unit"> g · {{ nutrition.protein_gkg }} g/kg</span></div>
          </div>
        </div>
        <div class="nutr-protein-dist">
          {% for line in nutrition.protein_dist %}{{ line }}{% if not loop.last %}<br>{% endif %}{% endfor %}
        </div>
      </div>

      {% if nutrition.pre %}
      <div class="nutr-timing">
        <div class="nutr-timing-block">
          <div class="nutr-timing-lbl">Pre-Workout</div>
          <div class="nutr-timing-main">{{ nutrition.pre.emoji }} {{ nutrition.pre.title }}</div>
          <div class="nutr-timing-sub">{{ nutrition.pre.sub }}</div>
        </div>
        <div class="nutr-timing-block">
          <div class="nutr-timing-lbl">During</div>
          <div class="nutr-timing-main">{{ nutrition.during.emoji }} {{ nutrition.during.title }}</div>
          <div class="nutr-timing-sub">{{ nutrition.during.sub }}</div>
        </div>
        <div class="nutr-timing-block">
          <div class="nutr-timing-lbl">Post · 30min</div>
          <div class="nutr-timing-main">{{ nutrition.post.emoji }} {{ nutrition.post.title }}</div>
          <div class="nutr-timing-sub">{{ nutrition.post.sub }}</div>
        </div>
      </div>
      {% endif %}

      {% if nutrition.tips %}
      <div>
        {% for tip in nutrition.tips %}
        <div class="nutr-tip">
          <div class="nutr-tip-dot nutr-tip-dot-{{ tip.color }}"></div>
          <div class="nutr-tip-text">{{ tip.text }}</div>
        </div>
        {% endfor %}
      </div>
      {% endif %}
    </div>
    {% endif %}

  </div>

  <!-- READINESS + TSS-ÜBERSICHT -->
  <div class="two-col-grid">

    <!-- READINESS -->
    <div class="readiness-card">
      <div class="card-headline" style="margin-bottom:14px">Readiness Score</div>

      <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:14px">
        <div class="readiness-score" style="color:{{ readiness_color }}">{{ readiness_score }}</div>
        <div class="readiness-tag" style="color:{{ readiness_color }}">{{ readiness_label }}</div>
      </div>

      <div style="display:flex;align-items:center;gap:10px;padding:10px;background:rgba(255,255,255,0.03);border:1px solid {{ hrv_status_color }};border-color:{{ hrv_status_color }};opacity-border:0.3;border-radius:10px;margin-bottom:10px;border-color:color-mix(in srgb,{{ hrv_status_color }} 35%,transparent)">
        <div>
          <div class="rbar-lbl" style="margin-bottom:3px">Nächtliche HRV (RMSSD)</div>
          <div style="font-size:1.4rem;font-weight:900;color:var(--text);line-height:1">{{ hrv_val }}</div>
        </div>
        <div style="margin-left:auto;text-align:right">
          <div style="font-size:0.6rem;font-weight:700;color:{{ hrv_status_color }};background:rgba(255,255,255,0.05);padding:3px 8px;border-radius:12px;margin-bottom:4px">● {{ hrv_status }}</div>
          <div class="rbar-lbl">Normalber. {{ hrv_range }} ms</div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:12px">
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center">
          <div class="rbar-lbl" style="margin-bottom:3px">Schlaf</div>
          <div style="font-size:0.85rem;font-weight:800;color:{{ sleep_color }}">{{ sleep_val }}</div>
          <div class="rbar-lbl">/ 8h</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center">
          <div class="rbar-lbl" style="margin-bottom:3px">TSB</div>
          <div style="font-size:0.85rem;font-weight:800;color:{{ tsb_bar_color }}">{{ tsb_bar_val }}</div>
          <div class="rbar-lbl">Form</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center">
          <div class="rbar-lbl" style="margin-bottom:3px">Ruhepuls</div>
          <div style="font-size:0.85rem;font-weight:800;color:var(--text)">{{ pulse_val }}</div>
          <div class="rbar-lbl">bpm</div>
        </div>
      </div>

      <div class="sparkline-wrap">
        <div class="spark-label">Readiness · 7 Tage</div>
        <div class="sparkline">
          {% for bar in sparkline %}
          <div class="spark-bar {% if loop.last %}spark-today{% endif %}" style="height:{{ bar.pct }}%;background:{{ bar.color }}"></div>
          {% endfor %}
        </div>
      </div>
    </div>

    <!-- TSS-ÜBERSICHT 8 WOCHEN -->
    <div class="ausblick-card" style="margin-bottom:0">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
        <div class="card-headline">TSS-Übersicht · 8 Wochen</div>
        <span style="font-size:0.7rem;font-weight:600;color:var(--muted)">Ø {{ tss_summary.avg_tss }} TSS</span>
      </div>

      <div style="position:relative;height:80px;margin-bottom:18px">
        <div style="position:absolute;left:0;right:0;bottom:{{ tss_summary.avg_line_pct }}%;border-top:1px dashed rgba(148,163,184,0.25);pointer-events:none;z-index:1">
          <span style="position:absolute;right:0;top:-8px;font-size:0.48rem;color:rgba(148,163,184,0.4)">Ø</span>
        </div>
        <div style="display:flex;align-items:flex-end;gap:4px;height:100%">
          {% for w in tss_weeks %}
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;position:relative">
            <span style="font-size:0.5rem;color:{{ w.label_color }};margin-bottom:2px;white-space:nowrap">
              {% if not w.is_future and w.tss_ist > 0 %}{{ w.tss_ist }}{{ w.arrow }}{% elif w.is_current %}▶{% endif %}
            </span>
            <div style="width:100%;height:{{ w.bar_height_pct }}%;background:{{ w.bar_color }};border-radius:3px 3px 0 0;{% if w.is_current %}opacity:0.55{% endif %}"></div>
            <span style="position:absolute;bottom:-14px;font-size:0.5rem;color:{% if w.is_current %}var(--text){% else %}var(--muted){% endif %}">KW{{ w.kw }}</span>
          </div>
          {% endfor %}
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px">
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
          <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Ø 8 Wochen</div>
          <div style="font-size:0.85rem;font-weight:800;color:var(--text)">{{ tss_summary.avg_tss }}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
          <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Höchste</div>
          <div style="font-size:0.85rem;font-weight:800;color:var(--yellow)">{{ tss_summary.max_tss }}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
          <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Niedrigste</div>
          <div style="font-size:0.85rem;font-weight:800;color:var(--red)">{{ tss_summary.min_tss }}</div>
        </div>
      </div>
    </div>

  </div>

  <!-- POLARISATION -->
  <div class="polar-card" style="margin-bottom:12px">
    <div class="card-headline" style="margin-bottom:14px">Polarisation · letzte 7 Tage · Rad</div>
    {% if polar_no_data %}
    <div style="color:var(--muted);font-size:0.75rem;padding:16px 0;text-align:center">Keine Rad-Aktivitäten in den letzten 7 Tagen</div>
    {% else %}
    <span class="pi-badge {% if polar_ok %}pi-ok{% else %}pi-warn{% endif %}">PI: {{ polar_pi }}% · {% if polar_ok %}✅ Grüner Bereich{% else %}⚠️ Zu viel Z3{% endif %}</span>
    <div class="polar-row">
      <span class="polar-lbl">Z1–Z2</span>
      <div class="polar-track"><div class="polar-fill" style="width:{{ polar_z12_pct }}%;background:#3a7a4a"></div></div>
      <span class="polar-pct" style="color:var(--green)">{{ polar_z12_pct }}%</span>
    </div>
    <div class="polar-row">
      <span class="polar-lbl">Z3</span>
      <div class="polar-track"><div class="polar-fill" style="width:{{ polar_z3_pct }}%;background:#7a6a2a"></div></div>
      <span class="polar-pct">{{ polar_z3_pct }}%</span>
    </div>
    <div class="polar-row">
      <span class="polar-lbl">Z4–Z7</span>
      <div class="polar-track"><div class="polar-fill" style="width:{{ polar_z47_pct }}%;background:#7040a0"></div></div>
      <span class="polar-pct" style="color:var(--subtle)">{{ polar_z47_pct }}%</span>
    </div>
    <div class="polar-note">Ziel ≥80% LIT · Z3 &lt;15% · Seiler &amp; Kjerland 2006</div>
    {% endif %}
  </div>

  ```

- [ ] **Step 4.2 — Verify template renders**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && python generate.py
  ```

  Expected: `✓ docs/dashboard.html generated for KW17` (no errors)

- [ ] **Step 4.3 — Spot-check output HTML structure**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && \
  python -c "
  html = open('docs/dashboard.html').read()
  checks = [
    ('Wochenplan+Ernährung grid', 'WOCHENPLAN + ERNÄHRUNG' in html),
    ('Sleep chart', 'Schlaf-Verlauf · 30 Tage' in html),
    ('8h Ziel line', '8h Ziel' in html),
    ('Readiness+TSS grid', 'READINESS + TSS' in html),
    ('Polarisation standalone', 'class=\"polar-card\"' in html),
    ('No old main-grid', 'class=\"main-grid\"' not in html),
    ('CTL still present', 'CTL-Verlauf · 6 Monate' in html),
  ]
  for name, ok in checks:
    print(f'{'✅' if ok else '❌'} {name}')
  "
  ```

  Expected: All 7 checks print ✅.

- [ ] **Step 4.4 — Commit**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && \
  git add dashboard.template.html && \
  git commit -m "feat(dashboard): new layout – Wochenplan+Ernährung, CTL+Sleep, Readiness+TSS, standalone Polar"
  ```

---

## Task 5 — Generate final output and push

- [ ] **Step 5.1 — Run full generation**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && python generate.py
  ```

  Expected: `✓ docs/dashboard.html generated for KW17`

- [ ] **Step 5.2 — Commit generated dashboard**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && \
  git add docs/dashboard.html && \
  git commit -m "chore: regenerate dashboard [skip ci]"
  ```

- [ ] **Step 5.3 — Push all commits**

  ```bash
  cd "/Users/stefan/Documents/Claude Code/Coaching" && git push
  ```

  Expected: `main -> main` pushed successfully.

- [ ] **Step 5.4 — Confirm dashboard rebuild triggered**

  GitHub Actions will rebuild within ~2 minutes (or the next hourly cron fires). The live dashboard at https://hallo-jpg.github.io/coaching-dashboard/ should show the new layout with the sleep chart.

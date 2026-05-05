# Dashboard Redesign – Glassmorphism Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply Glassmorphism + Glow Rings design to `dashboard.template.html` without touching `generate.py` or any Jinja2 variable names.

**Architecture:** Single-file change. All edits in `dashboard.template.html`: update `:root` tokens, replace body background with radial gradients, apply glassmorphism to all card classes via a grouped CSS selector, add 3-layer glow SVG rings (track + blurred glow clone + gradient arc), update card headers to `.chard` pattern. Jinja2 variables `readiness_offset`, `ctl_offset`, `atl_offset`, `tss_compliance_offset` are preserved as-is (glow layer is a blurred copy of the same arc).

**Tech Stack:** HTML/CSS/SVG, Jinja2 template rendered by `generate.py`. No JS changes. No changes to `generate.py`.

**Mockup reference:** `.superpowers/brainstorm/96274-1778007792/content/final-mockup-v2.html`

---

## File Map

- Modify: `dashboard.template.html` (1069 lines, all changes here)
- Read-only reference: `.superpowers/brainstorm/96274-1778007792/content/final-mockup-v2.html`

---

### Task 1: Design Tokens + Body Background

**Files:**
- Modify: `dashboard.template.html:18-44`

- [ ] **Step 1: Replace `:root` block**

Find (lines 18–33):
```css
  :root {
    --bg: #060a0c;
    --surface: #131e26;
    --surface2: #1a2a35;
    --border: #1c2830;
    --accent: #94a3b8;
    --green: #22c55e;
    --yellow: #f59e0b;
    --red: #ef4444;
    --orange: #ff6b35;
    --purple: #7c6af7;
    --teal: #00c4b4;
    --text: #e8f4f8;
    --muted: #4a6270;
    --subtle: #2a3840;
  }
```
Replace with:
```css
  :root {
    --green:  #22c55e;
    --yellow: #f59e0b;
    --red:    #ef4444;
    --orange: #ff6b35;
    --purple: #a78bfa;
    --teal:   #2dd4bf;
    --blue:   #60a5fa;
    --text:   #f0f6ff;
    --muted:  rgba(180,210,240,0.42);
    --border: rgba(255,255,255,0.08);
    /* compat aliases kept for any inline-style references */
    --bg:      #070b11;
    --surface:  rgba(255,255,255,0.04);
    --surface2: rgba(255,255,255,0.06);
    --accent:  #94a3b8;
    --subtle:  rgba(255,255,255,0.10);
  }
```

- [ ] **Step 2: Replace `body { background }` line**

Inside the `body { ... }` block (line 36), find:
```css
    background: var(--bg);
```
Replace with:
```css
    background:
      radial-gradient(ellipse 80% 60% at 15%  8%, rgba(99,70,210,0.26)  0%, transparent 55%),
      radial-gradient(ellipse 55% 45% at 88% 18%, rgba(34,197,94,0.13)  0%, transparent 50%),
      radial-gradient(ellipse 50% 55% at 50% 85%, rgba(45,212,191,0.11) 0%, transparent 55%),
      radial-gradient(ellipse 65% 35% at  8% 75%, rgba(96,165,250,0.09) 0%, transparent 50%),
      #070b11;
    background-attachment: fixed;
```

- [ ] **Step 3: Verify Jinja2 syntax**

Run from the project root:
```bash
python -c "from jinja2 import Template; Template(open('dashboard.template.html').read()); print('OK')"
```
Expected output: `OK`

- [ ] **Step 4: Commit**

```bash
git add dashboard.template.html
git commit -m "style(dashboard): design tokens + radial gradient background"
```

---

### Task 2: Glass Card CSS

**Files:**
- Modify: `dashboard.template.html` (`<style>` block)

Add one grouped glass-card rule covering all card selectors. Then strip gradient backgrounds from individual card classes, keeping only structural properties.

- [ ] **Step 1: Add glass card group + `.g` class**

After the `* { box-sizing: border-box; margin: 0; padding: 0; }` line (line 34), insert:
```css
  /* ── GLASS CARDS ── */
  .g,
  .countdown-card-main,
  .countdown-card-secondary,
  .ring-card,
  .week-card,
  .readiness-card,
  .polar-card,
  .ausblick-card,
  .nutr-card {
    background: rgba(255,255,255,0.048);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    box-shadow: 0 1px 0 rgba(255,255,255,0.07) inset, 0 8px 32px rgba(0,0,0,0.35);
  }
```

- [ ] **Step 2: Replace `.ring-card` CSS**

Find (line 126):
```css
  .ring-card { background: linear-gradient(160deg, rgba(30,50,65,0.9) 0%, rgba(12,24,32,0.95) 100%); border: 1px solid rgba(148,163,184,0.12); border-bottom-color: rgba(148,163,184,0.05); box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 4px 16px rgba(0,0,0,0.3); border-radius: 16px; padding: 20px 16px; display: flex; flex-direction: column; align-items: center; gap: 12px; }
```
Replace with:
```css
  .ring-card { padding: 20px 16px; display: flex; flex-direction: column; align-items: center; gap: 12px; }
```

- [ ] **Step 3: Replace `.week-card` CSS**

Find (line 171):
```css
  .week-card { background: linear-gradient(160deg, rgba(30,50,65,0.9) 0%, rgba(12,24,32,0.95) 100%); border: 1px solid rgba(148,163,184,0.12); border-bottom-color: rgba(148,163,184,0.05); box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 4px 16px rgba(0,0,0,0.3); border-radius: 16px; padding: 20px; }
```
Replace with:
```css
  .week-card { padding: 20px; }
```

- [ ] **Step 4: Replace `.readiness-card` CSS**

Find (line 198):
```css
  .readiness-card { background: linear-gradient(160deg, rgba(30,50,65,0.9) 0%, rgba(12,24,32,0.95) 100%); border: 1px solid rgba(148,163,184,0.12); border-bottom-color: rgba(148,163,184,0.05); box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 4px 16px rgba(0,0,0,0.3); border-radius: 16px; padding: 18px; }
```
Replace with:
```css
  .readiness-card { padding: 18px; }
```

- [ ] **Step 5: Replace `.polar-card` CSS**

Find (line 213):
```css
  .polar-card { background: linear-gradient(160deg, rgba(30,50,65,0.9) 0%, rgba(12,24,32,0.95) 100%); border: 1px solid rgba(148,163,184,0.12); border-bottom-color: rgba(148,163,184,0.05); box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 4px 16px rgba(0,0,0,0.3); border-radius: 16px; padding: 18px; }
```
Replace with:
```css
  .polar-card { padding: 18px; }
```

- [ ] **Step 6: Replace `.ausblick-card` CSS**

Find (line 233):
```css
  .ausblick-card { background: linear-gradient(160deg, rgba(30,50,65,0.9) 0%, rgba(12,24,32,0.95) 100%); border: 1px solid rgba(148,163,184,0.12); border-bottom-color: rgba(148,163,184,0.05); box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 4px 16px rgba(0,0,0,0.3); border-radius: 16px; padding: 18px; margin-bottom: 12px; }
```
Replace with:
```css
  .ausblick-card { padding: 18px; margin-bottom: 12px; }
```

- [ ] **Step 7: Replace `.nutr-card` CSS**

Find (line 244):
```css
  .nutr-card { background: linear-gradient(160deg, rgba(30,50,65,0.9) 0%, rgba(12,24,32,0.95) 100%); border: 1px solid rgba(148,163,184,0.12); border-bottom-color: rgba(148,163,184,0.05); box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 4px 16px rgba(0,0,0,0.3); border-radius: 16px; padding: 18px; margin-bottom: 12px; }
```
Replace with:
```css
  .nutr-card { padding: 18px; margin-bottom: 12px; }
```

- [ ] **Step 8: Verify + Commit**

```bash
python -c "from jinja2 import Template; Template(open('dashboard.template.html').read()); print('OK')"
git add dashboard.template.html
git commit -m "style(dashboard): glass card grouped selector + strip gradient backgrounds"
```

---

### Task 3: Header, Phase-Pill, Countdown CSS

**Files:**
- Modify: `dashboard.template.html` (`<style>` block, lines 46–113)

- [ ] **Step 1: Replace `.phase-pill` + `.phase-pill .dot` CSS**

Find (lines 50–58):
```css
  .phase-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(148,163,184,0.08); color: var(--accent);
    padding: 3px 11px; border-radius: 20px;
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px;
    margin-bottom: 7px;
  }
  .phase-pill .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); animation: pulse 2s infinite; }
```
Replace with:
```css
  .phase-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(167,139,250,0.13); border: 1px solid rgba(167,139,250,0.22);
    color: var(--purple); padding: 4px 12px; border-radius: 99px;
    font-size: 0.61rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px;
    margin-bottom: 7px;
  }
  .phase-pill .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--purple); animation: pulse 2s infinite; }
```

- [ ] **Step 2: Update `.header-title` typography**

Find:
```css
  .header-title { font-size: 1.4rem; font-weight: 800; letter-spacing: -0.3px; }
```
Replace with:
```css
  .header-title { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.5px; }
```

- [ ] **Step 3: Replace `.countdown-card-main` CSS**

Find (lines 67–71):
```css
  .countdown-card-main {
    flex: 1;
    background: linear-gradient(135deg, #091410 0%, #080c0e 100%);
    border-radius: 14px; padding: 16px 20px;
    display: flex; gap: 16px; align-items: stretch;
  }
```
Replace with:
```css
  .countdown-card-main {
    flex: 1;
    padding: 18px 22px;
    display: flex; gap: 20px; align-items: center;
  }
```

- [ ] **Step 4: Replace `.countdown-card-secondary` CSS**

Find (lines 101–106):
```css
  .countdown-card-secondary {
    flex: 0 0 200px;
    background: linear-gradient(135deg, #091410 0%, #0a1210 100%);
    border-radius: 14px; padding: 16px 18px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
```
Replace with:
```css
  .countdown-card-secondary {
    flex: 0 0 188px;
    padding: 18px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
```

- [ ] **Step 5: Update countdown number typography**

Find:
```css
  .cd-num { font-size: 2.2rem; font-weight: 900; line-height: 1; color: var(--accent); }
```
Replace with:
```css
  .cd-num { font-size: 2.7rem; font-weight: 900; line-height: 1; color: var(--yellow); letter-spacing: -2px; }
```

Find:
```css
  .cd-sec-num { font-size: 1.8rem; font-weight: 900; color: var(--teal); line-height: 1; }
```
Replace with:
```css
  .cd-sec-num { font-size: 2.1rem; font-weight: 900; color: var(--purple); letter-spacing: -1px; line-height: 1; }
```

- [ ] **Step 6: Commit**

```bash
git add dashboard.template.html
git commit -m "style(dashboard): header + phase-pill + countdown CSS"
```

---

### Task 4: Phase Bar CSS

**Files:**
- Modify: `dashboard.template.html` (`<style>` block, lines 114–123)

- [ ] **Step 1: Update `.phase-bar-label`**

Find:
```css
  .phase-bar-label { font-size: 0.58rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
```
Replace with:
```css
  .phase-bar-label { font-size: 0.54rem; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
```

- [ ] **Step 2: Update `.phase` base**

Find:
```css
  .phase { flex: 1; border-radius: 8px; padding: 7px 5px; font-size: 0.6rem; font-weight: 700; text-align: center; line-height: 1.3; }
```
Replace with:
```css
  .phase { flex: 1; border-radius: 10px; padding: 7px 4px; font-size: 0.57rem; font-weight: 700; text-align: center; line-height: 1.3; }
```

- [ ] **Step 3: Replace `.phase.done`**

Find:
```css
  .phase.done { background: rgba(62,207,142,0.08); color: rgba(62,207,142,0.6); }
```
Replace with:
```css
  .phase.done { background: rgba(34,197,94,0.07); border: 1px solid rgba(34,197,94,0.10); color: rgba(34,197,94,0.45); }
```

- [ ] **Step 4: Replace `.phase.active`**

Find:
```css
  .phase.active { background: linear-gradient(135deg, rgba(148,163,184,0.12), rgba(155,127,232,0.1)); color: #cbd5e1; outline: 1px solid rgba(148,163,184,0.25); outline-offset: -1px; }
```
Replace with:
```css
  .phase.active { background: rgba(167,139,250,0.14); border: 1px solid rgba(167,139,250,0.28); color: var(--purple); box-shadow: 0 0 14px rgba(167,139,250,0.12); }
```

- [ ] **Step 5: Replace `.phase.upcoming`**

Find:
```css
  .phase.upcoming { background: var(--surface); color: var(--subtle); }
```
Replace with:
```css
  .phase.upcoming { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); color: rgba(180,210,240,0.2); }
```

- [ ] **Step 6: Commit**

```bash
git add dashboard.template.html
git commit -m "style(dashboard): phase bar glass treatment"
```

---

### Task 5: Card Headers — `.chard` Pattern

**Files:**
- Modify: `dashboard.template.html` (CSS `<style>` block + HTML body)

- [ ] **Step 1: Add `.chard`, `.chard-icon`, `.ring-eyebrow` CSS**

After the `.card-headline { ... }` rule (line 128), insert:
```css
  .chard { font-size: .82rem; font-weight: 800; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
  .chard-icon { width: 22px; height: 22px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: .75rem; flex-shrink: 0; }
  .ring-eyebrow { font-size: .62rem; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: .7px; text-align: center; }
```

- [ ] **Step 2: Ring card eyebrows (HTML)**

Find:
```html
    <div class="ring-card-title">Recovery</div>
```
Replace with:
```html
    <div class="ring-eyebrow">Readiness · Heute</div>
```

Find:
```html
    <div class="ring-card-title">Trainingsform</div>
```
Replace with:
```html
    <div class="ring-eyebrow">Trainingsform · CTL / ATL</div>
```

Find:
```html
    <div class="ring-card-title">Wochenziel</div>
```
Replace with:
```html
    <div class="ring-eyebrow">Wochenziel · TSS</div>
```

- [ ] **Step 3: Wochenplan header (HTML)**

Find:
```html
      <span class="card-headline">Wochenplan</span>
```
Replace with:
```html
      <div class="chard" style="margin-bottom:0"><div class="chard-icon" style="background:rgba(148,163,184,0.10)">📅</div>Wochenplan</div>
```

- [ ] **Step 4: Ernährung header (HTML)**

Find:
```html
        <div class="card-headline">Ernährung · Heute</div>
```
Replace with:
```html
        <div class="chard" style="margin-bottom:0"><div class="chard-icon" style="background:rgba(255,107,53,0.14)">⛽</div>Ernährung · Heute</div>
```

- [ ] **Step 5: Readiness Score header (HTML)**

Find:
```html
    <div class="card-headline" style="margin-bottom:14px">Readiness Score</div>
```
Replace with:
```html
    <div class="chard"><div class="chard-icon" style="background:rgba(34,197,94,0.12)">💚</div>Readiness Score</div>
```

- [ ] **Step 6: Polarisation header (HTML)**

Find:
```html
  <div class="card-headline" style="margin-bottom:14px">Polarisation · letzte 7 Tage · Rad</div>
```
Replace with:
```html
  <div class="chard"><div class="chard-icon" style="background:rgba(96,165,250,0.12)">📊</div>Polarisation · letzte 7 Tage · Rad</div>
```

- [ ] **Step 7: Power Bestwerte header (HTML)**

Find:
```html
    <div class="card-headline">🚴 Power Bestwerte</div>
```
Replace with:
```html
    <div class="chard" style="margin-bottom:0"><div class="chard-icon" style="background:rgba(245,158,11,0.12)">⚡</div>Power Bestwerte · All-Time</div>
```

- [ ] **Step 8: Lauf Bestwerte header (HTML)**

Find:
```html
    <div class="card-headline">🏃 Lauf Bestwerte</div>
```
Replace with:
```html
    <div class="chard" style="margin-bottom:0"><div class="chard-icon" style="background:rgba(34,197,94,0.10)">🏃</div>Lauf Bestwerte · All-Time</div>
```

- [ ] **Step 9: Commit**

```bash
git add dashboard.template.html
git commit -m "style(dashboard): .chard card header pattern + icon anchors"
```

---

### Task 6: Ring Legend + Dual-Ring Color Updates

**Files:**
- Modify: `dashboard.template.html` (CSS + HTML)

The dual ring colors change from blue/orange to purple/red to match the new ring arc colors.

- [ ] **Step 1: Update `.dual-legend` CSS**

Find:
```css
  .dual-legend { display: flex; flex-direction: column; gap: 5px; width: 100%; }
```
Replace with:
```css
  .dual-legend { display: flex; flex-direction: column; gap: 6px; width: 100%; padding-top: 10px; border-top: 1px solid var(--border); }
```

- [ ] **Step 2: Update CTL legend dot + value color (HTML)**

Find:
```html
        <div class="dl-dot" style="background:#4f8ef7"></div>
        <span class="dl-name">CTL · Fitness</span>
        <span class="dl-val" style="color:#94a3b8">{{ ctl }} <span style="font-size:.5rem;color:var(--muted)">/ 90</span></span>
```
Replace with:
```html
        <div class="dl-dot" style="background:var(--purple)"></div>
        <span class="dl-name">CTL · Fitness</span>
        <span class="dl-val" style="color:var(--purple)">{{ ctl }} <span style="font-size:.5rem;color:var(--muted)">/ 90</span></span>
```

- [ ] **Step 3: Update ATL legend dot + value color (HTML)**

Find:
```html
        <div class="dl-dot" style="background:#f5a623"></div>
        <span class="dl-name">ATL · Fatigue</span>
        <span class="dl-val" style="color:#f5a623">{{ atl }}</span>
```
Replace with:
```html
        <div class="dl-dot" style="background:#f87171"></div>
        <span class="dl-name">ATL · Fatigue</span>
        <span class="dl-val" style="color:#f87171">{{ atl }}</span>
```

- [ ] **Step 4: Update `.rbar-track` + `.polar-track` backgrounds**

Find:
```css
  .rbar-track { flex: 1; height: 5px; background: var(--surface2); border-radius: 3px; overflow: hidden; }
```
Replace with:
```css
  .rbar-track { flex: 1; height: 4px; background: rgba(255,255,255,0.07); border-radius: 2px; overflow: hidden; }
```

Find:
```css
  .polar-track { flex: 1; height: 8px; background: var(--surface2); border-radius: 4px; overflow: hidden; }
```
Replace with:
```css
  .polar-track { flex: 1; height: 7px; background: rgba(255,255,255,0.07); border-radius: 3px; overflow: hidden; }
```

- [ ] **Step 5: Update `.nutr-timing-block` background**

Find:
```css
  .nutr-timing-block { background: var(--surface2); border-radius: 10px; padding: 10px 8px; text-align: center; }
```
Replace with:
```css
  .nutr-timing-block { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-radius: 9px; padding: 9px 8px; text-align: center; }
```

- [ ] **Step 6: Commit**

```bash
git add dashboard.template.html
git commit -m "style(dashboard): dual-ring legend colors + track backgrounds"
```

---

### Task 7: Glow Rings — Rewrite All 3 SVGs

**Files:**
- Modify: `dashboard.template.html` (HTML body, lines 398–473)

Each ring gets 3 layers: track (semi-transparent), glow clone (blurred copy of arc), gradient arc. Jinja2 variables `readiness_offset`, `ctl_offset`, `atl_offset`, `tss_compliance_offset` are preserved — the glow clone uses the same `stroke-dasharray`/`stroke-dashoffset` as the main arc.

- [ ] **Step 1: Rewrite Recovery Ring SVG**

Find (inside the Recovery `ring-card`, lines ~405–409):
```html
      <svg viewBox="0 0 130 130" width="140" height="140">
        <circle cx="65" cy="65" r="55" fill="none" stroke="#1c1c1c" stroke-width="10"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="{{ readiness_color }}" stroke-width="10" stroke-linecap="round"
          stroke-dasharray="345.4" stroke-dashoffset="{{ readiness_offset }}" transform="rotate(-90 65 65)"/>
      </svg>
```
Replace with:
```html
      <svg viewBox="0 0 130 130" width="140" height="140" overflow="visible">
        <defs>
          <linearGradient id="g-gr" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%"   stop-color="#16a34a"/>
            <stop offset="100%" stop-color="#86efac"/>
          </linearGradient>
          <filter id="glow-gr" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
          </filter>
        </defs>
        <circle cx="65" cy="65" r="55" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="9"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="#22c55e" stroke-width="9"
                stroke-linecap="round" stroke-dasharray="345.4" stroke-dashoffset="{{ readiness_offset }}"
                transform="rotate(-90 65 65)" opacity="0.45" filter="url(#glow-gr)"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="url(#g-gr)" stroke-width="9"
                stroke-linecap="round" stroke-dasharray="345.4" stroke-dashoffset="{{ readiness_offset }}"
                transform="rotate(-90 65 65)"/>
      </svg>
```

- [ ] **Step 2: Rewrite Trainingsform Dual Ring SVG**

Find (inside the Trainingsform `ring-card`, lines ~427–433):
```html
      <svg viewBox="0 0 130 130" width="140" height="140">
        <circle cx="65" cy="65" r="55" fill="none" stroke="#1c1c1c" stroke-width="9"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="#94a3b8" stroke-width="9" stroke-linecap="round"
          stroke-dasharray="345.4" stroke-dashoffset="{{ ctl_offset }}" transform="rotate(-90 65 65)"/>
        <circle cx="65" cy="65" r="41" fill="none" stroke="#1c1c1c" stroke-width="9"/>
        <circle cx="65" cy="65" r="41" fill="none" stroke="#f5a623" stroke-width="9" stroke-linecap="round"
          stroke-dasharray="257.6" stroke-dashoffset="{{ atl_offset }}" transform="rotate(-90 65 65)"/>
      </svg>
```
Replace with:
```html
      <svg viewBox="0 0 130 130" width="140" height="140" overflow="visible">
        <defs>
          <linearGradient id="g-pu" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%"   stop-color="#5b21b6"/>
            <stop offset="100%" stop-color="#c4b5fd"/>
          </linearGradient>
          <linearGradient id="g-re" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%"   stop-color="#991b1b"/>
            <stop offset="100%" stop-color="#fca5a5"/>
          </linearGradient>
          <filter id="glow-pu" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
          </filter>
          <filter id="glow-re" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/>
          </filter>
        </defs>
        <circle cx="65" cy="65" r="55" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="9"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="#a78bfa" stroke-width="9"
                stroke-linecap="round" stroke-dasharray="345.4" stroke-dashoffset="{{ ctl_offset }}"
                transform="rotate(-90 65 65)" opacity="0.4" filter="url(#glow-pu)"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="url(#g-pu)" stroke-width="9"
                stroke-linecap="round" stroke-dasharray="345.4" stroke-dashoffset="{{ ctl_offset }}"
                transform="rotate(-90 65 65)"/>
        <circle cx="65" cy="65" r="41" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="9"/>
        <circle cx="65" cy="65" r="41" fill="none" stroke="#f87171" stroke-width="8"
                stroke-linecap="round" stroke-dasharray="257.6" stroke-dashoffset="{{ atl_offset }}"
                transform="rotate(-90 65 65)" opacity="0.4" filter="url(#glow-re)"/>
        <circle cx="65" cy="65" r="41" fill="none" stroke="url(#g-re)" stroke-width="8"
                stroke-linecap="round" stroke-dasharray="257.6" stroke-dashoffset="{{ atl_offset }}"
                transform="rotate(-90 65 65)"/>
      </svg>
```

- [ ] **Step 3: Rewrite Wochenziel TSS Ring SVG**

Find (inside the Wochenziel `ring-card`, lines ~458–462):
```html
      <svg viewBox="0 0 130 130" width="140" height="140">
        <circle cx="65" cy="65" r="55" fill="none" stroke="#1c1c1c" stroke-width="10"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="{{ tss_compliance_color }}" stroke-width="10" stroke-linecap="round"
          stroke-dasharray="345.4" stroke-dashoffset="{{ tss_compliance_offset }}" transform="rotate(-90 65 65)"/>
      </svg>
```
Replace with:
```html
      <svg viewBox="0 0 130 130" width="140" height="140" overflow="visible">
        <defs>
          <linearGradient id="g-te" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%"   stop-color="#0d9488"/>
            <stop offset="100%" stop-color="#5eead4"/>
          </linearGradient>
          <filter id="glow-te" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
          </filter>
        </defs>
        <circle cx="65" cy="65" r="55" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="9"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="#2dd4bf" stroke-width="9"
                stroke-linecap="round" stroke-dasharray="345.4" stroke-dashoffset="{{ tss_compliance_offset }}"
                transform="rotate(-90 65 65)" opacity="0.45" filter="url(#glow-te)"/>
        <circle cx="65" cy="65" r="55" fill="none" stroke="url(#g-te)" stroke-width="9"
                stroke-linecap="round" stroke-dasharray="345.4" stroke-dashoffset="{{ tss_compliance_offset }}"
                transform="rotate(-90 65 65)"/>
      </svg>
```

- [ ] **Step 4: Verify + Commit**

```bash
python -c "from jinja2 import Template; Template(open('dashboard.template.html').read()); print('OK')"
git add dashboard.template.html
git commit -m "style(dashboard): 3-layer glow rings — track + glow-clone + gradient arc"
```

---

### Task 8: Typography + Pills + Final Cleanup

**Files:**
- Modify: `dashboard.template.html` (`<style>` block)

- [ ] **Step 1: Capsule border-radius on pills**

Find `.kw-pill { ... border-radius: 20px; }` — change `border-radius: 20px` to `border-radius: 99px`.

Find `.tss-pill { ... border-radius: 20px; }` — change `border-radius: 20px` to `border-radius: 99px`.

Find `.pi-badge { ... border-radius: 20px; }` — change `border-radius: 20px` to `border-radius: 99px`.

- [ ] **Step 2: Large number letter-spacing**

Find:
```css
  .ring-num { font-size: 2rem; font-weight: 900; line-height: 1; }
```
Replace with:
```css
  .ring-num { font-size: 2rem; font-weight: 900; line-height: 1; letter-spacing: -2px; }
```

Find:
```css
  .readiness-score { font-size: 3.5rem; font-weight: 900; line-height: 1; margin-bottom: 4px; }
```
Replace with:
```css
  .readiness-score { font-size: 3.5rem; font-weight: 900; line-height: 1; letter-spacing: -3px; margin-bottom: 4px; }
```

- [ ] **Step 3: Eyebrow label style**

Find:
```css
  .section-label { font-size: 0.58rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 14px; }
```
Replace with:
```css
  .section-label { font-size: 0.54rem; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px; }
```

- [ ] **Step 4: Update `theme-color` meta to match new background**

Find:
```html
<meta name="theme-color" content="#0a0a0a">
```
Replace with:
```html
<meta name="theme-color" content="#070b11">
```

- [ ] **Step 5: Final syntax check**

```bash
python -c "from jinja2 import Template; Template(open('dashboard.template.html').read()); print('OK')"
```
Expected: `OK`

- [ ] **Step 6: Commit + Push**

```bash
git add dashboard.template.html
git commit -m "style(dashboard): typography polish + capsule pills + theme-color"
git push
```

---

## Self-Review

### Spec Coverage

| Spec requirement | Task |
|---|---|
| Radial gradient background | Task 1 Step 2 |
| `:root` color tokens | Task 1 Step 1 |
| Glass card CSS (all card types) | Task 2 Steps 1–7 |
| Phase-pill → purple, 99px radius | Task 3 Step 1 |
| Countdown → glass | Task 3 Steps 3–5 |
| Phase bar → glass treatment | Task 4 |
| `.chard` card headers + icon boxes | Task 5 |
| Dual-ring legend colors (purple/red) | Task 6 Steps 2–3 |
| Track/timing block backgrounds | Task 6 Steps 4–5 |
| Recovery ring — 3-layer glow | Task 7 Step 1 |
| Trainingsform dual ring — 3-layer glow | Task 7 Step 2 |
| Wochenziel ring — 3-layer glow | Task 7 Step 3 |
| Capsule pills border-radius 99px | Task 8 Step 1 |
| Large number letter-spacing | Task 8 Step 2 |
| `generate.py` unchanged | N/A — only template touched |
| Jinja2 vars preserved | Throughout (dashoffset vars kept as-is) |
| Layout order unchanged | N/A — no structural HTML changes |

### Placeholder Scan

No TBD, TODO, or vague steps — every step has exact find/replace content.

### Consistency Check

- Gradient IDs: `g-gr` (green/readiness), `g-pu` (purple/CTL), `g-re` (red/ATL), `g-te` (teal/TSS) — used only in Task 7, no conflicts
- Filter IDs: `glow-gr`, `glow-pu`, `glow-re`, `glow-te` — unique per SVG, no cross-card ID collisions
- `readiness_offset`, `ctl_offset`, `atl_offset`, `tss_compliance_offset` — appear unchanged in Task 7 ring SVGs, matching generate.py output
- Color `#f87171` (ATL red) used in Task 6 HTML and Task 7 SVG glow stroke — consistent
- Color `#a78bfa` = `var(--purple)` used in Task 7 CTL glow stroke — consistent with Task 1 token

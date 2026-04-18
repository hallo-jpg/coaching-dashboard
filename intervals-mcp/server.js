import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

// Load .env manually (no dotenv ESM issues)
const __dirname = dirname(fileURLToPath(import.meta.url));
const envPath = join(__dirname, ".env");
const envContent = readFileSync(envPath, "utf8");
for (const line of envContent.split("\n")) {
  const [key, val] = line.split("=");
  if (key && val) process.env[key.trim()] = val.trim();
}

const API_KEY = process.env.INTERVALS_API_KEY;
const ATHLETE_ID = process.env.INTERVALS_ATHLETE_ID;
const BASE_URL = `https://intervals.icu/api/v1/athlete/${ATHLETE_ID}`;
const AUTH = "Basic " + Buffer.from(`API_KEY:${API_KEY}`).toString("base64");

async function apiFetch(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      Authorization: AUTH,
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`intervals.icu API error ${res.status}: ${text}`);
  }
  return res.json();
}

function today() {
  return new Date().toISOString().split("T")[0];
}

function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().split("T")[0];
}

// ────────────────────────────────────────────────────────────
// MCP Server setup
// ────────────────────────────────────────────────────────────

const server = new McpServer({
  name: "intervals-icu",
  version: "1.0.0",
});

// ── Tool 1: Aktuelle Fitness (CTL/ATL/TSB + HRV) ────────────
server.tool(
  "get_current_fitness",
  "Aktuelle Fitness-Metriken: CTL, ATL, TSB (Form), HRV, Ruhepuls, Schlaf. Liefert die letzten 7 Tage.",
  {},
  async () => {
    const oldest = daysAgo(7);
    const newest = today();
    const data = await apiFetch(
      `/wellness?oldest=${oldest}&newest=${newest}`
    );
    if (!data.length) return { content: [{ type: "text", text: "Keine Wellness-Daten gefunden." }] };

    const latest = data[data.length - 1];
    const tsb = latest.ctl && latest.atl ? (latest.ctl - latest.atl).toFixed(1) : "n/a";

    const summary = {
      datum: latest.id,
      CTL: latest.ctl?.toFixed(1) ?? "n/a",
      ATL: latest.atl?.toFixed(1) ?? "n/a",
      TSB: tsb,
      HRV: latest.hrv ?? "n/a",
      Ruhepuls: latest.restingHR ?? "n/a",
      Schlaf_h: latest.sleepSecs ? (latest.sleepSecs / 3600).toFixed(1) : "n/a",
      Verlauf_7Tage: data.map(d => ({
        datum: d.id,
        ctl: d.ctl?.toFixed(1),
        atl: d.atl?.toFixed(1),
        tsb: d.ctl && d.atl ? (d.ctl - d.atl).toFixed(1) : null,
        hrv: d.hrv,
        schlaf_h: d.sleepSecs ? (d.sleepSecs / 3600).toFixed(1) : null,
      }))
    };

    return {
      content: [{ type: "text", text: JSON.stringify(summary, null, 2) }],
    };
  }
);

// ── Tool 2: Aktivitäten ──────────────────────────────────────
server.tool(
  "get_recent_activities",
  "Letzte Aktivitäten (Rad + Lauf) mit TSS, Watt, HF, Dauer. Für Wochen-Review.",
  {
    days: z.number().optional().describe("Wie viele Tage zurückschauen (default: 14)"),
  },
  async ({ days = 14 }) => {
    const oldest = daysAgo(days);
    const newest = today();
    const data = await apiFetch(
      `/activities?oldest=${oldest}&newest=${newest}`
    );

    if (!data.length) return { content: [{ type: "text", text: "Keine Aktivitäten gefunden." }] };

    const activities = data.map(a => ({
      datum: a.start_date_local?.split("T")[0],
      typ: a.type,
      name: a.name,
      dauer_min: a.moving_time ? Math.round(a.moving_time / 60) : null,
      distanz_km: a.distance ? (a.distance / 1000).toFixed(1) : null,
      tss: a.icu_training_load,
      avg_watt: a.icu_weighted_avg_watts,
      avg_hf: a.average_heartrate,
      max_hf: a.max_heartrate,
      ctl_danach: a.icu_ctl?.toFixed(1),
      atl_danach: a.icu_atl?.toFixed(1),
    }));

    return {
      content: [{ type: "text", text: JSON.stringify(activities, null, 2) }],
    };
  }
);

// ── Tool 3: Geplante Events lesen ───────────────────────────
server.tool(
  "get_planned_events",
  "Geplante Trainingseinheiten für eine Woche aus dem intervals.icu Kalender.",
  {
    oldest: z.string().describe("Startdatum YYYY-MM-DD"),
    newest: z.string().describe("Enddatum YYYY-MM-DD"),
  },
  async ({ oldest, newest }) => {
    const data = await apiFetch(`/events?oldest=${oldest}&newest=${newest}`);
    return {
      content: [{ type: "text", text: JSON.stringify(data, null, 2) }],
    };
  }
);

// ── Hilfsfunktion: .zwo XML generieren ──────────────────────
function buildZwo(name, description, steps) {
  const xmlSteps = steps.map(s => {
    const p = (v) => (v / 100).toFixed(3);
    if (s.warmup) {
      return `    <Warmup Duration="${s.duration_secs}" PowerLow="${p(s.power_pct_low ?? 40)}" PowerHigh="${p(s.power_pct_high ?? s.power_pct ?? 55)}"/>`;
    } else if (s.cooldown) {
      return `    <Cooldown Duration="${s.duration_secs}" PowerLow="${p(s.power_pct_end ?? s.power_pct ?? 40)}" PowerHigh="${p(s.power_pct_start ?? s.power_pct ?? 55)}"/>`;
    } else if (s.reps) {
      return `    <IntervalsT Repeat="${s.reps}" OnDuration="${s.steps[0].duration_secs}" OffDuration="${s.steps[1]?.duration_secs ?? 60}" OnPower="${p(s.steps[0].power_pct ?? 100)}" OffPower="${p(s.steps[1]?.power_pct ?? 50)}"/>`;
    } else {
      return `    <SteadyState Duration="${s.duration_secs}" Power="${p(s.power_pct ?? 55)}"/>`;
    }
  }).join("\n");

  return `<?xml version="1.0" encoding="utf-8"?>
<workout_file>
  <author>Coach Claude</author>
  <name>${name}</name>
  <description>${description ?? ""}</description>
  <sportType>bike</sportType>
  <workout>
${xmlSteps}
  </workout>
</workout_file>`;
}

// ── Tool 4: Workout einplanen ────────────────────────────────
server.tool(
  "create_planned_workout",
  "Plant ein Workout im intervals.icu Kalender. Rad-Workouts aus der Bibliothek via zwo_file_path (absoluter Pfad zur .zwo-Datei), dynamisch via workout_steps, oder Lauf/Kraft via Description-Format.",
  {
    date: z.string().describe("Datum YYYY-MM-DD"),
    type: z.enum(["Ride", "Run", "WeightTraining", "Other"]).describe("Aktivitätstyp"),
    name: z.string().describe("Name des Workouts"),
    description: z.string().optional().describe("Freitext-Beschreibung"),
    fueling_note: z.string().optional().describe("Fueling-Hinweis als separate Note im Kalender, z.B. '⛽ 40g/h Malto\\n🍽 Frühstück 90min vorher'. Wird als eigenes NOTE-Event am gleichen Tag angelegt."),
    duration_secs: z.number().optional().describe("Gesamtdauer in Sekunden"),
    tss: z.number().optional().describe("Geplanter TSS"),
    zwo_file_path: z.string().optional().describe("Absoluter Pfad zur .zwo-Datei aus der Workout-Library, z.B. '/Users/stefan/Documents/Claude Code/Coaching/Workout-Library/LIT-2h.zwo'. Wird server-seitig gelesen und als base64 hochgeladen – kein curl, kein API-Key im Skill nötig."),
    workout_steps: z.array(z.object({
      duration_secs: z.number().describe("Dauer in Sekunden"),
      power_pct: z.number().optional().describe("Zielwatt % FTP (Rad), z.B. 55"),
      power_pct_low: z.number().optional().describe("% FTP untere Grenze für Warmup/Cooldown"),
      power_pct_high: z.number().optional().describe("% FTP obere Grenze für Warmup/Cooldown"),
      pace_pct: z.number().optional().describe("% Schwellenpace (Lauf), z.B. 100 für Schwelle"),
      pace_pct_low: z.number().optional().describe("% Schwellenpace untere Grenze (Lauf), z.B. 70 für leicht"),
      pace_pct_high: z.number().optional().describe("% Schwellenpace obere Grenze (Lauf), z.B. 80 für Einlaufen"),
      warmup: z.boolean().optional(),
      cooldown: z.boolean().optional(),
      reps: z.number().optional().describe("Wiederholungen für Intervallblock"),
      steps: z.array(z.object({
        duration_secs: z.number(),
        power_pct: z.number().optional(),
      })).optional().describe("Schritte innerhalb Intervallblock"),
      text: z.string().optional(),
    })).optional(),
  },
  async ({ date, type, name, description, fueling_note, duration_secs, tss, zwo_file_path, workout_steps }) => {

    // Hilfsfunktion: Fueling-Note als separates Event anlegen
    async function createFuelingNote(noteText) {
      await apiFetch("/events", {
        method: "POST",
        body: JSON.stringify({
          start_date_local: `${date}T00:00:00`,
          type: "Note",
          category: "NOTE",
          name: `⛽ Fueling – ${name}`,
          description: noteText,
          show_as_note: true,
        }),
      });
    }

    // Rad-Workouts: .zwo-Bibliotheksdatei via Pfad (kein curl, kein API-Key im Skill)
    if (type === "Ride" && zwo_file_path) {
      const fileBytes = readFileSync(zwo_file_path);
      const b64 = fileBytes.toString("base64");
      const payload = [{
        start_date_local: `${date}T00:00:00`,
        type: "Ride",
        category: "WORKOUT",
        name,
        description: description ?? "",
        filename: zwo_file_path.split("/").pop(),
        file_contents_base64: b64,
      }];
      if (tss) payload[0].icu_training_load = tss;
      if (duration_secs) payload[0].moving_time = duration_secs;

      const url = `https://intervals.icu/api/v1/athlete/${ATHLETE_ID}/events/bulk?upsert=true`;
      const res = await fetch(url, {
        method: "POST",
        headers: { Authorization: AUTH, "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const result = await res.json();
      if (fueling_note) await createFuelingNote(fueling_note);
      return {
        content: [{ type: "text", text: `✅ Bibliotheks-Workout hochgeladen (${zwo_file_path.split("/").pop()}) · ID: ${result[0]?.id}\nzoneTimes: ${result[0]?.workout_doc?.zoneTimes ? "✅" : "❌"}${fueling_note ? "\n📝 Fueling-Note angelegt" : ""}` }],
      };
    }

    // Rad-Workouts: dynamisch via workout_steps → buildZwo
    if (type === "Ride" && workout_steps?.length) {
      const zwoXml = buildZwo(name, description, workout_steps);
      const b64 = Buffer.from(zwoXml).toString("base64");
      const payload = [{
        start_date_local: `${date}T00:00:00`,
        type: "Ride",
        category: "WORKOUT",
        name,
        description: description ?? "",
        filename: `${name.replace(/[^a-z0-9]/gi, "_")}.zwo`,
        file_contents_base64: b64,
      }];
      if (tss) payload[0].icu_training_load = tss;

      const url = `https://intervals.icu/api/v1/athlete/${ATHLETE_ID}/events/bulk?upsert=true`;
      const res = await fetch(url, {
        method: "POST",
        headers: { Authorization: AUTH, "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const result = await res.json();
      if (fueling_note) await createFuelingNote(fueling_note);
      return {
        content: [{ type: "text", text: `✅ Rad-Workout mit .zwo-Struktur erstellt (ID: ${result[0]?.id})\nzoneTimes: ${result[0]?.workout_doc?.zoneTimes ? "✅" : "❌"}${fueling_note ? "\n📝 Fueling-Note angelegt" : ""}` }],
      };
    }

    // Lauf: workout_steps → "- NUMm LOW-HIGH% Pace" Format
    // intervals.icu parsed diesen Text automatisch zu workout_doc Steps → visuelle Balken + COROS ✅
    if (type === "Run" && workout_steps?.length) {
      const lines = workout_steps.flatMap(s => {
        const mins = Math.round(s.duration_secs / 60);
        if (s.reps && s.steps) {
          const inner = s.steps.map(sub => {
            const m = Math.round(sub.duration_secs / 60);
            const pct = sub.pace_pct_high
              ? `${sub.pace_pct_low ?? sub.pace_pct}-${sub.pace_pct_high}% Pace`
              : `${sub.pace_pct ?? sub.pace_pct_low ?? 100}% Pace`;
            return `- ${m}m ${pct}`;
          });
          return Array(s.reps).fill(inner).flat();
        }
        const pct = s.pace_pct_high
          ? `${s.pace_pct_low ?? s.pace_pct}-${s.pace_pct_high}% Pace`
          : `${s.pace_pct ?? s.pace_pct_low ?? 75}% Pace`;
        return [`- ${mins}m ${pct}`];
      });

      const autoDesc = lines.join("\n");
      const totalDuration = workout_steps.reduce((acc, s) => {
        if (s.reps && s.steps) return acc + s.steps.reduce((a, sub) => a + sub.duration_secs, 0) * s.reps;
        return acc + s.duration_secs;
      }, 0);

      const payload = {
        start_date_local: `${date}T00:00:00`,
        type: "Run",
        category: "WORKOUT",
        name,
        description: description ? `${description}\n\n${autoDesc}` : autoDesc,
        moving_time: duration_secs ?? totalDuration,
      };
      if (tss) payload.icu_training_load = tss;

      const result = await apiFetch("/events", { method: "POST", body: JSON.stringify(payload) });
      if (fueling_note) await createFuelingNote(fueling_note);
      return {
        content: [{ type: "text", text: `✅ Lauf-Workout erstellt (ID: ${result.id})\nStruktur: ${lines.length} Schritte → visuelle Balken + COROS${fueling_note ? "\n📝 Fueling-Note angelegt" : ""}` }],
      };
    }

    // Kraft/Sonstiges: Description-Format
    const payload = {
      start_date_local: `${date}T00:00:00`,
      type,
      category: "WORKOUT",
      name,
      description: description ?? "",
      workout_doc: {},
    };
    if (duration_secs) payload.moving_time = duration_secs;
    if (tss) payload.icu_training_load = tss;

    const result = await apiFetch("/events", { method: "POST", body: JSON.stringify(payload) });
    if (fueling_note) await createFuelingNote(fueling_note);
    return {
      content: [{ type: "text", text: `✅ Workout erstellt (ID: ${result.id})${fueling_note ? "\n📝 Fueling-Note angelegt" : ""}` }],
    };
  }
);

// ── Tool 5: .zwo Datei generieren ───────────────────────────
server.tool(
  "generate_zwo",
  "Generiert eine .zwo Datei für ein Rad-Workout. Die Datei kann in intervals.icu via Drag & Drop importiert werden und zeigt dann die farbige Workout-Struktur.",
  {
    name: z.string().describe("Workout-Name"),
    description: z.string().optional().describe("Beschreibung"),
    steps: z.array(z.object({
      type: z.enum(["warmup", "steady", "cooldown", "interval", "recovery", "ramp"]),
      duration_secs: z.number(),
      power_pct: z.number().optional().describe("Zielwatt in % FTP (z.B. 55 für 55%)"),
      power_pct_start: z.number().optional().describe("Startwatt % FTP für Ramp"),
      power_pct_end: z.number().optional().describe("Endwatt % FTP für Ramp"),
      text: z.string().optional(),
    })),
    output_path: z.string().optional().describe("Speicherpfad (default: ~/Downloads/<name>.zwo)"),
  },
  async ({ name, description, steps, output_path }) => {
    const { writeFileSync } = await import("fs");
    const { homedir } = await import("os");
    const { join } = await import("path");

    const xmlSteps = steps.map(s => {
      const pct = (v) => (v / 100).toFixed(3);
      if (s.type === "warmup") {
        return `    <Warmup Duration="${s.duration_secs}" PowerLow="${pct(s.power_pct_start ?? 40)}" PowerHigh="${pct(s.power_pct_end ?? s.power_pct ?? 55)}">${s.text ? `\n      <textevent timeoffset="0" message="${s.text}"/>` : ""}\n    </Warmup>`;
      } else if (s.type === "cooldown") {
        return `    <Cooldown Duration="${s.duration_secs}" PowerLow="${pct(s.power_pct_end ?? 40)}" PowerHigh="${pct(s.power_pct_start ?? s.power_pct ?? 55)}">${s.text ? `\n      <textevent timeoffset="0" message="${s.text}"/>` : ""}\n    </Cooldown>`;
      } else if (s.type === "ramp") {
        return `    <Ramp Duration="${s.duration_secs}" PowerLow="${pct(s.power_pct_start ?? 40)}" PowerHigh="${pct(s.power_pct_end ?? 80)}">${s.text ? `\n      <textevent timeoffset="0" message="${s.text}"/>` : ""}\n    </Ramp>`;
      } else {
        const pwr = pct(s.power_pct ?? 55);
        const tag = s.type === "recovery" ? "FreeRide" : "SteadyState";
        return `    <${tag} Duration="${s.duration_secs}" Power="${pwr}">${s.text ? `\n      <textevent timeoffset="0" message="${s.text}"/>` : ""}\n    </${tag}>`;
      }
    }).join("\n");

    const xml = `<?xml version="1.0" encoding="utf-8"?>
<workout_file>
  <author>Coach Claude</author>
  <name>${name}</name>
  <description>${description ?? ""}</description>
  <sportType>bike</sportType>
  <workout>
${xmlSteps}
  </workout>
</workout_file>`;

    const safeName = name.replace(/[^a-z0-9äöüß\-_]/gi, "_");
    const filePath = output_path ?? join(homedir(), "Downloads", `${safeName}.zwo`);
    writeFileSync(filePath, xml, "utf8");

    return {
      content: [{
        type: "text",
        text: `✅ .zwo Datei gespeichert: ${filePath}\n\nImport in intervals.icu: Workouts → + → Datei hochladen (oder Drag & Drop)`,
      }],
    };
  }
);

// ── Tool 6: Event löschen ────────────────────────────────────
server.tool(
  "delete_event",
  "Löscht ein geplantes Event aus dem intervals.icu Kalender anhand der Event-ID.",
  {
    event_id: z.string().describe("Die ID des zu löschenden Events"),
  },
  async ({ event_id }) => {
    const url = `https://intervals.icu/api/v1/athlete/${ATHLETE_ID}/events/${event_id}`;
    const res = await fetch(url, {
      method: "DELETE",
      headers: { Authorization: AUTH },
    });
    if (!res.ok) throw new Error(`Delete failed: ${res.status}`);
    return {
      content: [{ type: "text", text: `✅ Event ${event_id} gelöscht.` }],
    };
  }
);

// ── Tool 7: Zonen-Analyse ────────────────────────────────────
server.tool(
  "get_activity_zones",
  "Zonen-Analyse abgeschlossener Aktivitäten: Zeit in jeder Powerzone (Z1-Z7) und HF-Zone. Für Wochen-Review und Trainingsqualität.",
  {
    days: z.number().optional().describe("Wie viele Tage zurückschauen (default: 7)"),
  },
  async ({ days = 7 }) => {
    const oldest = daysAgo(days);
    const data = await apiFetch(`/activities?oldest=${oldest}&newest=${today()}`);

    if (!data.length) return { content: [{ type: "text", text: "Keine Aktivitäten gefunden." }] };

    const powerZoneNames = ["Z1 Erholung", "Z2 Ausdauer", "Z3 Tempo", "Z4 Schwelle", "Z5 VO2max", "Z6 Anaerob", "Z7 Sprint"];
    const hrZoneNames = ["Z1 <60%", "Z2 60-70%", "Z3 70-80%", "Z4 80-90%", "Z5 >90%"];

    // icu_zone_times kann Array von Zahlen ODER Array von {id, secs}-Objekten sein
    function parseZoneTimes(raw, names) {
      if (!raw?.length) return [];
      return raw
        .filter(z => z.id !== "SS") // Sweetspot separat, keine eigene Zone
        .map((z, i) => {
          const secs = typeof z === "number" ? z : z.secs;
          const label = typeof z === "object" && z.id ? z.id : (names[i] ?? `Z${i + 1}`);
          return { zone: label, secs };
        });
    }

    const result = data.map(a => {
      const totalSecs = a.moving_time ?? 1;

      const powerZones = parseZoneTimes(a.icu_zone_times, powerZoneNames)
        .map(z => ({ zone: z.zone, min: Math.round(z.secs / 60), pct: Math.round(z.secs / totalSecs * 100) }))
        .filter(z => z.min > 0);

      const hrZones = parseZoneTimes(a.icu_hr_zone_times, hrZoneNames)
        .map(z => ({ zone: z.zone, min: Math.round(z.secs / 60), pct: Math.round(z.secs / totalSecs * 100) }))
        .filter(z => z.min > 0);

      return {
        datum: a.start_date_local?.split("T")[0],
        name: a.name,
        typ: a.type,
        dauer_min: Math.round(totalSecs / 60),
        tss_ist: a.icu_training_load,
        tss_soll: a.icu_planned_training_load ?? null,
        avg_watt: a.icu_weighted_avg_watts,
        avg_hf: a.average_heartrate,
        power_zones: powerZones,
        hr_zones: hrZones,
      };
    });

    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── Tool 8: Wochenrückblick ──────────────────────────────────
server.tool(
  "get_weekly_review",
  "Vollständiger Wochenrückblick: Geplante vs. absolvierte Einheiten, TSS-Bilanz, Zonen pro Session, HRV-Verlauf. Basis für Coach-Feedback.",
  {
    week_start: z.string().describe("Montag der Woche YYYY-MM-DD"),
  },
  async ({ week_start }) => {
    const start = new Date(week_start);
    const endDate = new Date(start);
    endDate.setDate(endDate.getDate() + 6);
    const endStr = endDate.toISOString().split("T")[0];

    const [events, activities, wellness] = await Promise.all([
      apiFetch(`/events?oldest=${week_start}&newest=${endStr}`),
      apiFetch(`/activities?oldest=${week_start}&newest=${endStr}`),
      apiFetch(`/wellness?oldest=${week_start}&newest=${endStr}`),
    ]);

    const workoutEvents = events.filter(e =>
      e.category === "WORKOUT" || ["Ride", "Run", "WeightTraining"].includes(e.type)
    );

    function parseZones(raw) {
      if (!raw?.length) return [];
      return raw
        .filter(z => typeof z === "number" || (z.id && z.id !== "SS"))
        .map((z, i) => ({
          zone: typeof z === "object" ? z.id : `Z${i + 1}`,
          secs: typeof z === "number" ? z : z.secs,
        }));
    }

    const activityDetails = activities.map(a => {
      const totalSecs = a.moving_time ?? 1;
      const powerZones = parseZones(a.icu_zone_times)
        .map(z => ({ zone: z.zone, min: Math.round(z.secs / 60), pct: Math.round(z.secs / totalSecs * 100) }))
        .filter(z => z.min > 0);

      return {
        id: a.id,
        datum: a.start_date_local?.split("T")[0],
        name: a.name,
        typ: a.type,
        dauer_min: Math.round(totalSecs / 60),
        tss: a.icu_training_load,
        avg_watt: a.icu_weighted_avg_watts,
        avg_hf: a.average_heartrate,
        power_zones: powerZones,
      };
    });

    const plannedByDay = {};
    workoutEvents.forEach(e => {
      const d = e.start_date_local?.split("T")[0];
      if (d) plannedByDay[d] = (plannedByDay[d] ?? []).concat({
        name: e.name, tss: e.icu_training_load, type: e.type,
      });
    });

    const actualByDay = {};
    activityDetails.forEach(a => {
      if (a.datum) actualByDay[a.datum] = (actualByDay[a.datum] ?? []).concat(a);
    });

    const plannedTSS = workoutEvents.reduce((s, e) => s + (e.icu_training_load ?? 0), 0);
    const actualTSS = activities.reduce((s, a) => s + (a.icu_training_load ?? 0), 0);

    const hrvTrend = wellness.map(w => ({
      datum: w.id,
      hrv: w.hrv,
      schlaf_h: w.sleepSecs ? (w.sleepSecs / 3600).toFixed(1) : null,
      ruhepuls: w.restingHR,
    }));

    // ── Polarisations-Monitor ─────────────────────────────────
    // Nur Rad-Aktivitäten (haben verlässliche Power-Zonen via icu_zone_times)
    let totalLowSecs = 0, totalMidSecs = 0, totalHighSecs = 0;
    const rideActivities = activities.filter(a => a.type === "Ride" || a.type === "VirtualRide");

    rideActivities.forEach(a => {
      const zones = parseZones(a.icu_zone_times);
      zones.forEach(z => {
        const num = parseInt(z.zone.replace("Z", ""), 10);
        if (num <= 2)       totalLowSecs  += z.secs;
        else if (num === 3) totalMidSecs  += z.secs;
        else if (num >= 4)  totalHighSecs += z.secs;
      });
    });

    const totalZoneSecs = totalLowSecs + totalMidSecs + totalHighSecs;
    let polarisation = null;
    if (totalZoneSecs > 0) {
      const pctLow  = Math.round(totalLowSecs  / totalZoneSecs * 100);
      const pctMid  = Math.round(totalMidSecs  / totalZoneSecs * 100);
      const pctHigh = Math.round(totalHighSecs / totalZoneSecs * 100);
      // Polarisations-Index: Z1-2 / (Z1-2 + Z4-7) × 100
      const pi = (totalLowSecs + totalHighSecs) > 0
        ? Math.round(totalLowSecs / (totalLowSecs + totalHighSecs) * 100)
        : null;

      const warnings = [];
      if (pctMid > 15) warnings.push(`⚠️ Sweetspot-Drift: Z3 = ${pctMid}% (Ziel: <15%) – LIT-Einheiten zu intensiv gefahren`);
      if (pi !== null && pi < 80) warnings.push(`⚠️ Polarisations-Index: ${pi}% (Ziel: ≥80%) – zu wenig echte Grundlage vs. Intensität`);

      polarisation = {
        basis: `${rideActivities.length} Rad-Einheiten`,
        zonen: {
          "Z1-Z2 (Low)":  `${pctLow}%  (${Math.round(totalLowSecs  / 60)} min)`,
          "Z3 (Moderate)": `${pctMid}%  (${Math.round(totalMidSecs  / 60)} min)`,
          "Z4-Z7 (High)":  `${pctHigh}% (${Math.round(totalHighSecs / 60)} min)`,
        },
        polarisations_index: pi !== null ? `${pi}% (Ziel: ≥80%)` : "n/a",
        status: warnings.length ? warnings : ["✅ Trainingsverteilung im grünen Bereich"],
      };
    } else {
      polarisation = { basis: "Keine Rad-Aktivitäten mit Zonen-Daten", status: [] };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          zeitraum: `${week_start} bis ${endStr}`,
          tss_soll: plannedTSS,
          tss_ist: actualTSS,
          tss_differenz: actualTSS - plannedTSS,
          einheiten_geplant: workoutEvents.length,
          einheiten_absolviert: activities.length,
          geplant_pro_tag: plannedByDay,
          absolviert_pro_tag: actualByDay,
          hrv_verlauf: hrvTrend,
          aktivitaeten_detail: activityDetails,
          polarisation,
        }, null, 2),
      }],
    };
  }
);

// ── Hilfsfunktionen: Readiness-Score ────────────────────────
function _avg(arr) { return arr.reduce((a, b) => a + b, 0) / arr.length; }
function _stdDev(arr) {
  const m = _avg(arr);
  return Math.sqrt(arr.reduce((s, v) => s + (v - m) ** 2, 0) / arr.length);
}

// Berechnet Score aus einem Array von Wellness-Einträgen (chronologisch, min. 3)
// Gibt score, ampel, empfehlung, komponenten und interne _meta zurück
function computeReadiness(data) {
  // HRV (40 Punkte)
  const hrvValues = data.map(d => d.hrv).filter(Boolean);
  let hrvPts = 20, hrvDetail = "Keine HRV-Daten", hrvDiffSDs = 0;
  if (hrvValues.length >= 3) {
    const mean = _avg(hrvValues);
    const sd = Math.max(_stdDev(hrvValues), 1);
    const last = hrvValues[hrvValues.length - 1];
    const diff = last - mean;
    hrvDiffSDs = diff / sd;
    if (diff > sd)         { hrvPts = 40; hrvDetail = `${last} ms (+${diff.toFixed(1)} > +1SD) – erhöht`; }
    else if (diff > 0)     { hrvPts = 33; hrvDetail = `${last} ms (+${diff.toFixed(1)}) – leicht über Mittel`; }
    else if (diff > -sd)   { hrvPts = 24; hrvDetail = `${last} ms (${diff.toFixed(1)}) – leicht unter Mittel`; }
    else if (diff > -2*sd) { hrvPts = 10; hrvDetail = `${last} ms (${diff.toFixed(1)} < -1SD) – supprimiert`; }
    else                   { hrvPts = 0;  hrvDetail = `${last} ms (${diff.toFixed(1)} < -2SD) – stark supprimiert`; }
  }

  // Schlaf (25 Punkte)
  const last3 = data.slice(-3);
  let sleepPts = 13, sleepDetail = "Keine Schlafdaten";
  const qualityVals = last3.map(d => d.sleepQuality).filter(v => v != null);
  const sleepSecsVals = last3.map(d => d.sleepSecs).filter(Boolean);
  if (qualityVals.length) {
    const avgQ = _avg(qualityVals);
    sleepPts = Math.round((avgQ / 5) * 25);
    sleepDetail = `Schlafqualität Ø ${avgQ.toFixed(1)}/5 (letzte 3 Nächte)`;
  } else if (sleepSecsVals.length) {
    const avgH = _avg(sleepSecsVals) / 3600;
    sleepPts = Math.min(25, Math.round((avgH / 8) * 25));
    sleepDetail = `Schlafdauer Ø ${avgH.toFixed(1)}h (Ziel: 8h)`;
  }

  // TSB (20 Punkte)
  const latest = data[data.length - 1];
  const tsb = latest.ctl && latest.atl ? latest.ctl - latest.atl : null;
  let tsbPts = 10, tsbDetail = "TSB nicht verfügbar";
  if (tsb !== null) {
    if (tsb > 10)        { tsbPts = 20; tsbDetail = `TSB ${tsb.toFixed(1)} – frisch`; }
    else if (tsb >= 0)   { tsbPts = 17; tsbDetail = `TSB ${tsb.toFixed(1)} – ausgeglichen`; }
    else if (tsb >= -10) { tsbPts = 13; tsbDetail = `TSB ${tsb.toFixed(1)} – leicht ermüdet`; }
    else if (tsb >= -20) { tsbPts = 6;  tsbDetail = `TSB ${tsb.toFixed(1)} – ermüdet`; }
    else                 { tsbPts = 0;  tsbDetail = `TSB ${tsb.toFixed(1)} – stark ermüdet`; }
  }

  // Ruhepuls (15 Punkte)
  const hrValues = data.map(d => d.restingHR).filter(Boolean);
  let hrPts = 8, hrDetail = "Keine Ruhepuls-Daten", hrDiff = 0;
  if (hrValues.length >= 3) {
    const meanHR = _avg(hrValues.slice(0, -1));
    const lastHR = hrValues[hrValues.length - 1];
    hrDiff = lastHR - meanHR;
    if (hrDiff <= -3)     { hrPts = 15; hrDetail = `${lastHR} bpm (${hrDiff.toFixed(1)} vs. Ø) – deutlich niedriger`; }
    else if (hrDiff <= 0) { hrPts = 12; hrDetail = `${lastHR} bpm (${hrDiff.toFixed(1)} vs. Ø) – normal/niedriger`; }
    else if (hrDiff <= 3) { hrPts = 8;  hrDetail = `${lastHR} bpm (+${hrDiff.toFixed(1)} vs. Ø) – leicht erhöht`; }
    else if (hrDiff <= 6) { hrPts = 3;  hrDetail = `${lastHR} bpm (+${hrDiff.toFixed(1)} vs. Ø) – erhöht`; }
    else                  { hrPts = 0;  hrDetail = `${lastHR} bpm (+${hrDiff.toFixed(1)} vs. Ø) – deutlich erhöht`; }
  }

  const score = hrvPts + sleepPts + tsbPts + hrPts;
  let ampel, empfehlung;
  if (score >= 80)      { ampel = "🟢"; empfehlung = "Voll trainieren – alle Einheiten wie geplant."; }
  else if (score >= 60) { ampel = "🟡"; empfehlung = "Planmäßig trainieren, gut beobachten."; }
  else if (score >= 40) { ampel = "🟡"; empfehlung = "Intensität −20% reduzieren, Volumen optional kürzen."; }
  else                  { ampel = "🔴"; empfehlung = "Nur LIT oder Ruhetag – Erholung priorisieren."; }

  return {
    score,
    ampel,
    empfehlung,
    komponenten: {
      hrv:      { punkte: hrvPts,   max: 40, detail: hrvDetail },
      schlaf:   { punkte: sleepPts, max: 25, detail: sleepDetail },
      tsb:      { punkte: tsbPts,   max: 20, detail: tsbDetail },
      ruhepuls: { punkte: hrPts,    max: 15, detail: hrDetail },
    },
    _meta: { hrvDiffSDs, hrDiff, tsbVal: tsb, sleepPts },
  };
}

// Erkennt Muster: Normal / Trainings-Ermüdung / Krank-Risiko
function detectPattern(meta) {
  const { hrvDiffSDs, hrDiff, tsbVal } = meta;
  // Krank-Risiko: HRV stark supprimiert UND Ruhepuls deutlich erhöht
  // Unterschied zu Ermüdung: Ermüdung zeigt meist nur TSB-Absenkung ohne starke HR-HRV-Kombination
  if (hrvDiffSDs < -1.5 && hrDiff > 5) {
    return {
      muster: "🔴 Krank-Risiko",
      hinweis: "HRV stark supprimiert + Ruhepuls deutlich erhöht – klassisches Infekt-Muster. Keine Belastung, komplette Pause. Unterschied zu Ermüdung: Trainingsfatigue normalisiert sich nach 1–2 Ruhetagen; bleibt der Score niedrig, ist ein Infekt wahrscheinlicher.",
    };
  }
  // Trainings-Ermüdung: hohe akkumulierte Last ohne akute Infekt-Marker
  if (tsbVal !== null && tsbVal < -15 && hrvDiffSDs > -2) {
    return {
      muster: "🟡 Trainings-Ermüdung",
      hinweis: "Hohe akkumulierte Last (TSB niedrig), keine Krank-Indikatoren. 1–2 Regenerationstage genügen für Erholung.",
    };
  }
  return { muster: "🟢 Normal", hinweis: null };
}

// Workout-Anpassungs-Empfehlungen basierend auf Score + geplantem Workout
function suggestWorkoutMods(score, plannedEvents) {
  const workouts = (plannedEvents ?? []).filter(e =>
    ["WORKOUT", "RACE"].includes(e.category) &&
    ["Ride", "Run", "WeightTraining", "VirtualRide"].includes(e.type)
  );
  if (!workouts.length) return null;

  return workouts.map(w => {
    const name = w.name ?? "";
    const isHIT  = /HIT|VO2|IE_|HITdec/i.test(name);
    const isSwSp = /SwSp|Sweetspot/i.test(name);
    const isKA   = /\bKA\b/i.test(name);
    const isMIT  = /MIT|Over.Under/i.test(name);
    const isLIT  = /LIT/i.test(name);

    let empfehlung;
    if (score >= 80) {
      empfehlung = "✅ Wie geplant";
    } else if (score >= 60) {
      empfehlung = isHIT
        ? "✅ Wie geplant – erstes Intervall als Test: RPE > 8 schon früh → letzten Satz streichen"
        : "✅ Wie geplant";
    } else if (score >= 40) {
      if (isHIT)       empfehlung = "⚠️ Sätze auf 2/3 reduzieren (z.B. 4×4 → 3×4), Intensität halten";
      else if (isSwSp) empfehlung = "⚠️ Ein Intervall weniger, Watt halten";
      else if (isKA)   empfehlung = "⚠️ Auf kürzere KA-Variante wechseln (z.B. 3×10 statt 4×10)";
      else if (isMIT)  empfehlung = "⚠️ Auf SwSp-Niveau reduzieren (~88% FTP statt 101%)";
      else if (isLIT)  empfehlung = "✅ LIT ideal bei diesem Score – wie geplant";
      else             empfehlung = "⚠️ Intensität −20%, Dauer optional −30min";
    } else {
      empfehlung = isLIT
        ? "⚠️ LIT auf 1h kürzen oder Ruhetag"
        : "🔴 Ersetzen durch LIT-1h oder komplette Pause";
    }
    return { workout: name, typ: w.type, empfehlung };
  });
}

// ── Tool 9: Readiness Score ──────────────────────────────────
server.tool(
  "get_readiness_score",
  "Readiness-Score (0–100) aus HRV-Trend, Schlaf, TSB und Ruhepuls. Erkennt Krank-Risiko vs. Trainings-Ermüdung, gibt konkrete Workout-Modifikationen für geplante Einheiten und zeigt 7/30-Tage-Verlauf.",
  {
    datum: z.string().optional().describe("Datum für Workout-Check YYYY-MM-DD (default: heute)"),
  },
  async ({ datum }) => {
    const checkDate = datum ?? today();

    // 30 Tage Wellness für Trend + 7-Tage-Fenster für heutigen Score
    const [wellnessAll, plannedEvents] = await Promise.all([
      apiFetch(`/wellness?oldest=${daysAgo(30)}&newest=${checkDate}`),
      apiFetch(`/events?oldest=${checkDate}&newest=${checkDate}`),
    ]);

    if (!wellnessAll.length) return { content: [{ type: "text", text: "Keine Wellness-Daten gefunden." }] };

    // Heutiger Score: letzten 7 verfügbaren Tage
    const window7 = wellnessAll.slice(-7);
    const { score, ampel, empfehlung, komponenten, _meta } = computeReadiness(window7);
    const { muster, hinweis } = detectPattern(_meta);
    const workout_empfehlungen = suggestWorkoutMods(score, plannedEvents);

    // ── Verlauf: Score für jeden der letzten 30 Tage berechnen ──
    // Pro Tag: nutze die bis dahin verfügbaren letzten 7 Einträge als Fenster
    const verlauf = wellnessAll.map((_, i) => {
      if (i < 2) return null; // Mindestens 3 Datenpunkte nötig
      const slice = wellnessAll.slice(Math.max(0, i - 6), i + 1);
      const r = computeReadiness(slice);
      return { datum: wellnessAll[i].id, score: r.score, ampel: r.ampel };
    }).filter(Boolean);

    const verlauf7  = verlauf.slice(-7);
    const verlauf30 = verlauf;

    // Trend-Richtung aus letzten 7 Tagen
    let trendRichtung = "stabil";
    if (verlauf7.length >= 4) {
      const first = _avg(verlauf7.slice(0, 3).map(v => v.score));
      const last  = _avg(verlauf7.slice(-3).map(v => v.score));
      if (last - first >  8) trendRichtung = "steigend ↑";
      if (last - first < -8) trendRichtung = "fallend ↓";
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          datum: checkDate,
          score,
          ampel,
          empfehlung,
          muster,
          muster_hinweis: hinweis,
          workout_empfehlungen,
          komponenten,
          trend: {
            richtung_7d: trendRichtung,
            verlauf_7d:  verlauf7,
            verlauf_30d: verlauf30,
          },
        }, null, 2),
      }],
    };
  }
);

// ── Tool 6 (Wellness): Zeitraum ──────────────────────────────
server.tool(
  "get_wellness_range",
  "Wellness-Daten (HRV, CTL, ATL, Schlaf) für einen bestimmten Zeitraum – für Trend-Analyse.",
  {
    oldest: z.string().describe("Startdatum YYYY-MM-DD"),
    newest: z.string().describe("Enddatum YYYY-MM-DD"),
  },
  async ({ oldest, newest }) => {
    const data = await apiFetch(`/wellness?oldest=${oldest}&newest=${newest}`);
    const simplified = data.map(d => ({
      datum: d.id,
      ctl: d.ctl?.toFixed(1),
      atl: d.atl?.toFixed(1),
      tsb: d.ctl && d.atl ? (d.ctl - d.atl).toFixed(1) : null,
      hrv: d.hrv,
      ruhepuls: d.restingHR,
      schlaf_h: d.sleepSecs ? (d.sleepSecs / 3600).toFixed(1) : null,
      schritte: d.steps,
    }));
    return {
      content: [{ type: "text", text: JSON.stringify(simplified, null, 2) }],
    };
  }
);

// ── Start ────────────────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);

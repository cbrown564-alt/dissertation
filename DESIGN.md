---
version: "alpha"
name: Evidence Notebook Design System
description: "A source-backed research dossier interface for a local-first clinical NLP dissertation project."
colors:
  primary: "#1C211D"
  on-primary: "#F4F0E7"
  secondary: "#59625C"
  on-secondary: "#F8F5EE"
  tertiary: "#0A7D82"
  on-tertiary: "#F8F5EE"
  accent: "#C79A38"
  on-accent: "#1C211D"
  surface: "#F4F0E7"
  surface-raised: "#FBF8F1"
  surface-muted: "#E9E3D6"
  surface-grid: "#DCD3C1"
  border: "#CFC5B4"
  border-strong: "#827867"
  text: "#1C1B18"
  text-muted: "#5E5A51"
  text-faint: "#81796B"
  link: "#0A6D71"
  success: "#247A57"
  warning: "#B47A16"
  danger: "#A6423A"
  info: "#2F6F9F"
typography:
  display-xl:
    fontFamily: Georgia, "Times New Roman", serif
    fontSize: 4.75rem
    fontWeight: "700"
    lineHeight: "0.95"
    letterSpacing: "0"
  display-md:
    fontFamily: Georgia, "Times New Roman", serif
    fontSize: 2.25rem
    fontWeight: "700"
    lineHeight: "1.05"
    letterSpacing: "0"
  heading-md:
    fontFamily: Georgia, "Times New Roman", serif
    fontSize: 1.5rem
    fontWeight: "700"
    lineHeight: "1.15"
    letterSpacing: "0"
  body-md:
    fontFamily: "Segoe UI", system-ui, sans-serif
    fontSize: 1rem
    fontWeight: "400"
    lineHeight: "1.55"
    letterSpacing: "0"
  body-sm:
    fontFamily: "Segoe UI", system-ui, sans-serif
    fontSize: 0.875rem
    fontWeight: "400"
    lineHeight: "1.45"
    letterSpacing: "0"
  label-caps:
    fontFamily: "Segoe UI", system-ui, sans-serif
    fontSize: 0.6875rem
    fontWeight: "800"
    lineHeight: "1.1"
    letterSpacing: "0.12em"
  data:
    fontFamily: "Cascadia Mono", "SFMono-Regular", Consolas, monospace
    fontSize: 0.8125rem
    fontWeight: "500"
    lineHeight: "1.35"
    letterSpacing: "0"
rounded:
  none: 0px
  xs: 2px
  sm: 4px
  md: 8px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  "2xl": 48px
  "3xl": 72px
components:
  app-rail:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    width: 128px
  app-surface:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
  source-card:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.none}"
    padding: 16px
  source-card-hover:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.text}"
  stat-button:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.none}"
    padding: 16px
  stat-button-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  record-panel:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.none}"
    padding: 24px
  primary-action:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
    padding: 12px
  secondary-action:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: 12px
  warning-chip:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.xs}"
    padding: 8px
---

## Overview

Evidence Notebook is a research-grade product interface for making an agentic dissertation project legible. It should feel like a supervisor-reviewable lab book: source-backed, quiet, rigorous, and distinctive without becoming decorative.

The interface should foreground what is true, what evidence supports it, what remains uncertain, and what action follows. It is not a landing page, portfolio, or generic analytics dashboard.

## Colors

The palette is an archival paper system with technical accents. It should feel warmer and more tactile than a standard SaaS dashboard while remaining readable for long review sessions.

- **Primary (#1C211D):** Deep green-black ink for the rail, strong text, and selected navigation.
- **Surface (#F4F0E7):** Warm paper base. Avoid pure white.
- **Surface Raised (#FBF8F1):** Slightly lifted paper for records and source cards.
- **Border (#CFC5B4):** Fine ledger rules, tables, and quiet separation.
- **Tertiary (#0A7D82):** Evidence and navigation accent. Use for links, active source traces, and primary actions only.
- **Accent (#C79A38):** Review highlight. Use sparingly for active milestone, warnings, or attention cues.
- **Success, warning, danger, info:** Semantic states for evaluation quality, risk, blockers, and context. Do not use them as decoration.

Do not use pure black or pure white. Neutrals should stay slightly warm and tinted.

## Typography

Use a serif display voice for the notebook identity and a system sans for working UI.

- Display headings use Georgia or a compatible editorial serif. They create the lab-book identity.
- UI labels, navigation, search, metadata, tables, and controls use system sans.
- Data paths, run ids, and code-like artifacts use a monospace style.
- Body prose should stay within 65 to 75 characters where possible.
- Inner screens should not repeat the full hero scale. The overview may use `display-xl`; deeper views should use `display-md` or `heading-md`.

## Layout

The product uses a left rail, a paper grid surface, and ledger-like horizontal rules.

- The overview may be spacious and editorial.
- Inner views should compress repeated chrome and bring the working content above the fold.
- Source cards and stats are useful context, but they should be collapsible or visually secondary on deep screens.
- Prefer dossiers, ledgers, timelines, and split readers over generic card grids.
- Use predictable grids for task flow, but vary rhythm between sections so the interface does not become monotonous.
- Avoid nested cards. A panel may contain sections, rows, or rules, but not more framed cards.

## Elevation & Depth

Depth should come from paper layering, rules, and tonal shifts rather than shadows.

- Use 1px borders and background shifts for separation.
- Avoid glass effects, heavy shadows, floating chrome, and decorative blurs.
- Hover states may lift slightly through color, transform, or underline, but should remain calm.

## Shapes

The system is mostly square-edged and archival.

- Default panels and ledger rows use `rounded.none`.
- Buttons and focusable controls may use `rounded.sm` for tactility.
- Avoid pill-heavy interfaces unless the element is a compact status chip.

## Components

### App Rail

The rail is a stable project index. It should show the monogram, view navigation, and local archive timestamp. The selected view must be obvious through background and border changes, not color alone.

### Source Ledger

Source cards are audit affordances. Each card should show the source name, freshness, and destination. Keep them plain, link-like, and easy to scan.

### Stats Strip

Stats are navigation and orientation, not hero metrics. They should sit below the source ledger and may become compact buttons on deeper screens.

### Claim Dossier

A claim dossier must preserve the four-part research contract:

1. Claim.
2. Evidence.
3. Uncertainty.
4. Next action.

Evidence should contain visible source links. Uncertainty should never be hidden below decorative content.

### Timeline

The timeline should distinguish complete, active, planned, blocked, and review-needed states. The active milestone gets the strongest accent. Planned milestones should be quieter.

### Session Feed

Session rows should first answer what changed. Expanded details should show outcome, evidence, uncertainty, and handoff. Source-log links should be stable and visible.

### Artifact Shelf

Artifacts should be grouped by use: active evidence, generated visuals, planned visuals, dissertation support. The shelf should show purpose, path, status, and intended use.

### Decisions

Decision records should follow an ADR-like structure: decision, rationale, consequence, evidence. They should feel durable and citable.

## Do's and Don'ts

Do:

- Make every status claim traceable to a source.
- Keep source links visible and legible.
- Use restrained color for state and evidence.
- Compress repeated header material on inner screens.
- Favor dense, calm product UI over cinematic page choreography.
- Use motion for state changes, reveal, focus, and navigation orientation.

Don't:

- Do not make this look like a generic SaaS dashboard.
- Do not use decorative gradients, glass panels, or ornamental motion.
- Do not use random stock imagery or AI-themed visuals in the working interface.
- Do not bury uncertainty or next actions.
- Do not use identical icon-card grids.
- Do not treat evidence metrics as marketing stats.

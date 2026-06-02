---
name: saas-redesign
description: Redesign the Vue 3 frontend into a modern SaaS-style interface with a left vertical navigation sidebar (replacing the top nav bar), a consistent spacing/typography scale, and a polished professional look. Use when asked to modernize the UI, add a sidebar/left nav, improve visual design, make the app look like a SaaS product, or apply a consistent design system across views.
---

# SaaS UI Redesign

Transforms this app's top-nav layout into a modern SaaS shell: a fixed **left vertical sidebar** for primary navigation, a slim top bar for global controls (search, language, profile), and a consistent design system applied across every view.

## Non-negotiable rules

- **Delegate every `.vue` create/edit to the `vue-expert` subagent** (CLAUDE.md mandates this). This skill is the design brief; vue-expert does the file edits. Pass it the relevant section of this skill plus the target file.
- **Preserve all behavior**: routes, `router-link` targets, the `<FilterBar />`, modals, i18n (`t('nav.*')`), and `ProfileMenu`/`LanguageSwitcher` must keep working. This is a visual + layout change, not a feature change.
- **No emojis in UI** (design system rule). Use SVG icons for nav items.
- **Composition API + scoped styles only**, matching the existing `client/CLAUDE.md` conventions.

## Target layout

```
┌────────────┬──────────────────────────────────────┐
│            │  Top bar: page title │ search │ lang │ profile
│  SIDEBAR   ├──────────────────────────────────────┤
│            │  FilterBar (unchanged)               │
│  logo      ├──────────────────────────────────────┤
│  ──────    │                                      │
│  ▸ nav     │  main-content (router-view)          │
│  ▸ nav     │                                      │
│  ▸ nav     │                                      │
│            │                                      │
│  profile   │                                      │
└────────────┴──────────────────────────────────────┘
```

- Sidebar: fixed left, full height, `width: 260px` (collapsed `72px`, icon-only — optional stretch goal). Logo/wordmark at top, nav links as a vertical stack, push profile/user block to the bottom with `margin-top: auto`.
- Content area: `margin-left: 260px`. Top bar becomes a thin `sticky` strip holding the page title slot, language switcher, and profile menu (move these out of the old `.top-nav`).
- Keep `FilterBar` exactly where it sits in the content column, directly under the top bar.

## Design system (apply consistently)

Introduce CSS custom properties on `:root` in [App.vue](client/src/App.vue) — none exist yet — and refactor hardcoded hex values to use them. This is what makes the result feel "consistent and polished."

```css
:root {
  /* Color — keep the existing slate/blue identity */
  --bg-app: #f8fafc;          /* page background */
  --bg-surface: #ffffff;      /* cards, sidebar, top bar */
  --bg-sidebar: #0f172a;      /* dark sidebar (SaaS look) */
  --border: #e2e8f0;
  --text-strong: #0f172a;
  --text: #334155;
  --text-muted: #64748b;
  --text-on-dark: #cbd5e1;    /* sidebar inactive text */
  --accent: #2563eb;
  --accent-soft: #eff6ff;
  --success: #16a34a; --warning: #d97706; --danger: #dc2626; --info: #2563eb;

  /* Spacing scale (4px base) — use ONLY these, no ad-hoc rem values */
  --sp-1: 0.25rem; --sp-2: 0.5rem; --sp-3: 0.75rem; --sp-4: 1rem;
  --sp-5: 1.5rem;  --sp-6: 2rem;   --sp-8: 3rem;

  /* Radius / elevation / type */
  --radius: 8px; --radius-lg: 12px;
  --shadow-sm: 0 1px 3px rgba(15,23,42,0.06);
  --shadow-md: 0 4px 12px rgba(15,23,42,0.08);
  --font-sm: 0.875rem; --font-base: 0.938rem; --font-lg: 1.125rem;
  --font-h2: 1.5rem; --font-h1: 1.875rem;
}
```

Design principles to enforce while editing:
- **Spacing**: every padding/margin/gap pulls from `--sp-*`. Cards use `--sp-5` internal padding; page gutters `--sp-6`; element gaps `--sp-3`/`--sp-4`.
- **Surfaces**: cards = `--bg-surface` + `1px solid --border` + `--radius-lg` + `--shadow-sm`. Avoid heavy borders + shadow together; pick the lighter look.
- **Typography**: one `h1` per page (`--font-h1`, `letter-spacing: -0.025em`), section headers `--font-h2`. Body `--font-base`, secondary text `--text-muted`.
- **Interaction**: `transition: all 0.15s ease` on nav items, buttons, cards-with-hover. Active nav item = `--accent` text on `--accent-soft` (light bar) or a left accent border (dark sidebar).
- **Density**: generous but not sparse — aim for a calm, aligned grid. Consistent vertical rhythm beats decoration.

## Sidebar nav items (match current routes exactly)

| Label (i18n key)            | Route        |
|-----------------------------|--------------|
| `t('nav.overview')`         | `/`          |
| `t('nav.inventory')`        | `/inventory` |
| `t('nav.orders')`           | `/orders`    |
| `t('nav.finance')`          | `/spending`  |
| `t('nav.demandForecast')`   | `/demand`    |
| `Reports`                   | `/reports`   |

Add a small inline SVG icon per item (e.g. grid, box, cart, dollar, trend, chart). Active state via `$route.path` comparison, same logic as today. Verify against [App.vue](client/src/App.vue#L9-L34) in case routes changed.

## Step-by-step

1. **Read the current shell.** Open [App.vue](client/src/App.vue) — note `.top-nav`, `.nav-container`, `.nav-tabs`, `.main-content`, and where `<FilterBar />`, `<LanguageSwitcher />`, `<ProfileMenu />` live.
2. **Add design tokens.** Insert the `:root` block above into App.vue's global styles (this file holds app-wide styles per CLAUDE.md). Have vue-expert do it.
3. **Restructure App.vue (vue-expert).** Replace the `<header class="top-nav">` block with: an `<aside class="sidebar">` (logo + vertical nav + bottom profile area) and a `<div class="layout-main">` wrapping a slim `<header class="topbar">` (page-title slot + LanguageSwitcher + ProfileMenu), the existing `<FilterBar />`, and `<main class="main-content">`. Keep all modals and script logic intact.
4. **Refactor existing styles to tokens.** Convert the slate/blue hex values throughout App.vue to the new variables so the rest of the app inherits the system.
5. **Polish each view (vue-expert, one at a time).** For each of `Dashboard, Inventory, Orders, Spending, Demand, Backlog, Reports` in [client/src/views/](client/src/views/): align cards to the surface/spacing/typography rules, fix inconsistent paddings, and ensure section headers use the type scale. Don't change data flow or computed logic.
6. **Responsive check.** Sidebar should collapse to a top/overlay or icon-rail under ~`900px`. At minimum, ensure content doesn't break (`margin-left` removed on narrow screens).
7. **Verify in the browser.** Use the `start` skill to run both servers, then Playwright MCP against `http://localhost:3000`: navigate, screenshot the Dashboard and 2–3 other views, confirm nav highlights the active route and no console errors. Resize to mobile width and screenshot. Use the `stop` skill when done.

## Verification checklist

- [ ] Sidebar is fixed-left, full height; all 6 routes present and navigable; active route highlighted.
- [ ] Top bar holds language + profile; FilterBar still renders and filters still work.
- [ ] All modals (`ProfileDetailsModal`, `TasksModal`, detail modals) still open.
- [ ] No hardcoded hex colors left in App.vue for the core palette (tokens used).
- [ ] Spacing uses `--sp-*` consistently; cards share one surface style.
- [ ] No console errors; i18n labels render; no emojis added.
- [ ] Mobile width is usable (sidebar collapses/overlays).
- [ ] `test` skill passes (no regressions in existing frontend tests).

## Scope notes

- This skill is tailored to this project's shell ([App.vue](client/src/App.vue), `FilterBar`, the 6 routes). If routes or components have changed, re-read App.vue first and adjust the nav table.
- Keep the existing slate/blue brand identity — modernize layout and consistency, don't reinvent the color story.

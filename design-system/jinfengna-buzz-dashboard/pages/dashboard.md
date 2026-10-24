# Page Override: Cinematic Thriller Command Center (`dashboard`)

> **Overrides:** `design-system/jinfengna-buzz-dashboard/MASTER.md`
> **Design North Star (設計北極星):** 「暗黑懸疑電影質感 × 戰情室級即時聲量情報中心」— 以黑曜石深邃畫布（`#090A0F`）襯托酒紅警示光暈（`#E11D48`）與流金焦點（`#F59E0B`），每一屏只有一個視覺主角，數據採用等寬字體（`JetBrains Mono` / `Fira Code`）精準對齊，搭配紅黃綠語義燈號（`🟢 成長`、`🟡 持平`、`🔴 下滑`），兼具電影美學與高密度情報檢索效率。

---

## 1. Three-Layer Token Architecture (`design-system` Skill)

### Layer 1: Primitive Tokens
- `--raw-obsidian-950`: `#090A0F`
- `--raw-velvet-900`: `#11131C`
- `--raw-velvet-800`: `#171A26`
- `--raw-velvet-700`: `#1F2435`
- `--raw-crimson-600`: `#E11D48`
- `--raw-crimson-400`: `#FB7185`
- `--raw-gold-500`: `#F59E0B`
- `--raw-gold-300`: `#FCD34D`
- `--raw-emerald-500`: `#10B981`
- `--raw-emerald-300`: `#6EE7B7`
- `--raw-cyan-400`: `#38BDF8`
- `--raw-ivory-50`: `#F8FAFC`
- `--raw-slate-200`: `#E2E8F0`
- `--raw-slate-400`: `#94A3B8`

### Layer 2: Semantic Tokens
- `--bg-canvas`: `var(--raw-obsidian-950)`
- `--bg-surface`: `var(--raw-velvet-900)`
- `--bg-elevated`: `var(--raw-velvet-800)`
- `--text-primary`: `var(--raw-ivory-50)`
- `--text-secondary`: `var(--raw-slate-200)`
- `--text-muted`: `var(--raw-slate-400)`
- `--accent-brand`: `var(--raw-crimson-600)`
- `--accent-gold`: `var(--raw-gold-500)`
- `--accent-telemetry`: `var(--raw-cyan-400)`
- `--status-growth`: `var(--raw-emerald-500)`
- `--status-flat`: `var(--raw-gold-500)`
- `--status-decline`: `var(--raw-crimson-600)`
- `--border-subtle`: `rgba(255, 255, 255, 0.08)`
- `--border-strong`: `rgba(255, 255, 255, 0.16)`

### Layer 3: Component Tokens
- `--card-bg`: `var(--bg-surface)`
- `--card-border`: `var(--border-subtle)`
- `--card-radius`: `14px`
- `--nav-bg`: `rgba(9, 10, 15, 0.84)`
- `--font-display`: `'Noto Serif TC', 'Noto Sans TC', serif`
- `--font-sans`: `'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif`
- `--font-mono`: `'JetBrains Mono', 'Fira Code', monospace`

## 2. Layout & Ergonomics (`oil-ui` & `ui-ux-pro-max`)
- **Zero Card-in-Card Nesting**: Do not wrap bordered containers inside bordered containers.
- **Zero Single-Side Colored Borders**: Use clean subtle borders and surface elevation instead of `border-left: 4px solid`.
- **Readable CJK Line-Height & Width**: Multi-line headings `line-height: 1.35`, body copy `line-height: 1.68`, max measure `60ch` to eliminate eye fatigue.
- **Touch & Keyboard Accessibility**: Minimum `44px` interactive height/touch targets on mobile, visible `:focus-visible` rings, `prefers-reduced-motion` support, and color-blind-safe shape+text status indicators.

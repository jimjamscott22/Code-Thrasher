# UI refresh — design working files

Source artboards for the Code Thrasher UI refresh proposal. These are
Design Component files (`.dc.html`) laid out by `canvas.json`; they are
design references, not application code, and nothing here is imported by
`client/`.

## Artboards

| File | What it proposes |
| --- | --- |
| `Main.dc.html` | Logged-out hero / landing at 1440px. Today a signed-out visitor lands on the bare "Exercises" heading plus the login prompt box. |
| `HeroMobile.dc.html` | The same hero at 390px. |
| `Dashboard.dc.html` | Filter bar (difficulty chips, unsolved-only, search), section headers with counts and per-category progress, and exercise cards that differentiate solved / attempted / untouched. |
| `States.dc.html` | Skeleton loading cards, a designed empty state, and the post-submit result panel. |

## Tokens

Everything lifts existing values — no new palette:

- brand `#22c55e` / `#16a34a` / `#15803d` (`tailwind.config.js`)
- ground `#030712` (gray-950), cards `#111827` (gray-900), hover `#1f2937`
- borders `#1f2937`, text `#f3f4f6` / `#9ca3af` / `#6b7280` / `#4b5563`
- difficulty chips: `#4ade80` / `#facc15` / `#f87171` at `/10` fill, `/20` ring
- JetBrains Mono for the wordmark, section heads and numerics
- radii 8 / 12 / 16px; the `0 0 36px rgba(34,197,94,0.08)` glow already used
  on the editor panel in `ExerciseDetail.tsx`

## Notes for implementation

- The dashboard card states use data already in `useProgressStore`
  (`best_score`, `attempts`, `solved`) — no backend change needed.
- The post-submit panel surfaces `User.total_score` and `User.streak`,
  which the API already returns and the UI currently never displays.
- `client/index.html` loads JetBrains Mono at weights `400;500` only, but
  the wordmark and section heads request 600/700, so those are currently
  synthetically bolded. Add `600;700` to the font URL.

## Regenerating the canvas

The published canvas is built from these files with the `/design` skill's
seeder; the seeded output is gitignored because it embeds the editor
(~2.5 MB). Re-run the seeder with all four artboards plus `canvas.json`
after editing anything here.

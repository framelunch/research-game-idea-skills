# Source Weighting and Filter Application

## Date Range Logic

The scripts automatically determine the correct date range based on `{year}`:

| Specified year | Date range used |
|----------------|-----------------|
| Past year (e.g. 2024 when current year is 2026) | Full calendar year: Jan 1 – Dec 31 |
| Current year (e.g. 2026 when current year is 2026) | Rolling 12-month window: exactly one year ago → today |

The rolling window is used for the current year because the calendar year hasn't finished — it ensures a full year of data is always available.

---

## Weighting Sources by `{market_focus}`

After collecting data from all four sources, weight their signals according to the user's target market:

| `{market_focus}` | Primary sources | Deprioritize |
|------------------|-----------------|--------------|
| **国内** | Qiita (heaviest), Reddit, HN | Ideas without clear Japanese market fit |
| **海外** | Reddit (heaviest), HN | Japan-specific ideas |
| **両方** | All four sources equally | Nothing by default |

**Indie Hackers is always a cross-cutting source regardless of `{market_focus}`.** Use IH data to validate that a niche is actively generating revenue or growing — not as a primary signal of player demand.

---

## Applying `{genre_filter}` in Synthesis

If the user specified one or more genres:

- Prioritize ideas that match the specified genre(s).
- Discard strong signals from unrelated genres.
- Exception: if no relevant signals exist for the specified genre(s), note the gap explicitly rather than fabricating results.

If `{genre_filter}` is "指定なし", consider all genres equally.

---

## Growth Signal Filter

When synthesizing ideas, check whether any Indie Hackers post or product provides evidence that the niche is **actively growing** (e.g., a founder reporting revenue, user growth, or faster-than-expected traction).

- If IH traction evidence exists for an idea → label it **「成長中ニッチ確認済み」** in the report.
- If no IH evidence exists, omit the label. Do not penalize the idea — absence of IH data is not a negative signal, only positive IH data is meaningful here.

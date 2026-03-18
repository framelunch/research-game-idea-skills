# Indie Hackers Research Guide

## Goal

Find game-related discussions, product launches, and revenue data from Indie Hackers to surface **growing niche markets** and validated business opportunities for small indie game teams.

## Why Indie Hackers for Game Research

IH is where indie developers share **actual revenue numbers, growth trajectories, and lessons learned**. Unlike Reddit (player complaints) or HN (technical discussion), IH provides:

- Real MRR/ARR data from indie game developers
- Founder interviews on what worked and what didn't
- Early signals of **emerging niches** before they hit mainstream coverage
- Discussion threads where developers openly compare markets and monetization strategies

High vote counts on IH (20+) indicate the topic resonates with practitioners, not just observers.

## アクセス方法

Indie Hackers には公開APIが存在せず、JSレンダリングのため HTMLスクレイピングも機能しない。**WebSearch を直接使う**のが唯一の実用的な方法。

---

## Search Strategies（WebSearch クエリ）

### 基本クエリ
```
site:indiehackers.com game {year}
site:indiehackers.com indie game revenue {year}
site:indiehackers.com "game" "monthly revenue" {year}
indiehackers.com "launched a game" OR "released a game" {year}
indiehackers.com game niche growing {year}
```

### ジャンル別
```
site:indiehackers.com roguelike
site:indiehackers.com "mobile game" revenue
site:indiehackers.com "puzzle game" OR "casual game" traction
site:indiehackers.com "cozy game" OR "idle game"
site:indiehackers.com "merge game" OR "crafting game"
```

### 成長ニッチ発見用
```
indiehackers.com "unexpected" game audience {year}
indiehackers.com game "I didn't expect" OR "blew up" {year}
indiehackers.com indie game "solo dev" revenue {year}
```

---

## What Signals to Extract

各 WebSearch 結果から以下を記録する：

1. **Revenue mentions** — "$X MRR", "reached $X/month", "crossed $X ARR" — 収益の実証
2. **Growth trajectory language** — "growing fast", "unexpected audience", "niche I didn't expect"
3. **Market gap statements** — "nobody was doing X", "I searched and couldn't find a game that..."
4. **Platform mentions** — mobile / Steam / browser で成長中の未開拓エリア
5. **Team size** — solo または 2人チームでトラクションを得た事例

## Patterns That Signal Growing Niche Markets

- **Founder reports faster-than-expected growth in an unusual genre** — そのニッチが加熱中のシグナル
- **Multiple founders independently mentioning the same underserved market** — コンセンサスシグナル
- **"I built this for myself and it blew up"** — 潜在需要が満たされていなかったことの証拠
- **Game categories where founders report high revenue with minimal marketing** — 市場がオーガニックに引っ張る
- **Cross-platform success of a niche concept** — PC → モバイル等で新規オーディエンスを発見

## Red Flags

- 収益がYouTuber一本バズりに起因する一過性のもの
- MRR データなし・「数千ユーザー」のような曖昧な主張のみ
- 直近の IH 投稿が軒並み失敗報告になっているニッチ
- 西洋市場向けで日本語化パスが見えないゲーム（`{market_focus}` = 国内の場合）

## Output

WebSearch 結果から 5〜8 件の IH 投稿を選び、タイトル・URL・市場シグナルの要約をまとめる。収益データがある場合は必ず記録する。最も強い「成長中ニッチ」シグナルを synthesis ステップに渡す。

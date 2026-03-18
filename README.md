# research-game-idea-skills

小規模インディーチーム（1〜3人）向けに、**穴場のゲームアイデア**を調査・発掘するスキル。

---

## 概要

Reddit のペインポイント、Hacker News の高エンゲージメント投稿、Qiita の個人開発者記事、Indie Hackers のファウンダー議論をリサーチし、モバイルアプリ・Steam 向けの未開拓ゲーム機会と**成長中のニッチ市場**を特定します。Qiita により**国内市場（日本語圏）の需要**も、Indie Hackers により**実際に収益が出ているニッチの検証**も行えます。

**トリガーワード例:**
- 「穴場のゲームを探したい」「ゲームアイデア調査」「インディーゲーム市場」「成長中のニッチ市場」
- "find game ideas", "market gap", "underserved game niche", "growing niche"

---

## ファイル構成

```
research-game-idea-skills/
├── SKILL.md                          # スキル本体（Claude への指示）
├── README.md                         # このファイル
├── .env                              # APIトークン（.gitignore で除外、リポジトリ非管理）
├── .gitignore                        # .env などの機密ファイルを除外
├── memo.txt                          # 作成時のメモ
├── scripts/
│   ├── fetch_reddit.py               # Reddit からゲーム関連投稿を収集するスクリプト
│   ├── fetch_hn.py                   # Hacker News からゲーム関連投稿を収集するスクリプト
│   ├── fetch_qiita.py                # Qiita からゲーム関連記事を収集するスクリプト
│   └── fetch_indiehackers.py         # 未使用（IH はAPI・スクレイピング不可のため WebSearch で代替）
├── references/
│   ├── source-weighting.md           # ソース重み付け・フィルター適用ルール・日付範囲ロジック
│   ├── reddit-research.md            # Reddit 調査手順・対象サブレディット一覧
│   ├── hackernews-research.md        # Hacker News 調査手順・シグナル抽出方法
│   ├── qiita-research.md             # Qiita 調査手順・日本語市場シグナル抽出方法
│   ├── indiehackers-research.md      # Indie Hackers 調査手順・成長中ニッチシグナル抽出方法
│   ├── evaluation-framework.md       # 5軸評価フレームワーク（採点基準）+ 成長シグナルラベル
│   └── output-template.md           # レポート出力テンプレート（日本語）
└── report/
    └── {year}/
        └── {YYYY-MM-DD}/
            └── report_{HHmmss}.md   # 調査レポート（実行ごとに生成）
```

---

## 使い方

スキルを呼び出すと、Claude が以下のステップで調査を進めます。

### Step 1: 調査パラメーターの確認

実行時に以下の3点を日本語で確認します。

1. **調査対象の年号**（例：2024年）
2. **ゲームジャンル**（複数選択可。「指定なし」なら全ジャンル対象）
3. **ターゲット市場**（国内／海外／両方）

ソース重み付け・フィルター適用ルール・日付範囲ロジックは `references/source-weighting.md` に記載されています。

### Step 2: リサーチ（スクリプト実行）

スクリプトを使ってデータを自動収集します（4ソース並行実行）。

```bash
# Reddit: 17サブレディットからゲーム関連投稿を収集
python scripts/fetch_reddit.py --year {year} --output /tmp/reddit_raw.json

# Hacker News: ゲーム関連クエリで投稿を収集
python scripts/fetch_hn.py --year {year} --output /tmp/hn_raw.json

# Qiita: 日本語ゲーム開発記事を収集（国内市場向け）
python scripts/fetch_qiita.py --year {year} --output /tmp/qiita_raw.json

# Indie Hackers: ゲーム関連投稿・プロダクトを収集（成長中ニッチ検証向け）
# Indie Hackers: WebSearch で直接調査（スクリプト不使用）
# → references/indiehackers-research.md のクエリを参照
```

| ソース | スクリプト | 収集対象 | 強み |
|--------|-----------|----------|------|
| **Reddit** | `fetch_reddit.py` | r/patientgamers, r/indiegaming, r/iosgaming 等17サブレディット | 英語圏のペインポイント |
| **Hacker News** | `fetch_hn.py` | "indie game", "Show HN game", "roguelike" 等15クエリ | 技術者・アーリーアダプターの嗜好 |
| **Qiita** | `fetch_qiita.py` | 個人開発・インディーゲーム・Unity/Godot 等12クエリ | **国内市場の生の声・DL/売上データ**（QIITA_TOKEN で認証アクセス推奨） |
| **Indie Hackers** | WebSearch（スクリプト不使用） | `site:indiehackers.com game` 等のクエリで直接検索 | **成長中ニッチの収益検証**（MRR・実ファウンダーのトラクションデータ）API・スクレイピング不可のため WebSearch が唯一の手段 |

**スクリプトのオプション:**

```bash
# 取得件数・出力先を変更する場合
python scripts/fetch_reddit.py --year 2024 --limit 50 --output /tmp/reddit_raw.json
python scripts/fetch_hn.py --year 2024 --min-points 10 --output /tmp/hn_raw.json
python scripts/fetch_qiita.py --year 2024 --min-likes 5 --output /tmp/qiita_raw.json

# 調査対象を一部のサブレディット／クエリに絞る場合
python scripts/fetch_reddit.py --year 2024 --subreddits indiegaming,iosgaming,cozygames --output /tmp/reddit_raw.json
python scripts/fetch_hn.py --year 2024 --queries "indie game,cozy game,roguelike" --output /tmp/hn_raw.json
python scripts/fetch_qiita.py --year 2024 --queries "インディーゲーム,個人開発 ゲーム リリース" --output /tmp/qiita_raw.json

# Qiita: .env からトークンを読み込んで認証アクセス（取得上限引き上げ）
QIITA_TOKEN=$(grep '^QIITA_TOKEN=' .env | cut -d= -f2) \
  python scripts/fetch_qiita.py --year 2024 --output /tmp/qiita_raw.json
```

> **注意:** `.env` には API トークンが含まれるため、`.gitignore` によりバージョン管理から除外されています。リポジトリをクローンした場合は、`.env` ファイルを手動で作成し `QIITA_TOKEN=<your_token>` を設定してください。

### Step 3: ゲームアイデアの合成

調査結果から **3〜5個** の穴場ゲームアイデアを特定。以下の条件を満たすものを選定：

- 実ユーザーのペインポイントや未充足の欲求に基づく
- 1〜3人チームで実現可能
- モバイルまたは Steam での収益化パスがある

### Step 4: レポート保存・提示

- レポートを `report/{year}/{YYYY-MM-DD}/report_{HHmmss}.md` に保存
- チャットで**日本語のサマリー**を提示（スコア表 + 各アイデアの詳細）

---

## 評価フレームワーク（5軸・各5点満点）

| 評価軸 | 概要 |
|--------|------|
| **実現可能性** | 小規模チームで技術的に実現できるか |
| **開発期間** | MVPをどれだけ早く出荷できるか（短いほど高スコア） |
| **収益性** | 明確な収益モデルと市場規模があるか |
| **競合優位性** | ニッチが本当に未開拓か |
| **小規模開発適性** | インディーチームの強みを活かせるか |

**総合スコア（25点満点）の評価基準:**

| スコア | グレード |
|--------|----------|
| 20〜25 | 優秀 — 強力な候補 |
| 14〜19 | 良好 — 検討価値あり |
| 8〜13  | 普通 — 対処すべきリスクあり |
| 7以下  | 弱い — 見送りを推奨 |

---

## レポート出力フォーマット

冒頭に全アイデアのスコアをまとめたサマリー表を置き、続いて各アイデアの詳細を記載します。

各アイデアには以下が含まれます：
- 対象プラットフォーム・**ターゲット市場（国内/海外/両方）**・一言ピッチ
- コンセプト説明（ゲームループ・ターゲット層・面白さ）
- 調査ソース（Reddit / HN / Qiita のシグナル）
- 穴場である理由
- 5軸評価表
- **MVP スコープ**（Must Have / Out of Scope / 完成の定義）
- 次のアクション案（バリデーション・プロトタイプのステップ）

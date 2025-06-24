# 🏗️ 新卒研修プロジェクト — Clean Architecture & Postgres Hands-On

このリポジトリは、新卒エンジニアが **PostgreSQL・トランザクション制御・Clean Architecture・GitHub CI/CD** を実践的に学ぶための演習プロジェクトです。簡易的な「タスク管理 API」を題材とし、ドメイン層〜インフラ層までを段階的に実装します。

---

## 📋 前提条件

| ツール/環境 | バージョン例 | 備考 |
|-------------|-------------|------|
| Docker / Docker Compose | 24.x 以上 | DB・CI/CD コンテナ実行用 |
| Go (または TypeScript など言語は自由) | 1.22 / 21.x など | Clean Architecture 実装用 |
| PostgreSQL | 16.x（Docker イメージ） | ローカル実行はコンテナ推奨 |
| Make または Taskfile | 最新 | コマンド定義用 |
| Git | 2.40 以上 | PR フロー学習用 |
| GitHub Actions | — | CI/CD 実行基盤 |

> ※ 会社 PC の標準環境にないツールは、`./devcontainer` または Docker 上で完結します。

---

## 🚀 セットアップ手順

```bash
# 1. リポジトリをクローン
git clone git@github.com:your-org/newgrad-clean-arch.git
cd newgrad-clean-arch

# 2. 開発用コンテナを立ち上げ
docker compose up -d

# 3. DB マイグレーション
make migrate  # or: task migrate

# 4. 単体テストを実行
make test


⸻

▶️ アプリ実行

# API サーバ起動
make run          # localhost:8080 で待ち受け

# Swagger UI 生成 & 起動 (任意)
make docs


⸻

🎯 学習目標
	1.	PostgreSQL の基本操作
	•	DDL/DML、インデックス、トランザクション分離レベル
	2.	トランザクション／ロールバック／リカバリー
	•	BEGIN … COMMIT/ROLLBACK、障害発生時のリカバリー手順
	3.	GitHub Flow & CI/CD
	•	Pull Request → Review → Merge → GitHub Actions による自動テスト
	4.	テスト技法
	•	リポジトリ層のモック化／UseCase 層のユースケーステスト
	•	コンテナを用いた結合テスト
	5.	Clean Architecture
	•	domain ↔ usecase ↔ interface ↔ infrastructure 4 層構造
	•	依存関係逆転の原則 (DDD との対比学習)

⸻

🛠 技術要素の補足

Postgres の扱い
	•	コンテナ上で起動 (docker compose) し、src/infra/postgres に接続設定を配置。
	•	マイグレーションは [golang-migrate／dbmate] などを利用。

トランザクション管理
	•	Repository メソッドは tx *sql.Tx を受け取る形にし、UseCase でまとめて制御。
	•	擬似障害テストとして「途中で panic → ロールバックされること」を確認するテストを用意。

GitHub CI/CD
	•	.github/workflows/ci.yml にて Lint → UnitTest → IntegrationTest を実行。
	•	main ブランチへの直接 push を禁止し、PR マージ時のみデプロイ用ジョブをトリガー。

テスト
	•	UnitTest は 依存をモック化、IntegrationTest は Docker-Compose 上の本物 DB と通信。
	•	カバレッジは 80 %以上を目標。

Clean Architecture の構成

src/
 ├── domain        # エンティティ、値オブジェクト、リポジトリIF
 ├── usecase       # ユースケース & ポート
 ├── interface     # ハンドラ、GraphQL/REST、Presenter
 └── infrastructure# DB, 外部API, Logger, Migration


⸻

📚 参考リンク
	•	Clean Architecture 原著（Robert C. Martin）
	•	PostgreSQL 公式ドキュメント 16
	•	Effective Go / Go Modules

---

## テストリスト

```markdown
# ✅ テスト設計

## 1. 単体テスト (Unit Tests) — 例

| No. | テスト対象 | シナリオ | 期待結果 |
|-----|------------|---------|---------|
| U-01 | `TaskRepository.Insert` | 有効な Task を追加 | 返却 ID が auto-increment され、エラーなし |
| U-02 | `TaskRepository.FindByID` | 既存 ID を検索 | 一致する Domain Entity が返る |
| U-03 | `CreateTaskUseCase` | タイトル前後に空白を含む入力 | 空白が Trim された状態で保存 |
| U-04 | `CreateTaskUseCase` | DB 例外発生 (モックで強制エラー) | トランザクションがロールバックし、エラーを返す |
| U-05 | `HTTP Handler /tasks` | バリデーション NG (タイトル空) | 400 Bad Request & エラーメッセージ |

## 2. 結合テスト (Integration Tests) — 例

| No. | テストシナリオ | 手順 | 合格基準 |
|-----|---------------|------|---------|
| I-01 | タスク登録〜取得 E2E | REST POST `/tasks` → GET `/tasks/{id}` | 登録した内容が完全一致 |
| I-02 | 途中障害時のロールバック | Tx 中に APP 強制終了 → 再起動 | 中途半端なデータが残存しない |
| I-03 | リカバリー動作確認 | `pg_dump` でバックアップ → DB を drop → `pg_restore` | すべてのタスクデータが復元 |

## 3. テスト実行コマンド例

```bash
# 単体テスト & カバレッジ
make test           # = go test ./... -cover

# 結合テスト（DB コンテナ込み）
make integration    # = docker compose -f docker-compose.test.yml up --build --abort-on-container-exit

# すべて (CI と同一フロー)
make ci

---

**使い方のヒント**

- README から*学習目標*を眺めつつ、Pull Request ごとに 1 つのテーマ（例: リポジトリ層 → ユースケース層 → ハンドラ層…）を実装していく流れが効果的です。
- CI でテストが落ちた場合は、Green になるまで自分で修正 → 再 push → 再実行を体験させると、DevOps 思考が身に付きます。
- Clean Architecture のレイヤは最初は肥大化しがちなので、*インターフェースを明示する*ことを重視し、実装コードは小さく保ちましょう。

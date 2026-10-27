# 指定ライブラリのみを Databricks で利用する設定ガイド

Git フォルダで連携している指定ライブラリだけを Databricks（Serverless / Classic）で使えるようにし、
PyPI や GitHub など外部からのライブラリのインストールを遮断するための手順とサンプルです。

```
CodeCommit などの Git リポジトリ（指定ライブラリ）
   │ Git フォルダで連携
   ▼
Databricks Git フォルダ
   │ wheel をビルド
   ▼
Unity Catalog Volume
   ├─ Serverless：ワークスペースのベース環境に登録
   └─ Classic　 ：コンピュートポリシーに登録
   ▼
ノートブック・ジョブで使える

PyPI・GitHub など ── 遮断（Serverless：ネットワークポリシー／Classic：VPC の出口制御）
```

## 手順書

画面操作つきの設定手順（Serverless・Classic）

| 形式 | ファイル |
|---|---|
| Markdown（GitHub 上で閲覧） | [docs/setup-guide.md](docs/setup-guide.md) |
| PDF | [docs/setup-guide.pdf](docs/setup-guide.pdf) |
| Word | [docs/setup-guide.docx](docs/setup-guide.docx) |

## サンプル

| ファイル | 用途 | 手順書の該当箇所 |
|---|---|---|
| [notebooks/build_wheel.py](notebooks/build_wheel.py) | Git フォルダのソースから wheel を作り、Volume に置く | 手順3 |
| [notebooks/pull_git_folder.py](notebooks/pull_git_folder.py) | Git フォルダを最新に更新する（ジョブで自動化する場合） | 手順3 |
| [notebooks/verify_library_control.py](notebooks/verify_library_control.py) | 指定ライブラリが使え、外部からのインストールが失敗することを確認する | 手順6 / C-5 |
| [config/approved-base-env.yaml](config/approved-base-env.yaml) | ワークスペースのベース環境の定義 | 手順4 |
| [config/network-policy.json](config/network-policy.json) | ネットワークポリシー（外部通信をすべて遮断）の API 用定義 | 手順5 |
| [config/compute-policy.json](config/compute-policy.json) | コンピュートポリシーの定義（アクセスモード固定） | 手順C-3 |
| [config/job.json](config/job.json) | プル → wheel ビルドのジョブ定義 | 手順3 |

ノートブックは Databricks のソース形式（`.py`）です。ワークスペースの「インポート」から取り込めます。
`<カタログ>`、`<Git フォルダ名>` などの `<...>` は、環境に合わせて書き換えてください。

## CLI で設定する場合（参考）

```bash
# ワークスペースのベース環境を作成し、Serverless の既定に設定
databricks environments create-workspace-base-environment "承認済みライブラリ環境" \
  --workspace-base-environment-id approved-libs --base-environment-type CPU \
  --filepath /Workspace/approved-libs/approved-base-env.yaml -p <ワークスペースのプロファイル>
databricks environments update-default-workspace-base-environment \
  default-workspace-base-environment cpu_workspace_base_environment \
  --cpu-workspace-base-environment workspace-base-environments/approved-libs -p <ワークスペースのプロファイル>

# ライブラリ更新後の反映
databricks environments refresh-workspace-base-environment \
  workspace-base-environments/approved-libs -p <ワークスペースのプロファイル>

# ネットワークポリシーの作成とワークスペースへの割り当て（アカウント管理者）
databricks account network-policies create-network-policy-rpc \
  --json @config/network-policy.json -p <アカウントのプロファイル>
databricks account workspace-network-configuration update-workspace-network-option-rpc <ワークスペースID> \
  --json '{"workspace_id":<ワークスペースID>,"network_policy_id":"approved-libs-only"}' -p <アカウントのプロファイル>

# プル → wheel ビルドのジョブ
databricks jobs create --json @config/job.json -p <ワークスペースのプロファイル>
```

## 前提・留意事項

- Serverless の外部通信制御（ネットワークポリシー）には Enterprise プランが必要です
- Classic の外部通信制御には、顧客管理 VPC で作成したワークスペースが必要です
- 依存パッケージがあるライブラリは、依存パッケージの wheel も Volume に置いてください
- 実行時に外部からデータやモデルを取得するライブラリは、外部通信の遮断後は実行時に失敗します
- Classic の手順は公式ドキュメントに基づくものです。導入時に環境で動作確認してください

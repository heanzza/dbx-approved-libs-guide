# Databricks notebook source
# MAGIC %md
# MAGIC # Git フォルダを最新に更新（プル）
# MAGIC ジョブで wheel ビルドの前に実行する。実行ユーザー（またはサービスプリンシパル）に Git 認証情報が登録されている必要がある。

# COMMAND ----------

from databricks.sdk import WorkspaceClient

dbutils.widgets.text("repo_path", "/Workspace/approved-libs/<Git フォルダ名>")
dbutils.widgets.text("branch", "main")
repo_path = dbutils.widgets.get("repo_path")
branch = dbutils.widgets.get("branch")

w = WorkspaceClient()
repo_id = w.workspace.get_status(repo_path).object_id
w.repos.update(repo_id, branch=branch)
r = w.repos.get(repo_id)
print(r.path, r.branch, r.head_commit_id)

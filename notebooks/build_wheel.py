# Databricks notebook source
# MAGIC %md
# MAGIC # 指定ライブラリの wheel ビルド＆Volume 配置
# MAGIC Git フォルダのソースを wheel にし、Unity Catalog Volume にコピーする（手順3）。
# MAGIC 外部通信を遮断した環境でもビルドできるよう `--no-deps --no-build-isolation` を使う。

# COMMAND ----------

dbutils.widgets.text("src", "/Workspace/approved-libs/<Git フォルダ名>")
dbutils.widgets.text("dest", "/Volumes/<カタログ>/lib_mgmt/approved_wheels")
src = dbutils.widgets.get("src")
dest = dbutils.widgets.get("dest")

# COMMAND ----------

import glob, os, shutil, subprocess, sys, tempfile

work = tempfile.mkdtemp()
pkg = os.path.join(work, "pkg")
shutil.copytree(src, pkg, ignore=shutil.ignore_patterns(".git*", "dist", "build", "*.egg-info"))
out = os.path.join(work, "dist")
subprocess.run(
    [sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation", "-w", out, pkg],
    check=True,
)
for whl in glob.glob(f"{out}/*.whl"):
    shutil.copy(whl, dest)
    print("配置しました:", os.path.join(dest, os.path.basename(whl)))

# COMMAND ----------

display(dbutils.fs.ls(dest))

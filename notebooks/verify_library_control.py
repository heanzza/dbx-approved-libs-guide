# Databricks notebook source
# MAGIC %md
# MAGIC # 動作確認（手順6 / C-5）
# MAGIC 1. 指定ライブラリが import できる
# MAGIC 2. PyPI からのインストールが失敗する
# MAGIC 3. GitHub からのインストールが失敗する

# COMMAND ----------

dbutils.widgets.text("module", "<ライブラリのモジュール名>")
module = dbutils.widgets.get("module")

# COMMAND ----------

# 1. 指定ライブラリ → 成功するのが正しい
import importlib
m = importlib.import_module(module)
print(module, getattr(m, "__version__", "(no __version__)"))

# COMMAND ----------

# 2. PyPI → 失敗するのが正しい
import subprocess, sys
r = subprocess.run([sys.executable, "-m", "pip", "install", "--index-url", "https://pypi.org/simple",
                    "--timeout", "10", "--retries", "0", "emoji"], capture_output=True, text=True)
print("returncode =", r.returncode)
print(r.stderr[-600:])
assert r.returncode != 0, "PyPI からインストールできてしまった（外部通信が遮断されていない）"

# COMMAND ----------

# 3. GitHub → 失敗するのが正しい
r = subprocess.run([sys.executable, "-m", "pip", "install", "--timeout", "10", "--retries", "0",
                    "git+https://github.com/carpedm20/emoji.git"], capture_output=True, text=True)
print("returncode =", r.returncode)
print(r.stderr[-600:])
assert r.returncode != 0, "GitHub からインストールできてしまった（外部通信が遮断されていない）"

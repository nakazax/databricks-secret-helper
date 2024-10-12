# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks Secret Helper
# MAGIC This notebook is designed for managing secrets in Databricks, including setting up secret scopes and keys.

# COMMAND ----------

from databricks.sdk import WorkspaceClient
import pandas as pd

w = WorkspaceClient()

# COMMAND ----------

dbutils.widgets.text("secret_scope", "hinak-secret-scope", "Name of Secret Scope")
dbutils.widgets.text("secret_key", "", "Secret Key")
dbutils.widgets.text("secret_value", "", "Secret Value")

secret_scope = dbutils.widgets.get("secret_scope")
secret_key = dbutils.widgets.get("secret_key")
secret_value = dbutils.widgets.get("secret_value")

# COMMAND ----------

# MAGIC %md
# MAGIC ## List secret scopes

# COMMAND ----------

scope_list = [{"name": scope.name, "backend_type": str(scope.backend_type)} 
              for scope in w.secrets.list_scopes()]

if scope_list:
    df_scopes = pd.DataFrame(scope_list)
    display(df_scopes)
else:
    print("No secret scopes found.")
    df_scopes = pd.DataFrame(columns=["name", "backend_type"])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create secret scope if not exists

# COMMAND ----------

if secret_scope not in df_scopes['name'].values:
    try:
        w.secrets.create_scope(scope=secret_scope)
        print(f"Secret scope '{secret_scope}' created successfully.")
    except Exception as e:
        print(f"Error creating secret scope: {str(e)}")
else:
    print(f"Secret scope '{secret_scope}' already exists.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Put secret

# COMMAND ----------

try:
    w.secrets.put_secret(scope=secret_scope, key=secret_key, string_value=secret_value)
    print(f"Secret '{secret_key}' added to scope '{secret_scope}' successfully.")
except Exception as e:
    print(f"Error adding secret '{secret_key}' to scope '{secret_scope}': {str(e)}")

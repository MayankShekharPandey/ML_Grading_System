import sqlite3
from pathlib import Path

DB_PATH = Path("hmm_hyperparameter_tuning.db").resolve()
OLD_PATH = "/content/mlruns"
NEW_PATH = (Path.cwd() / "mlruns").resolve().as_posix()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Update experiment artifact locations
cursor.execute("""
    UPDATE experiments
    SET artifact_location = REPLACE(artifact_location, ?, ?)
    WHERE artifact_location LIKE ?
""", (OLD_PATH, NEW_PATH, OLD_PATH + "%"))

experiments_updated = cursor.rowcount

# Update individual run artifact locations
cursor.execute("""
    UPDATE runs
    SET artifact_uri = REPLACE(artifact_uri, ?, ?)
    WHERE artifact_uri LIKE ?
""", (OLD_PATH, NEW_PATH, OLD_PATH + "%"))

runs_updated = cursor.rowcount

conn.commit()

print("Database path:", DB_PATH)
print("New artifact path:", NEW_PATH)
print("Experiments updated:", experiments_updated)
print("Runs updated:", runs_updated)

conn.close()
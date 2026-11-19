
import sqlite3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "database" / "random_forest_tracking.db"
ARTIFACTS = ROOT / "mlartifacts"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute(
    "UPDATE experiments SET artifact_location=? WHERE experiment_id=1",
    ((ARTIFACTS / "1").resolve().as_uri(),)
)

columns = [r[1] for r in cursor.execute(
    "PRAGMA table_info(runs)"
).fetchall()]

run_col = "run_uuid" if "run_uuid" in columns else "run_id"

cursor.execute(
    f"SELECT {run_col} FROM runs WHERE experiment_id=1"
)

for (run_id,) in cursor.fetchall():
    uri = (
        ARTIFACTS / "1" / run_id / "artifacts"
    ).resolve().as_uri()

    cursor.execute(
        f"UPDATE runs SET artifact_uri=? WHERE {run_col}=?",
        (uri, run_id)
    )

conn.commit()
conn.close()

print("Database and artifact paths configured.")

subprocess.run([
    "mlflow", "ui",
    "--backend-store-uri", f"sqlite:///{DB.as_posix()}",
    "--host", "127.0.0.1",
    "--port", "5000"
], cwd=str(ROOT), check=True)

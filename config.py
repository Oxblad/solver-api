import os
db_link = os.environ.get("DATABASE_URL")
if db_link.startswith("postgres://"):
    db_link = db_link.replace("postgres://", "postgresql://", 1)
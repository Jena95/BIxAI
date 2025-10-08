import os
import bcrypt
import uuid
from jose import JWTError, jwt
from google.cloud import bigquery
from datetime import datetime, timedelta

# Load environment variables
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "brave-reason-421203")
DATASET = os.getenv("BIGQUERY_DATASET", "your_dataset")
USER_TABLE = os.getenv("USER_TABLE", "users")

client = bigquery.Client(project=PROJECT_ID)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_email(email: str):
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET}.{USER_TABLE}`
        WHERE email = @email
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", email)]
    )
    results = list(client.query(query, job_config=job_config))
    return dict(results[0]) if results else None

def create_user(email: str, password: str):
    user = get_user_by_email(email)
    if user:
        raise ValueError("User already exists")

    hashed_pw = hash_password(password)
    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    rows = [{
        "id": user_id,
        "email": email,
        "password": hashed_pw,
        "created_at": created_at,
    }]

    table = client.dataset(DATASET).table(USER_TABLE)
    client.insert_rows_json(table, rows)
    return {"id": user_id, "email": email}

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user["password"]):
        return None
    return user

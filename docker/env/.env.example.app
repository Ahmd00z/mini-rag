APP_NAME="mini-RAG"
APP_VERSION="0.1"
OPENAI_API_KEY=""

FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=512000 # 512KB 

POSTGRES_USERNAME=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_MAIN_DATABASE=

# ========================= LLM Config =========================
# تقدر تبدل بين OPENAI و COHERE و GEMINI
GENERATION_BACKEND="GEMINI"
EMBEDDING_BACKEND="COHERE"

OPENAI_API_KEY=""
OPENAI_API_URL=""
COHERE_API_KEY=""
GEMINI_API_KEY=""

# لو هتستخدم Gemini خليها: gemini-1.5-flash أو gemini-pro
# لو هتستخدم OpenAI خليها: gpt-3.5-turbo-0125
GENERATION_MODEL_ID=

EMBEDDING_MODEL_ID="embed-multilingual-light-v3.0"
EMBEDDING_MODEL_SIZE=384

INPUT_DAFAULT_MAX_CHARACTERS=1024
GENERATION_DAFAULT_MAX_TOKENS=300
GENERATION_DAFAULT_TEMPERATURE=0.1

# ========================= Vector DB Config =========================
VECTOR_DB_BACKEND_LITERAL = ["QDRANT", "PGVECTOR"]
VECTOR_DB_BACKEND = "PGVECTOR"
VECTOR_DB_PATH = "qdrant_db"
VECTOR_DB_DISTANCE_METHOD = "cosine"
VECTOR_DB_PGVEC_INDEX_THRESHOLD =
=

# ========================= Template Configs =========================
PRIMARY_LANG = "en"
DEFAULT_LANG = "ar"

# ========================= Celery Task Queue Config =========================
CELERY_BROKER_URL="amqp://minirag_user:minirag_rabbitmq_2222@localhost:5672/minirag_vhost"
CELERY_RESULT_BACKEND="redis://:minirag_redis_2222@localhost:6379/0"
CELERY_TASK_SERIALIZER="json"
CELERY_TASK_TIME_LIMIT=600
CELERY_TASK_ACKS_LATE=false
CELERY_WORKER_CONCURRENCY=2
CELERY_FLOWER_PASSWORD="minirag_flower_2222"
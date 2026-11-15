FROM node:22-slim AS frontend
WORKDIR /front
COPY package.json package-lock.json ./
RUN npm ci
COPY vite.config.js index.html ./
COPY src/ ./src/
COPY public-parallax/ ./public-parallax/
ARG PARALLAX_COMMIT=development
ENV VITE_PARALLAX_EXPANDED=1 VITE_PARALLAX_COMMIT=$PARALLAX_COMMIT
RUN npm run build

FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HF_HUB_DISABLE_TELEMETRY=1 TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=2 PARALLAX_MODEL_CACHE=/models
WORKDIR /app
COPY deploy/requirements-api.txt /tmp/requirements-api.txt
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && pip install --no-cache-dir -r /tmp/requirements-api.txt
RUN python -c "from sentence_transformers import SentenceTransformer; m=SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',cache_folder='/models'); assert m.get_sentence_embedding_dimension()==384"
COPY pipeline/__init__.py pipeline/common.py pipeline/check.py pipeline/prompts.py pipeline/embeddings.py pipeline/text.py pipeline/presentation.py /app/pipeline/
COPY service/ /app/service/
COPY --from=frontend /front/dist /app/frontend/
COPY deploy/previous-assets/ /app/frontend/assets/
RUN mkdir -p /app/work/parallax
ENV HF_HUB_OFFLINE=1 PARALLAX_BIND=0.0.0.0 PARALLAX_PORT=18808 PARALLAX_DB_SOCKET=/run/mysqld/mysqld.sock PARALLAX_WORK_DIR=/tmp/parallax
USER 10001:999
EXPOSE 18808
CMD ["python","-m","service.app"]

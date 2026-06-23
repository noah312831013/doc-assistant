# ─── Stage 1: builder ───────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# 先 copy 依賴檔，讓 Docker 快取這層
# （只要 requirements.txt 沒變，下次 build 這層不重跑）
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─── Stage 2: runtime ───────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# 只從 builder 拿裝好的 packages，不帶 pip、setuptools 等工具進來
COPY --from=builder /install /usr/local

WORKDIR /app
COPY app/ ./app/

# 非 root 使用者執行（安全最佳實踐）
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

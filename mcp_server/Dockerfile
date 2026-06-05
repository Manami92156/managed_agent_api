FROM python:3.11-slim-bookworm as builder

WORKDIR /build
# カレントディレクトリにある設定ファイルをコピー
COPY pyproject.toml uv.lock ./

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# uvを使って依存関係を requirements.txt にコンパイル
RUN pip install --no-cache-dir uv && \
    uv pip compile pyproject.toml -o requirements.txt

# ユーザー領域にライブラリをインストール
RUN pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt

# --- 本番用ステージ ---
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=True
ENV APP_HOME=/app
WORKDIR $APP_HOME

# builderからインストール済みのパッケージを丸ごとコピー（Python 3.11用）
COPY --from=builder /root/.local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /root/.local/bin /usr/local/bin

# ============================================
# 📦 今回のソースコードのコピー
# ============================================
# あなたの環境に合わせて、必要なファイルをコンテナに入れます
COPY server.py ./

# Cloud Run用の環境変数設定
ENV HOST=0.0.0.0
ENV PORT=8080

# エントリーポイント（pythonコマンドで直接起動）
CMD ["python", "server.py"]
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    COGNIESL_DATA_DIR=/app/data

ENV PATH=/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl poppler-utils \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Install Node dependencies (root for dom-to-pptx, webui for Next.js)
RUN npm install && cd webui && npm install && node node_modules/next/dist/bin/next build

# Create output directories
RUN mkdir -p /app/mnt /app/activity-logs /app/uploads && \
    chmod -R a+rwx /app/mnt /app/activity-logs /app/uploads

# Install playwright browsers
RUN python -m playwright install chromium

EXPOSE 8080

CMD ["python", "-u", "server.py"]

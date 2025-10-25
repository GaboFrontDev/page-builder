FROM python:3.11-slim

WORKDIR /app

# Install Node.js for React SSG
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ../shared ../shared


# Install Node.js dependencies for SSG
RUN cd nextjs-ssg && rm -rf node_modules package-lock.json && npm install

EXPOSE 3001

# Build SSG and start the application
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 3001 --reload"]
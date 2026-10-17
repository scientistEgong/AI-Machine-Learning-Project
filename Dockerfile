
# 1. Start with a Python runtime
FROM python:3.12-slim

# 2. Configure Python for containerized execution
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# 3. Set the application working directory
WORKDIR /app

# 4. Install a system library commonly needed by ML runtimes
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy dependencies first
COPY requirements.txt .

# 6. Install Python dependencies
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

# 7. Copy the application and required project files
COPY . .

# 8. Document the port used by Streamlit
EXPOSE 8501

# 9. Start the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]

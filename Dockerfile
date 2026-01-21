# 1. Use a lightweight Python base image (The OS)
FROM python:3.9-slim

# 2. Set the working folder inside the container
WORKDIR /app

# 3. Copy only the requirements first (Docker Caching trick for speed)
# We will create this file in a second
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the actual code
COPY producer.py .
COPY consumer.py .

# 6. The Default Command (We override this in docker-compose)
CMD ["python", "producer.py"]
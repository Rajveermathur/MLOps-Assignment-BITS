# Dockerfile
FROM python:3.9.6-slim

# Set a working directory
WORKDIR /app

# Install dependencies early to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY main.py .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

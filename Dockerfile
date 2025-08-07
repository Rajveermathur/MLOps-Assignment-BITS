FROM python:3.9.6-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app code
COPY . .

# Make the start script executable
RUN chmod +x run.sh

# Expose all required ports
EXPOSE 5000 5001 8000 8050

# Run everything
CMD ["./run.sh"]

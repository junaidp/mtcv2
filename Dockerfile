# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "combined_output:app", "--host", "0.0.0.0", "--port", "8000"]

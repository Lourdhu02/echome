# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Generate the item bank data
RUN python generate_real_items.py

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.assessment_app:app", "--host", "0.0.0.0", "--port", "8000"]

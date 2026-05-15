FROM python:3.12-slim

WORKDIR /app

# Avoid Python writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build deps then app deps
COPY requirements-app.txt /app/requirements-app.txt
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements-app.txt

# Copy project
COPY . /app

EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use Python 3.10 slim image for smaller size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything except what's in .dockerignore
# This excludes app.py for now (better caching)
COPY . ./

# Install the core whisper_normalizer package first
# (gets cached unless core package files change)
RUN pip install --no-cache-dir -e .

# Install web API dependencies separately
# (gets cached unless webapp requirements change)
RUN pip install --no-cache-dir -r ./examples/sample_webapp/requirements.txt

# Copy app.py separately (changes frequently)
COPY ./examples/sample_webapp/app.py ./

# Expose the port your app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
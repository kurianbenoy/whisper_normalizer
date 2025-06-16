# Use Python 3.10 slim image for smaller size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything except what's in .dockerignore
# This excludes app.py for now (better caching)
COPY . ./

# Install the package and all dependencies 
# (gets cached unless package files change)
RUN pip install --no-cache-dir -e .

# Copy app.py separately (changes frequently)
COPY app.py ./

# Expose the port your app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
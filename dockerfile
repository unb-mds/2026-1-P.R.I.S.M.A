# Use the official Python runtime image
FROM python:3.13

# Create the app directory
RUN mkdir /src
 
# Install cron daemon
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /src

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/src

# Install uv and sync dependencies from the lockfile
RUN pip install --upgrade pip uv

# Copy dependency manifests first to maximize cache reuse
COPY pyproject.toml uv.lock /src/

# Copy the Django project source
COPY src /src/src

# Copy the container entrypoint that applies migrations before starting Django
COPY docker-entrypoint.sh /src/docker-entrypoint.sh
RUN chmod +x /src/docker-entrypoint.sh

# Install project dependencies with uv
RUN uv sync --frozen --no-dev

# Expose the Django port
EXPOSE 8000

# Apply migrations on startup and then run Django's development server
CMD ["/src/docker-entrypoint.sh"]

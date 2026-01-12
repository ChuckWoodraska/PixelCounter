FROM python:3.12-slim

# Copy uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy the project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install the project's dependencies using the lockfile and settings
# Since we don't have a lock file yet, we use --system to install into system python
# which is fine for a container.
RUN uv pip install --system ".[dev]"

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

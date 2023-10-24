FROM python:3.6.15-slim-buster

ARG UID=1000
ARG GID=1000

# Create a non-root user
RUN groupadd -g "${GID}" gunicorn && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" gunicorn

# Set the working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy the rest of the application files
COPY app ./app
COPY run.py ./entrypoint.py

# Create necessary directories and files
RUN mkdir -p ./app && \
    chown -R gunicorn:gunicorn /app && \
    touch ./app/tags.json && \
    mkdir ./data

# Change to the non-root user
USER gunicorn

# Expose the port
EXPOSE 8000

# Set the entrypoint and command
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8000", "entrypoint:app"]

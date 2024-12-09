# Use the official Python 3.10.10 image as a base
FROM python:3.10.10

# Create a non-root user and set the PATH
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY --chown=user . /app

# Pre-download the Unidic models (if required)
RUN python -m unidic download

# Expose the port for Gunicorn
EXPOSE 5000

# Command to run the application using Gunicorn
CMD ["gunicorn", "-w", "1", "--threads", "1", "-b", "0.0.0.0:5000", "app:app"]


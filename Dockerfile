FROM python:3.11

WORKDIR /app

# Copy app
COPY . /app

# Copy dependencies
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps

# Run the application
CMD uvicorn main:app --host 0.0.0.0 --port 8080

# Dockerfile
# Start from a Python 3 Image 
FROM python:3
# Install Chrome and Webdriver
RUN apt-get update && apt-get install -y wget && \
    wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux64.tar.gz && \
    tar -C /usr/local/bin/ -xzf /tmp/geckodriver.tar.gz && \
    rm -f /tmp/geckodriver.tar.gz
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
# Install the Google SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get install apt-transport-https ca-certificates gnupg curl -y &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - &&\
    apt-get update && apt-get install google-cloud-sdk -y
# Change current directory to /app
WORKDIR /app
COPY .env /app/.env
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy application code to app/
COPY scraper.py .
# Call CMD
CMD ["sh", "-c", "python scraper.py && gsutil cp ./Data/*.csv gs://linkedin_jobs_scraper"]

ARG BUILD_TAG
FROM python:${BUILD_TAG}
ENV PYTHONUNBUFFERED 1

# pip install
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Django directory
COPY django /django

WORKDIR /django

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

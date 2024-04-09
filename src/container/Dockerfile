FROM python:3.10

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/ml/requirements.txt

RUN pip3 install --no-cache-dir -r /opt/ml/requirements.txt

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/ml/code:${PATH}"

ENV SM_MODEL_DIR="/opt/ml/model"
ENV SM_OUTPUT_DATA_DIR="/opt/ml/output"
ENV SM_CHANNEL_TRAIN="/opt/ml/input/data/train"

COPY code /opt/ml/code
WORKDIR /opt/ml/code

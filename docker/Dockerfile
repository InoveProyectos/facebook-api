FROM python:3.9.5

ENV PYTHONUNBUFFERED = 1

WORKDIR /opt/back_end

COPY . .

RUN pip install -r requirements.txt

RUN apt -y update && \
    rm -rf /var/lib/apt/lists/*

CMD python api/app.py

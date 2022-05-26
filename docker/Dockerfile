FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/back_end

COPY . .

RUN apt -y update && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD python crm/manage.py runserver 0.0.0.0:8000
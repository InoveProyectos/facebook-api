FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/back_end

COPY . .

RUN apt -y update && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# Environment variables
ENV POSTGRES_DB=inove
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=ics2022ma-
ENV POSTGRES_HOST=db
# Dejamos DEBUG=True para hacer los retoques antes de pasarlo a False para producción.
ENV DEBUG=True
ENV SECRET_KEY=django-insecure-x_^aet@$di37)k$5vb(kino$6w=px!&@-q4va4so^2c9s@)k8*

RUN python crm/manage.py collectstatic --noinput

# CMD python crm/manage.py runserver 0.0.0.0:8000
CMD gunicorn --chdir /opt/back_end/crm crm.wsgi:application --bind 0.0.0.0:$PORT
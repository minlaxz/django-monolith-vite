ARG PYTHON_VERSION=3.9.18-slim-bullseye
FROM --platform=linux/amd64 python:${PYTHON_VERSION} as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/usr/src/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update -q \
  && apt-get install \
  libpq-dev \
  gcc g++ make \
  python3-dev \
  libffi-dev musl-dev git -yqq

RUN pip install --upgrade pip
COPY ./requirements.txt .
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN pip install -r requirements.txt


FROM --platform=linux/amd64 python:${PYTHON_VERSION} as runner

WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/venv venv

RUN apt-get update -q \
  && apt-get install \
  libpq-dev ncat gettext python3-dev \
  libffi-dev musl-dev git \
  gcc g++ make \
  -yqq

RUN apt-get clean -y

ENV VIRTUAL_ENV=/usr/src/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# ENV _ENV fly

# COPY --from=builder /usr/src/app/wheels /wheels
# COPY --from=builder /usr/src/app/requirements.txt .
# RUN pip install --no-cache /wheels/*
# RUN rm -rf /wheels

# create the app user
ENV HOME=/home/app
RUN mkdir -p ${HOME}
RUN useradd -m -d /home/app -s /bin/bash -c "Container User" -u 1001 app

# create the appropriate directories for django
ENV APP_HOME=/home/app/web
RUN mkdir -p ${APP_HOME}
RUN mkdir ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles ${APP_HOME}/logs
WORKDIR ${APP_HOME}

# copy project
COPY . ${APP_HOME}
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput --clear

EXPOSE 8000
RUN chown -R app:app ${APP_HOME}
USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--log-level", "info", "--log-file", "/home/app/web/logs/gunicorn.log", "--error-logfile", "/home/app/web/logs/gunicorn.error.log", "--access-logfile", "/home/app/web/logs/gunicorn.access.log", "--timeout", "3000", "--graceful-timeout", "3000", "--reload", "django_monolith_vite.wsgi:application"]

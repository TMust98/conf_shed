FROM python:3.8.8

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN mkdir /conf_shed_app

WORKDIR /conf_shed_app

COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev

COPY . ./conf_shed

RUN chmod a+x app.sh

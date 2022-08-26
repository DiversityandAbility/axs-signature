FROM python:3.10

LABEL org.opencontainers.image.source = "https://github.com/DiversityandAbility/hancock"

ENV PYTHONUNBUFFERED=1

ARG GID=0
ARG UID=0

RUN addgroup --gid "$GID" hancock \
    && useradd --uid "$UID" --gid "$GID" --create-home --shell /bin/bash hancock

WORKDIR /usr/src/app
RUN chown hancock:hancock /usr/src/app

USER hancock

RUN python -m venv /home/hancock/venv
ENV VIRTUAL_ENV "/home/hancock/venv"
ENV PATH "/home/hancock/venv/bin:${PATH}"
ENV PYTHONPATH $PYTHONPATH:/usr/src/app/hancock

COPY --chown=hancock:hancock requirements.txt /usr/src/app/
RUN pip install -U pip && pip install -r requirements.txt

COPY --chown=hancock:hancock hancock /usr/src/app/hancock
COPY --chown=hancock:hancock gunicorn.conf.py /usr/src/app/

CMD gunicorn --config gunicorn.conf.py hancock.wsgi:application

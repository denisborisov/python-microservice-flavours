FROM python:3.11-slim as base-image

RUN apt-get update --yes \
    && apt-get upgrade --yes \
    && pip install --no-cache-dir --upgrade pip poetry \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf ~/.cache

FROM scratch AS runtime-image

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1

COPY --from=base-image / /

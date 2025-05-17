FROM python:3.12-alpine

RUN apk add --no-cache curl build-base cargo
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

RUN mkdir "LMS"
WORKDIR /LMS

COPY pyproject.toml .
COPY uv.lock .
COPY requirements.txt .

COPY ./src ./src

RUN uv sync

CMD ["/bin/sh"]
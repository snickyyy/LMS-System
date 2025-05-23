#!/bin/sh

. .venv/bin/activate && cd src && uvicorn main:app --reload --host ${APP_HOST} --port ${APP_PORT}
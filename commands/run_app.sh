#!/bin/sh

. .venv/bin/activate && cd src && uvicorn main:app --reload --host ${HOST} --port ${PORT}
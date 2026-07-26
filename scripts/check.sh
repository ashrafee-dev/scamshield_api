#!/usr/bin/env bash

echo "Running tests..."
uv run pytest

echo "Running lint..."
uv run pylint app tests

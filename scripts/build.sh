#!/usr/bin/env bash
set -euo pipefail

VERSION=$(grep -m1 '^version = ' pyproject.toml | sed 's/version = "\([^"]*\)"/\1/')

docker build -t "pdf-extractext:${VERSION}" -t "pdf-extractext:latest" .

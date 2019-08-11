#!/bin/bash

set -xe

isort **/*.py
black **/*.py

#!/bin/bash
TARGET_ENV_NAME=$(condaac-cli --select)

if [ -z "$TARGET_ENV_NAME" ]; then
    echo "No environment is activated."
else
    conda activate $TARGET_ENV_NAME
    echo "Environment $TARGET_ENV_NAME is activated."
fi

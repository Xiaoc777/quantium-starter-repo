#!/usr/bin/env bash

echo "Starting test script..."

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    echo "Virtual environment not found."
    exit 1
fi

# Run the test suite
python -m pytest tests/test_app.py
TEST_EXIT_CODE=$?

# Return correct exit code
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Something went wrong."
    exit 1
fi
#!/bin/bash

# Run pytest with coverage
pytest app/tests/ --cov=app --cov-report=html

# Check the exit code
if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Some tests failed. Please check the test output above."
    exit 1
fi
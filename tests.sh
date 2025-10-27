#!/bin/bash

echo "=========================================="
echo "Running PigLang Tests"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

tests="./tests"

if [ ! -d "$tests" ]; then
  echo "Tests directory not found!"
  exit 1
fi

for test in "$tests"/*.py; do
  if [ -f "$test" ]; then
    test_name=$(basename "$test")
    echo -e "${YELLOW}Running $test_name...${NC}"
    echo "=========================================="
    python3 "$test"
    EXIT=$?
    echo ""
    if [ $EXIT -eq 0 ]; then
        echo -e "${GREEN}✓ $test_name PASSED${NC}"
    else
        echo -e "${RED}✗ $test_name FAILED${NC}"
    fi
    echo ""
  fi
done

echo "=========================================="
echo "All tests completed"
echo "=========================================="
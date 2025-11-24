#!/bin/bash

mkdir -p llm
mkdir -p obj
mkdir -p exe

echo "========================================"
echo "  Running OINK Example Programs"
echo "========================================"
echo ""

if [ ! -d "programs" ]; then
    echo "ERROR: programs directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

for program_file in programs/*.txt; do
    program=$(basename "$program_file" .txt)
    
    echo "----------------------------------------"
    echo "Running: $program"
    echo "----------------------------------------"
    
    echo "Compiling $program.txt..."
    python3 -m compiler.compiler "$program_file" ./llm/"$program".ll
    if [ $? -ne 0 ]; then
        echo "ERROR: $program should have compiled successfully!"
        exit 1
    fi
    
    echo "Generating object file..."
    llc -filetype=obj -relocation-model=pic ./llm/"$program".ll -o ./obj/"$program".o
    
    echo "Linking executable..."
    clang -fPIE ./obj/"$program".o -o ./exe/"$program"
    
    echo "Executing $program..."
    ./exe/"$program"
    
    echo ""
done

echo "========================================"
echo "  All programs executed successfully!"
echo "========================================"
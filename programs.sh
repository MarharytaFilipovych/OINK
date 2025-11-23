#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' 

mkdir -p programs
mkdir -p llm
mkdir -p obj
mkdir -p exe

for file in programs/*.txt; do
    base_name=$(basename "$file" .txt)
    
    echo -e "${CYAN}========================================${NC}"
    echo -e "${YELLOW}Processing: ${base_name}${NC}"
    echo -e "${CYAN}========================================${NC}"
    
    echo -e "${BLUE}[1/4] Compiling...${NC}"
    python3 -m compiler.compiler "./programs/$base_name.txt" "./llm/$base_name.ll"
    
    echo -e "${BLUE}[2/4] Assembling...${NC}"
    llc -filetype=obj -relocation-model=pic "./llm/$base_name.ll" -o "./obj/$base_name.o"
    
    echo -e "${BLUE}[3/4] Linking...${NC}"
    clang -fPIE "./obj/$base_name.o" -o "./exe/$base_name"
    
    echo -e "${BLUE}[4/4] Running:${NC}"
    ./exe/"$base_name"
    echo ""
done

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ All programs processed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
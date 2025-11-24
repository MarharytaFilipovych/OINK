#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Create directories
mkdir -p llm
mkdir -p obj
mkdir -p exe

echo -e "${CYAN}========================================${NC}"
echo -e "${MAGENTA}  🐷 Running OINK Example Programs 🐷${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Check if programs directory exists
if [ ! -d "programs" ]; then
    echo -e "${RED}❌ ERROR: programs directory not found!${NC}"
    echo -e "${YELLOW}Please run this script from the project root directory.${NC}"
    exit 1
fi

# Count total programs
total_programs=$(ls -1 programs/*.txt 2>/dev/null | wc -l)
current=0

# Loop through all programs
for program_file in programs/*.txt; do
    program=$(basename "$program_file" .txt)
    ((current++))
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${WHITE}Running: ${GREEN}$program${WHITE} [$current/$total_programs]${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Compilation
    echo -e "${YELLOW}🔨 Compiling $program.txt...${NC}"
    python3 -m compiler.compiler "$program_file" ./llm/"$program".ll 2>&1 | grep -v "DEBUG"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ ERROR: $program failed to compile!${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Compilation successful${NC}"
    
    # Object file generation
    echo -e "${YELLOW}⚙️  Generating object file...${NC}"
    llc -filetype=obj -relocation-model=pic ./llm/"$program".ll -o ./obj/"$program".o 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ ERROR: Failed to generate object file!${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Object file generated${NC}"
    
    # Linking
    echo -e "${YELLOW}🔗 Linking executable...${NC}"
    clang -fPIE ./obj/"$program".o -o ./exe/"$program" 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ ERROR: Failed to link executable!${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Executable created${NC}"
    
    # Execution
    echo -e "${CYAN}▶️  Executing $program...${NC}"
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    ./exe/"$program"
    exit_code=$?
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ Program executed successfully (exit code: $exit_code)${NC}"
    else
        echo -e "${YELLOW}⚠ Program exited with code: $exit_code${NC}"
    fi
    
    echo ""
done

echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}✨ All programs completed! ✨${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${WHITE}Summary:${NC}"
echo -e "  ${GREEN}✓${NC} Compiled: ${MAGENTA}$total_programs${NC} programs"
echo -e "  ${GREEN}✓${NC} Output: ${BLUE}llm/${NC}, ${BLUE}obj/${NC}, ${BLUE}exe/${NC} directories"
echo -e "${CYAN}========================================${NC}"
program="program"

# Ensure the output directories exist
mkdir -p llm
mkdir -p obj
mkdir -p exe

echo "Running $program.txt compilation..."

# 1. Compilation (Creates ./llm/program.ll)
python3 -m compiler.compiler ./"$program".txt ./llm/"$program".ll
if [ $? -ne 0 ]; then
    echo "ERROR: The program should have compiled successfully!"
    exit 1
fi

# 2. LLVM Object Generation (Reads from ./llm/program.ll and creates ./obj/program.o)
# FIX: Correctly points llc to the input file in the 'llm' directory
llc -filetype=obj -relocation-model=pic ./llm/"$program".ll -o ./obj/"$program".o

# 3. Final Executable (Reads from ./obj/program.o and creates ./exe/program)
# FIX: Correctly points clang to the object file in the 'obj' directory
clang -fPIE ./obj/"$program".o -o ./exe/"$program"

EXEC_CMD="./exe/"$program""

echo "Running executable: $EXEC_CMD"
eval $EXEC_CMD
echo ""
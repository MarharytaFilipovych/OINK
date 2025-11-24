program="program
echo "Running a program..."
python3 -m compiler.compiler ./"$program".txt ./llm/"$program".ll
if [ $? -ne 0 ]; then
    echo "ERROR: The program should have compiled successfully!"
    exit 1
fi
llc -filetype=obj -relocation-model=pic ./"$program".ll -o ./"$program".o
clang -fPIE ./"$program".o -o ./"$program"

EXEC_CMD="./"$program""


eval $EXEC_CMD
echo ""
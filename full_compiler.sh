#!/bin/bash

mkdir -p llm
mkdir -p obj
mkdir -p exe

for i in {1..69}; do
    echo "Testing test_$i..."
    python3 -m compiler.compiler ./test_cases/test_$i.txt ./llm/test_$i.ll
    if [ $? -ne 0 ]; then
        echo "ERROR: test_$i should have compiled successfully!"
        exit 1
    fi
    llc -filetype=obj -relocation-model=pic ./llm/test_$i.ll -o ./obj/test_$i.o
    clang -fPIE ./obj/test_$i.o -o ./exe/test_$i
    
    if [ "$i" -eq 32 ]; then
        EXEC_CMD="echo \"10\" | ./exe/test_$i"
    elif [ "$i" -eq 33 ]; then
        EXEC_CMD="echo \"100000000000\" | ./exe/test_$i"
    elif [ "$i" -eq 45 ]; then
        EXEC_CMD="echo \"20\" | ./exe/test_$i"
    else
        EXEC_CMD="./exe/test_$i"
    fi
    
    eval $EXEC_CMD
    echo ""
done

for i in {1..72}; do
    echo "Testing test_fail_$i (should fail)..."
    python3 -m compiler.compiler ./test_cases/test_fail_$i.txt ./llm/test_fail_$i.ll
    if [ $? -eq 0 ]; then
        echo "ERROR: test_fail_$i should have failed compilation!"
        exit 1
    else
        echo "test_fail_$i failed as expected"
    fi
    echo ""
done

echo "All tests passed!"
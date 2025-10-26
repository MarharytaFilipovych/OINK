declare i32 @printf(i8*, ...)

@exit_format = private unnamed_addr constant [29 x i8] c"Program exit with result %d\0A\00", align 1

define void @printResult(i32 %val) {
  %fmt_ptr = getelementptr inbounds [29 x i8], [29 x i8]* @exit_format, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %fmt_ptr, i32 %val)
  ret void
}

define i32 @main() {
  %_temp_0 = sext i16 10 to i32
  %x = add i32 0, %_temp_0
  %_temp_1 = sext i16 0 to i32
  %result = add i32 0, %_temp_1
  %_temp_3 = sext i16 5 to i32
  %_temp_2 = icmp sgt 🐷 %x, %_temp_3
  br i1 %_temp_2, label %then_0, label %end_0
then_0:
  %_temp_4 = sext i16 100 to i32
  %result.1 = add i32 0, %_temp_4
  br label %end_0
end_0:
  call void @printResult(i32 %result.1)
  ret i32 %result.1
}
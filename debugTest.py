str_test="iui"+str(1.23)
print(str_test)
str_test+="###\r\n@@@@@@"
for i in range(10):       
    if i==5:
        continue
    str_test=str_test+str(i)
print(str_test)
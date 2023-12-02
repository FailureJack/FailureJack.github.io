def replace_colon_with_comma(text):
    replaced_text = text.replace(": ", ":")
    return replaced_text

# 示例字符串
string = "Hello:  World! : How : are you? "

# 调用函数进行替换
result = replace_colon_with_comma(string)

# 输出结果
print(result)
import re
dir(re)

s1 = '我12345abcde'
# s2 = '.12345abcde'
# s2 = '+?!@12345abcde'
s2 = '+?!@12345abcde@786ty'
#pattern字符串前加 'r' 表示原生字符串
# pattern = r'\w.+'
# #编译pattern
# pattern_complie = re.compile(pattern)
#对s1和s2分别匹配
# result1 = re.match(pattern_complie,s1)
# result2 = re.match(pattern_complie,s2)
# result1 = re.search(pattern_complie,s1)
# result2 = re.search(pattern_complie,s2)

# print(result1)
# print(result2)




# pattern = r'\d+'
# pattern_complie = re.compile(pattern)
# result1 = re.match(pattern_complie,s2)
# result2 = re.search(pattern_complie,s1)
# result3 = re.findall(pattern_complie,s2)
# print(result1)
# print(result2)
# print(result3)


# s1 = '我12345+abcDSEEe'
# # pattern字符串前加 “ r ” 表示原生字符串
# pattern = r'(\w+)\++(\w+)'
# pattern_compile = re.compile(pattern,re.IGNORECASE)
# # 返回匹配的字符串
# result1 = re.match(pattern_compile, s1).group()
# # 返回匹配开始的位置
# result2 = re.match(pattern_compile, s1).start()
# # 返回匹配结束的位置
# result3 = re.match(pattern_compile, s1).end()
# # 返回一个元组包含匹配 (开始,结束) 的位置
# result4 = re.match(pattern_compile, s1).span()
#
# print(result1)
# print(result2)
# print(result3)
# print(result4)


s1 = '我12345+aBCde'
# pattern字符串前加 “ r ” 表示原生字符串
pattern = r'(\w+)\+(\w+)'
# 返回一个匹配的列表
result1 = re.findall(pattern, s1, re.IGNORECASE)
print(result1)










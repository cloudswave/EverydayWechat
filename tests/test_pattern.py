import re
rubbish_complie = r'^\s*(.*?)(?:3|垃圾|rubbish|是什么垃圾)(?!\d)'
rubbish_clear_compile = r'1|垃圾|rubbish|是什么垃圾|\s'
htext = '猫娘是什么垃圾'
print(re.findall(rubbish_complie, htext, re.I))
if re.findall(rubbish_complie, htext, re.I):
    key = re.sub(rubbish_clear_compile, '', htext, flags=re.IGNORECASE).strip()
    print(key)
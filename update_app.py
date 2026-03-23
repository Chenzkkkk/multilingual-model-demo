import re

with open('frontend/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'\s*"测试页": "pages/stage\d+_test\.py",\n', '\n', text)
text = re.sub(r'c1, c2, _ = st\.columns\(\[1, 1, 2\]\)', 'c1, _ = st.columns([1, 2])', text)
text = re.sub(r'if st\.button\(f"进入\{stage_name\}讲解", key=f"guide_\{idx\}", use_container_width=True\):', 'if st.button(f"进入{stage_name}", key=f"guide_{idx}", use_container_width=True):', text)
text = re.sub(r'    with c2:\s*if st\.button\(f"进入\{stage_name\}测试", key=f"test_\{idx\}", use_container_width=True\):\s*st\.switch_page\(info\["测试页"\]\)', '', text)

with open('frontend/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("done")

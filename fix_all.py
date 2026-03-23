import os, re

def update_ui_components():
    with open("frontend/ui_components.py", "r", encoding="utf-8") as f:
        text = f.read()

    # CSS inject
    css_inject = """html, body, [class*="css"] {
    font-family: "Noto Sans SC", "Microsoft YaHei", "PingFang SC", sans-serif;
    color: var(--text);
}
/* 增大侧边栏字体并使得整体更 modern / 大 */
[data-testid="stSidebarNav"] span, .css-1d391kg {
    font-size: 18px !important;
}"""
    text = text.replace("""html, body, [class*="css"] {
    font-family: "Noto Sans SC", "Microsoft YaHei", "PingFang SC", sans-serif;
    color: var(--text);
}""", css_inject)

    # Rewrite render_model_result
    new_func = """def render_model_result(result: dict[str, Any]) -> None:
    model_name = str(result.get("model", "Unknown Model"))
    success = bool(result.get("success", False))
    payload = result.get("result")
    
    user_input = result.get("user_input") or result.get("input") or result.get("text")
    if isinstance(payload, dict):
        base_input = payload.get("user_input") or payload.get("input") or payload.get("text")
        if base_input and not user_input:
            user_input = base_input

    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    status = "成功" if success else "失败"
    st.markdown(f"<div class='result-title'>{html.escape(model_name)} | 运行{status}</div>", unsafe_allow_html=True)

    if user_input:
        st.markdown("<div class='result-kv'>输入</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-input'>{html.escape(str(user_input))}</div>", unsafe_allow_html=True)

    if success:
        if isinstance(payload, dict):
            output_val = payload.get("output") or payload.get("result") or payload.get("prediction") or payload.get("摘要")
            if output_val and not (isinstance(output_val, list) and len(output_val)>0 and isinstance(output_val[0], dict)):
                st.markdown("<div class='result-kv'>输出</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-output'>{html.escape(str(output_val))}</div>", unsafe_allow_html=True)
            elif payload.get("predictions") and isinstance(payload.get("predictions"), list):
                st.markdown("<div class='result-kv'>预测结果 / 最相近词汇</div>", unsafe_allow_html=True)
                for idx, item in enumerate(payload.get("predictions", [])[:5], start=1):
                    token = item.get("token") or item.get("label") or ""
                    score = item.get("score", "N/A")
                    st.write(f"{idx}. {token} (score={score})")
            else:
                filtered = {k: v for k, v in payload.items() if k not in ["model_info", "architecture", "cache_dir", "task", "advantage_over_word2vec", "provider", "model_id", "user_input", "input", "text", "usage"]}
                if filtered:
                    st.markdown("<div class='result-kv'>其他输出</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-output'>{html.escape(str(filtered))}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-kv'>输出</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-output'>{html.escape(str(payload))}</div>", unsafe_allow_html=True)
    else:
        err = payload if isinstance(payload, str) else str(payload)
        st.markdown("<div class='result-kv'>错误信息</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-error'>{html.escape(err)}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)"""

    text = re.sub(r"def render_model_result\(result: dict\[str, Any\]\) -> None:.*?st\.markdown\(\"</div>\", unsafe_allow_html=True\)", new_func, text, flags=re.DOTALL)

    with open("frontend/ui_components.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("ui_components.py updated")

def update_stages():
    import glob
    for i in range(1, 5):
        stage_file = f"frontend/pages/stage{i}.py"
        test_file = f"frontend/pages/stage{i}_test.py"
        if not os.path.exists(stage_file) or not os.path.exists(test_file):
            continue
        with open(stage_file, "r", encoding="utf-8") as f:
            stage_content = f.read()
        with open(test_file, "r", encoding="utf-8") as f:
            test_content = f.read()
            
        # Combine: Remove the duplicate imports and run headers if any, but since we are quick, 
        # let's just append test_content, but removing its `st.set_page_config` and `render_page_header`
        # and imports. Or just strip out duplicate page configs.
        stage_content = re.sub(r"st\.set_page_config\([^)]+\)", "", stage_content, count=0)
        test_content = re.sub(r"st\.set_page_config\([^)]+\)", "", test_content, count=0)
        
        # In both, `render_page_header` might be called twice. We keep the one from test or something, let's keep one.
        # It's cleaner to just join them and let streamlit render both. The instructions say "For each, put the markdown explanation at the top, and the test UI at the bottom of the SAME file."
        combined = stage_content + "\n\n" + "st.markdown('---')\n" + "st.title('测试平台')\n" + test_content
        
        # fix: ensure 'import sys' at top is not broken.
        with open(stage_file, "w", encoding="utf-8") as f:
            f.write(combined)
        print(f"combined {stage_file}")
        os.remove(test_file)
        print(f"deleted {test_file}")

if __name__ == "__main__":
    update_ui_components()
    update_stages()

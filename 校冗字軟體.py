
import streamlit as st
import re
from collections import Counter

# ── Google Analytics（GA4）追蹤碼 ──────────────────────
# 啟動時把 GA 程式碼寫進 Streamlit 的 index.html，只會寫入一次
import pathlib

GA_SCRIPT = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LB73SCWDRQ"></script>
<script id="google_analytics">
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-LB73SCWDRQ');
</script>
"""

def inject_ga():
    try:
        index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
        html = index_path.read_text(encoding="utf-8")
        if 'id="google_analytics"' not in html:
            html = html.replace("<head>", "<head>" + GA_SCRIPT, 1)
            index_path.write_text(html, encoding="utf-8")
    except Exception:
        pass  # 就算失敗也不影響 app 運作

inject_ga()
# ─────────────────────────────────────────────────────

# 定義常見虛詞列表
COMMON_PARTICLES = ["的", "了", "而", "就", "是", "在", "和", "也", "不", "有", "著", "那", "要", "對", "這", "個", "嗎", "吧", "呢", "還", "就算", "所以", "但是"]

# 定義檢測冗字的函數
def detect_redundant_words(text, threshold=3):
    """
    檢測文本中的冗字（高頻虛詞）。
    :param text: 輸入的文本
    :param threshold: 判定為冗字的重複次數閾值
    :return: 標記冗字的文本和統計報告
    """
    paragraphs = text.split("\n")
    marked_paragraphs = []
    word_counter = Counter()

    for paragraph in paragraphs:
        if paragraph.strip():
            # 統計虛詞頻率
            words = list(paragraph)
            particle_counts = Counter([word for word in words if word in COMMON_PARTICLES])
            word_counter.update(particle_counts)

            # 標記冗字
            for word, count in particle_counts.items():
                if count > threshold:
                    paragraph = re.sub(f"({re.escape(word)})", r"<span style='color:red; font-weight:bold;'>\1</span>", paragraph)
            marked_paragraphs.append(paragraph)

    # 返回標記文本和統計報告
    marked_text = "<br><br>".join(marked_paragraphs)  # 使用 HTML 保留段落結構
    return marked_text, word_counter

# 初始化 session state
if "highlight_word" not in st.session_state:
    st.session_state["highlight_word"] = None

# Streamlit 應用程式
st.title("中文冗字檢測工具")
st.write("輸入中文文本，檢測是否存在高頻重複的虛詞（如 '的'、'了' 等）。")

# 用戶輸入
user_input = st.text_area("請輸入文本。", height=200)

# 閾值輸入
threshold = st.slider("設置冗字的重複次數閾值：", min_value=2, max_value=10, value=3)

# 初始化空的 word_counter
word_counter = Counter()

# 檢測冗字
if st.button("檢測"):
    if user_input.strip():
        marked_text, word_counter = detect_redundant_words(user_input, threshold)

        # 顯示檢測結果
        st.markdown("### 檢測結果：")
        st.markdown(marked_text, unsafe_allow_html=True)

        # 顯示統計報告
st.sidebar.markdown("### 統計報告")
st.sidebar.markdown("**高頻虛詞使用情況：**")
for word, count in word_counter.most_common(10):
    st.sidebar.markdown(f"- **{word}**: {count} 次")

# 高亮顯示用戶選擇的詞
if st.session_state["highlight_word"]:
    highlight_word = st.session_state["highlight_word"]
    highlighted_paragraphs = [
        re.sub(
            f"({re.escape(highlight_word)})", 
            r"<span style='background-color: yellow;'>\1</span>", 
            paragraph
        )
        for paragraph in user_input.split("\n")
    ]
    highlighted_text = "<br>".join(highlighted_paragraphs)  # 使用 <br> 保留段落
    st.markdown("### 高亮顯示：")
    st.markdown(highlighted_text, unsafe_allow_html=True)

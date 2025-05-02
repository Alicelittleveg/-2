import streamlit as st
import re
from collections import Counter

# 定義常見虛詞列表
COMMON_PARTICLES = ["的", "了", "而", "就", "是", "在", "和", "也", "不", "有", "著", "那", "要", "對", "這", "個", "嗎", "吧", "呢", "還", "就算", "所以", "但是"]

def detect_redundant_words(text, threshold=3):
    """
    檢測文本中的冗字（高頻虛詞）。
    :param text: 用戶輸入的文本
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
                    # 使用非貪婪模式替換，避免多次替換問題
                    paragraph = re.sub(f"({re.escape(word)})", r"<span style='color:red; font-weight:bold;'>\1</span>", paragraph)
            marked_paragraphs.append(paragraph)

    marked_text = "<br><br>".join(marked_paragraphs)  # 保留段落結構，使用 HTML 換行
    return marked_text, word_counter


# 初始化 Streamlit 應用
st.title("中文冗字檢測工具")
st.write("輸入中文文本，檢測是否存在高頻重複的虛詞，高亮顯示超出閾值的詞語。")

# 用戶輸入
user_input = st.text_area("請輸入中文文本：", height=200)

# 冗字閾值
threshold = st.slider("設置冗字的重複次數閾值：", min_value=2, max_value=10, value=3)

# 檢測按鈕
if st.button("檢測"):
    if user_input.strip():
        marked_text, word_counter = detect_redundant_words(user_input, threshold)

        # 顯示檢測結果
        st.subheader("檢測結果")
        st.markdown(marked_text, unsafe_allow_html=True)

        # 顯示統計報告
        st.sidebar.subheader("統計報告")
        st.sidebar.write("高頻虛詞使用情況：")
        for word, count in word_counter.most_common():
            st.sidebar.write(f"{word}: {count} 次")
    else:
        st.error("請輸入有效的文本！")

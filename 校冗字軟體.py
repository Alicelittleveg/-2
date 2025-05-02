from collections import Counter

# 定義常見虛詞列表
common_particles = ["的", "了", "而", "就", "是", "在", "和", "也", "不", "有", "著", "那", "要", "對", "這", "個", "嗎", "吧", "呢", "還", "就算", "所以", "但是"]

# 定義檢測冗字的函數
def detect_redundant_words(text, threshold=3):
"""
   檢測文本中的冗字（高頻虛詞）。
    :param text: 輸入的文本
    :param text: 用戶輸入的文本
   :param threshold: 判定為冗字的重複次數閾值
   :return: 標記冗字的文本和統計報告
   """
    # 分段處理
paragraphs = text.split("\n")
marked_paragraphs = []
word_counter = Counter()
@@ -22,62 +20,42 @@ def detect_redundant_words(text, threshold=3):
if paragraph.strip():
# 統計虛詞頻率
words = list(paragraph)
            particle_counts = Counter([word for word in words if word in common_particles])
            particle_counts = Counter([word for word in words if word in COMMON_PARTICLES])
word_counter.update(particle_counts)

# 標記冗字
for word, count in particle_counts.items():
if count > threshold:
                    paragraph = paragraph.replace(word, f"**{word}**")  # 高亮冗字
                    paragraph = re.sub(f"({word})", r"**\1**", paragraph)
marked_paragraphs.append(paragraph)

    # 返回標記文本和統計報告
    marked_text = "\n\n".join(marked_paragraphs)  # 使用雙換行符保留段落結構
    marked_text = "\n\n".join(marked_paragraphs)  # 保留段落結構
return marked_text, word_counter

# 初始化 session state
if "highlight_word" not in st.session_state:
    st.session_state["highlight_word"] = None

# Streamlit 應用程式
# 初始化 Streamlit 應用
st.title("中文冗字檢測工具")
st.write("輸入中文文本，檢測是否存在高頻重複的虛詞（如 '的'、'了' 等）。")
st.write("輸入中文文本，檢測是否存在高頻重複的虛詞，高亮顯示超出閾值的詞語。")

# 用戶輸入
user_input = st.text_area("請輸入文本。", height=200)
user_input = st.text_area("請輸入中文文本：", height=200)

# 閾值輸入
# 冗字閾值
threshold = st.slider("設置冗字的重複次數閾值：", min_value=2, max_value=10, value=3)

# 檢測冗字
# 檢測按鈕
if st.button("檢測"):
if user_input.strip():
marked_text, word_counter = detect_redundant_words(user_input, threshold)

# 顯示檢測結果
        st.markdown("### 檢測結果：")
        st.markdown(marked_text.replace("\n", "<br>"), unsafe_allow_html=True)  # 使用 <br> 保留換行符
        st.subheader("檢測結果")
        st.markdown(marked_text.replace("\n", "<br>"), unsafe_allow_html=True)

# 顯示統計報告
        st.sidebar.markdown("### 統計報告")
        st.sidebar.markdown("**高頻虛詞使用情況：**")
        for word, count in word_counter.most_common(5):
            if st.sidebar.button(f"高亮顯示：{word}"):
                st.session_state["highlight_word"] = word
        st.sidebar.subheader("統計報告")
        st.sidebar.write("高頻虛詞使用情況：")
        for word, count in word_counter.most_common():
            st.sidebar.write(f"{word}: {count} 次")
else:
        st.warning("請輸入文本！")

# 高亮顯示用戶選擇的詞
if st.session_state["highlight_word"]:
    highlight_word = st.session_state["highlight_word"]
    highlighted_paragraphs = [
        re.sub(
            f"({highlight_word})", 
            r"<span style='background-color: yellow;'>\1</span>", 
            paragraph
        )
        for paragraph in user_input.split("\n")
    ]
    highlighted_text = "<br>".join(highlighted_paragraphs)  # 使用 <br> 保留段落
    st.markdown("### 高亮顯示：")
    st.markdown(highlighted_text, unsafe_allow_html=True)
        st.error("請輸入有效的文本！")

import pickle
import pandas as pd
# Load the ai_news.pkl file
with open('ai_news.pkl', 'rb') as file:
    ai_news = pickle.load(file)

# Print or inspect the loaded data
print(ai_news)


import jieba

import pickle
import pandas as pd
import jieba

# Optional: 加載自定義詞典（如果有需要）
# jieba.load_userdict('custom_dict.txt')

# Define a function to tokenize text using jieba
def jieba_cut_to_list(text):
    return list(jieba.cut(text))  # 返回斷詞結果作為列表

# Load the ai_news.pkl file
with open('ai_news.pkl', 'rb') as file:
    ai_news = pickle.load(file)

# Assuming ai_news is a DataFrame and has a 'sentence' column
if isinstance(ai_news, pd.DataFrame) and 'sentence' in ai_news.columns:
    # 新增一個欄位存放 tokens 列表
    ai_news['tokens'] = ai_news['sentence'].apply(jieba_cut_to_list)

# Print the 'tokens' column
if 'tokens' in ai_news.columns:
    print(ai_news['tokens'])
else:
    print("The 'tokens' column does not exist.")


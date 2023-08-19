import streamlit as st
import json
from datetime import datetime
import pytz
import urllib.parse
import time

# 禁止ワードのリスト
banned_words = ["馬鹿", "禁止ワード2", "禁止ワード3"]

# ユーザーの投稿内容をチェックする関数
def check_post_content(title, content):
    for banned_word in banned_words:
        if banned_word in title:
            title = title.replace(banned_word, "＠" * len(banned_word))
        if banned_word in content:
            content = content.replace(banned_word, "＠" * len(banned_word))
    return title, content

def save_post(title, content):
    now = datetime.now(pytz.timezone("Asia/Tokyo"))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    post = {"title": title, "content": content, "timestamp": now_str}
    with open('posts.json', 'a') as file:
        file.write(json.dumps(post))
        file.write('\n')

def load_posts():
    with open('posts.json', 'r') as file:
        lines = file.readlines()
        posts = [json.loads(line.strip()) for line in lines]
        
        for post in posts:
            timestamp = datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S")
            timestamp = pytz.timezone("Asia/Tokyo").localize(timestamp)
            post['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return posts

# JSONファイルの整合性を確認する関数
def validate_json_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        validated_posts = []
        for line in lines:
            try:
                post = json.loads(line)
                if 'title' in post and 'content' in post and 'timestamp' in post:
                    validated_posts.append(post)
                else:
                    st.warning("不正な形式の投稿が見つかりました。修正されます。")
            except json.JSONDecodeError:
                st.warning("不正なJSON形式が見つかりました。修正されます。")
        with open(filename, 'w') as file:
            for post in validated_posts:
                file.write(json.dumps(post))
                file.write('\n')
        st.success("JSONファイルの整合性が確認され、修正されました。")

def main():
    st.title("掲示板アプリ")

    # 新規投稿の入力
    new_post_content = st.text_area("管理者以外記述厳禁", height=100)
    new_post_title = st.text_input("ページ")
    
    # 投稿ボタンが押された場合
    if st.button("投稿する") and new_post_title and new_post_content:
        new_post_title, new_post_content = check_post_content(new_post_title, new_post_content)
        if "＠" in new_post_title or "＠" in new_post_content:
            st.warning("禁止ワードが含まれています！")
        save_post(new_post_title, new_post_content)
        st.success("投稿が保存されました！")

    # 保存された投稿の表示
    posts = load_posts()
    st.subheader("保存された投稿")

    if not posts:
        st.info("まだ投稿がありません。")
    else:
        for post in posts:
            post_url = f"<a href='https://maichan-bord-{urllib.parse.quote(post['title'])}.streamlit.app'>{post['title']}</a>"
            st.subheader(post['content'])
            st.write(post['timestamp'])  # タイムスタンプを表示
            st.markdown(post_url, unsafe_allow_html=True)
            st.markdown("---")

    # JSONファイルの整合性を確認
    validate_json_file('posts.json')

if __name__ == "__main__":
    main()

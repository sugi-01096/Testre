import streamlit as st
import json
from datetime import datetime
import pytz
import urllib.parse

# 禁止ワードのリスト
banned_words = ["馬鹿", "禁止ワード2", "禁止ワード3"]

# ユーザーの投稿内容をチェックする関数
def check_post_content(title, content):
    # タイトルと投稿内容の禁止ワードの検出
    for banned_word in banned_words:
        if banned_word in title:
            title = title.replace(banned_word, "＠" * len(banned_word))
        if banned_word in content:
            content = content.replace(banned_word, "＠" * len(banned_word))
    return title, content

def save_post(title, content):
    now = datetime.now(pytz.timezone("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    post = {"title": title, "content": content, "timestamp": now}
    with open('posts.json', 'a') as file:
        file.write(json.dumps(post))
        file.write('\n')

def load_posts():
    with open('posts.json', 'r') as file:
        lines = file.readlines()
        return [json.loads(line) for line in lines]

def main():
    st.title("掲示板アプリ")

    # 新規投稿の入力
    
    new_post_content = st.text_area("新規投稿", height=100)
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
            # 各タイトルにリンクを付けて表示
            post_url = f"<a href='https://wikiwiki.jp/{urllib.parse.quote(post['title'])}'>{post['title']}</a>"
            st.write(post['content'])
            st.markdown(post_url, unsafe_allow_html=True)
            st.markdown("---")

if __name__ == "__main__":
    main()

import streamlit as st
import json

# 禁止ワードのリスト
banned_words = ["馬鹿", "禁止ワード2", "禁止ワード3"]

# ユーザーの投稿内容をチェックする関数
def check_post_content(post_content):
    # 禁止ワードの検出
    for banned_word in banned_words:
        if banned_word in post_content:
            # 禁止ワードを＠に置き換える
            post_content = post_content.replace(banned_word, "＠" * len(banned_word))
            return post_content, True  # 禁止ワードが検出された場合は置き換えた投稿内容とTrueを返す
    return post_content, False  # 禁止ワードが検出されなかった場合は投稿内容とFalseを返す

def save_post(title, content):
    post = {"title": title, "content": content}
    with open('posts.json', 'a') as file:
        json.dump(post, file)
        file.write('\n')

def load_posts():
    with open('posts.json', 'r') as file:
        return [json.loads(line) for line in file]

def main():
    st.title("掲示板アプリ")

    # 新規投稿の入力
    new_post_title = st.text_input("タイトル")
    new_post_content = st.text_area("新規投稿", height=100)

    # 投稿ボタンが押された場合
    if st.button("投稿する") and new_post_title and new_post_content:
        new_post_content, banned = check_post_content(new_post_content)
        if banned:
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
            st.text(post["title"])
            st.text(post["content"])
            st.markdown("---")

if __name__ == "__main__":
    main()


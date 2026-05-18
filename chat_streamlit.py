import contextlib
import io
import streamlit as st
# import src.tools as tools  # noqa: F401
from src.agent.ReactAgent import ReactAgent


st.set_page_config(page_title="Tomori Chat", page_icon="🎐", layout="centered")
st.title("Tomori 对话前端（Streamlit）")

if "agent" not in st.session_state:
    st.session_state.agent = ReactAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("清空会话"):
    st.session_state.agent = ReactAgent()
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("请输入你的问题")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Tomori 思考中..."):
            run_logs = io.StringIO()
            with contextlib.redirect_stdout(run_logs):
                answer = st.session_state.agent.run(user_input) or "（无返回内容）"
        st.markdown(answer)
        logs_text = run_logs.getvalue().strip()
        if logs_text:
            with st.expander("运行日志"):
                st.code(logs_text)

    st.session_state.messages.append({"role": "assistant", "content": answer})

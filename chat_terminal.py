import contextlib
import io
import tools  # noqa: F401
from src.agent.ReactAgent import ReactAgent


def main() -> None:
    print("Tomori 终端对话已启动，输入 exit / quit / 退出 可结束。")
    agent = ReactAgent()

    while True:
        try:
            user_input = input("\n你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTomori: 已退出对话。")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "q", "退出"}:
            print("Tomori: 已退出对话。")
            break

        run_logs = io.StringIO()
        with contextlib.redirect_stdout(run_logs):
            answer = agent.run(user_input)
        print(f"Tomori: {answer or '（无返回内容）'}")


if __name__ == "__main__":
    main()

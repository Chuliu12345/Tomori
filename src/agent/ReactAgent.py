from .LLMModel import LLMModel
from tools.tool import ToolRegistry
class ReactAgent:
    def __init__(self, max_step:int = 5):
        self.client = LLMModel()
        self.max_step = max_step
        self.system_message = self._load_system_message()
        self.tool_desc = ToolRegistry().get_tools_descriptor()
        self.all_token = 0
        self.chat_message = [{"role": "system", "content": self.system_message}]
        # print(self.tool_desc)
    def run(self, user_question: str) -> str:
        self.chat_message.append({"role": "user", "content": user_question})
        for i in range(0, self.max_step):
            response = self.client.think(messages=self.chat_message, tools = self.tool_desc)
            # TODO 可以考虑连续调用一系列tools
            # 统计每次迭代的token消耗
            input_token = response.usage.prompt_tokens
            output_token = response.usage.completion_tokens
            print(f"input_token: {input_token}")
            print(f"output_token: {output_token}")
            self.all_token += input_token + output_token
            try:
                choice = response.choices[0]
                print(choice.finish_reason)
                if choice.finish_reason == "stop":
                    print("Agent has completed the task.")
                    final_answer = choice.message.content or ""
                    print(final_answer)
                    self.chat_message.append({"role": "assistant", "content": final_answer})
                    # 结束
                    return final_answer
                elif choice.finish_reason == "tool_calls":
                    print(f"调用工具：{choice.message.content}")

                    # LLM 调用了工具，构建 assistant 消息
                    assistant_msg = {
                        "role": "assistant",
                        "content": choice.message.content or ""
                    }
                    # 添加 tool_calls 信息
                    if choice.message.tool_calls:
                        assistant_msg["tool_calls"] = [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in choice.message.tool_calls
                        ]
                    self.chat_message.append(assistant_msg)
                    
                    # 执行工具调用
                    tool_calls = choice.message.tool_calls
                    print(len(tool_calls))
                    print(tool_calls)
                    for tool_call in tool_calls:
                        # 收集tool调用信息
                        tool_name = tool_call.function.name
                        tool_args = tool_call.function.arguments
                        # 执行tool并获取结果
                        tool_result = ToolRegistry().execute_tool(tool_name, tool_args)  
                        self.chat_message.append(
                            {
                                "role": "tool",
                                "content": tool_result,
                                "tool_call_id": tool_call.id,
                                "name": tool_name
                            }
                        )
                        print(tool_call)
            except Exception as e:
                error_msg = f"Error processing LLM response: {e}"
                print(f"Error processing LLM response: {e}")
                return error_msg
        # 如果没有在max_step内完成任务，需要强制输出最终结果
        user_msg = {"role": "user", "content": "请基于之前的工具调用结果，给出最终的回答。"}
        self.chat_message.append(user_msg)
        final_response = self.client.think(messages=self.chat_message, tools = self.tool_desc)
        final_answer = final_response.choices[0].message.content or ""
        self.chat_message.append({"role": "assistant", "content": final_answer})
        return final_answer


    
    def _load_system_message(self):
        system_message = """
            你是tomori，是一个能够利用tools，与用户对话，解答二次元相关问题的ACG智能体。
            一些可能的工作流[注意：你可以在一次迭代中同时调用多个tool]：
            1.番剧评价：获取番剧id -> [获取番剧评价和番剧信息(返回所有相关tool及对应参数)] -> 内容整合并返回给用户
            2.新番预测：根据番剧tag和对番剧吐槽，结合制作人员信息(可以参考对制作人员的吐槽)，预测番剧质量
            建议流程如下：
            step1: 获取番剧的subject_id
            step2: 利用subject_id获取subject_info，其中包含staff_id 和 subject_comment信息
            step3: 根据staff_id获取person_comment
            """
        return system_message
if __name__ == "__main__":
    agent = ReactAgent()
    print(agent.run("帮我预测新番上伊那牡丹的质量"))



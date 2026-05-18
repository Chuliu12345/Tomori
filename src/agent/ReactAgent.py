try:
    from .LLMModel import LLMModel
    from ..tools.tool import ToolRegistry
except ImportError:
    from LLMModel import LLMModel
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
            
            [Tool调用的**强制性**参数策略]
            ⚠️ 【CRITICAL】必须遵守以下规则，违反会导致任务失败：
            1. 仅传入*必需*参数（required=true）。非必需参数（required=false）默认**不传入**。
            2. 对于search_subjects：只传入"subject"，不传"limit"和"offset"（除非显式需要更多结果）
            3. 对于其他可选参数：只有当明确需要时才传入（例：确实需要更大范围搜索时）
            
            [何时例外地传入可选参数]
            - 仅当上一次调用的结果不足以回答用户问题时
            - 存在大量重复信息(如续集、同名作品)导致真实样本量远小于真实需求时
            - 仅当你需要显式扩大搜索范围时
            - 例：如果search_subjects返回结果包含大量续集，你可以修改offset参数，并考虑传入limit参数以获取更多结果
            
            [参考工作流]
            下面提供一下可能会使用到的工作流，当然，存在其他的工作场景，需要自行决定工作流
            【tip】你可以考虑同时返回多个tool调用，只要这些tool之间互相没有参数依赖关系
            1.番剧评价：search_subjects(仅传subject) -> get_subject_info -> 整合返回
            2.新番预测：search_subjects(仅传subject) -> get_subject_info & get_person_comments(&表示可以在一次迭代中同时调用多个tool,因为这些tool之间没有参数依赖关系) -> 分析预测，具体步骤如下：
            step1: 获取番剧的subject_id（search_subjects仅用subject参数）
            step2: 利用subject_id获取subject_info（包含staff_id和subject_comment）
            step3: 根据staff_id获取person_comment进行分析
            """
        return system_message
if __name__ == "__main__":
    agent = ReactAgent()
    # print(agent.run("帮我预测新番上伊那牡丹的质量"))
    print(agent.run("帮我预测新番想结束这场“我爱你”的游戏的质量"))



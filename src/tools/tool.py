from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any, Dict, List, Callable, Optional
import json
import inspect
class ToolParameter(BaseModel):
    """工具参数定义"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
class Tool(ABC):
    """工具基类"""

    def __init__(self, func, name: str, description: str):
        self.func = func
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, args: Dict) -> str:
        """执行工具"""
        pass

    @abstractmethod
    def get_parameters(self) -> List[ToolParameter]:
        """获取工具参数定义"""
        pass


class FunctionTool(Tool):
    """函数型工具 - 用于包装函数为Tool对象"""

    def run(self, args: Dict) -> str:
        """执行工具"""
        try:
            result = self.func(**args)
            return str(result)
        except Exception as e:
            return f"错误：{str(e)}"

    def get_parameters(self) -> List[ToolParameter]:
        """从函数签名提取参数定义"""
        parameters = []
        sig = inspect.signature(self.func)

        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue

            param_type = self._get_parameter_type(param.annotation)
            is_required = param.default == inspect.Parameter.empty

            param_info = ToolParameter(
                name=param_name,
                type=param_type,
                description=f"参数: {param_name}",
                required=is_required
            )

            if param.default != inspect.Parameter.empty:
                param_info.default = param.default

            parameters.append(param_info)

        return parameters

    def _get_parameter_type(self, annotation) -> str:
        """根据类型注解转换为OpenAI API支持的类型"""
        if annotation == inspect.Parameter.empty:
            return "string"

        type_str = str(annotation).lower()

        type_mapping = {
            "int": "integer",
            "float": "number",
            "bool": "boolean",
            "str": "string",
            "list": "array",
            "dict": "object",
        }

        for key, value in type_mapping.items():
            if key in type_str:
                return value

        return "string"


# 语法糖：支持 @tool 和 @tool() 两种使用方式
def tool(name: Optional[str] = None, description: Optional[str] = None):
    def wrap(func: Callable) -> FunctionTool:  # 使用FunctionTool包装函数
        # func -> FunctionTool
        tool_name = name or func.__name__
        tool_desc = description or func.__doc__ or "工具"
        tool_obj = FunctionTool(func, name=tool_name, description=tool_desc)
        ToolRegistry().register_tool(tool_obj)
        return tool_obj
    
    # 支持两种用法：@tool 和 @tool() 或 @tool(name="xxx")
    # 如果 name 是可调用对象（函数），说明用的是 @tool 不带括号
    if callable(name) and description is None:
        # @tool 的情况，name 实际是被装饰的函数
        func = name
        tool_name = func.__name__
        tool_desc = func.__doc__ or "工具"
        tool_obj = FunctionTool(func, name=tool_name, description=tool_desc)
        ToolRegistry().register_tool(tool_obj)
        return tool_obj
    
    # @tool() 或 @tool(name="xxx") 的情况
    return wrap
class ToolRegistry:
    """
    HelloAgents工具注册表

    提供工具的注册、管理和执行功能。
    单例模式
    支持两种工具注册方式：
    1. Tool对象注册（推荐）
    2. 函数直接注册（简便）
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 只在第一次初始化时创建字典
        if not hasattr(self, '_tools'):
            self._tools: dict[str, Tool] = {}
            self._functions: dict[str, dict[str, Any]] = {}# [name[discription, func]]

    def register_tool(self, tool: Tool):
        """
        注册Tool对象

        Args:
            tool: Tool实例
        """
        if tool.name in self._tools:
            print(f"⚠️ 警告：工具 '{tool.name}' 已存在，将被覆盖。")

        self._tools[tool.name] = tool
        print(f"✅ 工具 '{tool.name}' 已注册。")

    def register_function(self, name: str, description: str, func: Callable):
        """
        直接注册函数作为工具（简便方式）

        Args:
            name: 工具名称
            description: 工具描述
            func: 工具函数，接受字符串参数，返回字符串结果
        """
        if name in self._functions:
            print(f"⚠️ 警告：工具 '{name}' 已存在，将被覆盖。")

        self._functions[name] = {
            "description": description,# str
            "func": func # 
        }
        print(f"✅ 工具 '{name}' 已注册。")

    def get_tool(self, name: str) -> Optional[Tool]:
        """获取Tool对象"""
        return self._tools.get(name)

    def get_function(self, name: str) -> Optional[Callable]:
        """获取工具函数"""
        func_info = self._functions.get(name)
        return func_info["func"] if func_info else None
    def execute_tool(self, name:str, args):
        # 如果 args 是字符串（JSON格式），需要先解析成字典
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                return f"❌ 工具参数格式错误：无法解析JSON字符串 '{args}'"
        
        if name in self._tools:
            tool = self._tools[name]
            try:
                return tool.run(args)
            except Exception as e:
                err_msg = f"❌ 执行工具 '{name}' 时发生错误: {e}"
                return err_msg
        elif name in self._functions:
            func = self._functions[name]
            try:
                return func(args)
            except Exception as e:
                err_msg = f"❌ 执行工具 '{name}' 时发生错误: {e}"
                return err_msg
        else:
            return f"工具 '{name}' 不存在。"

    def get_tools_descriptor(self) -> List[Dict]:
        """
        获取所有可用工具的OpenAI Function Calling格式描述

        Returns:
            JSON格式字符串，包含所有工具的定义
        """
        tools_list = []

        # 处理Tool对象
        for tool_name, tool in self._tools.items():
            tool_schema = self._build_tool_schema(tool.name, tool.description, tool.get_parameters())
            tools_list.append(tool_schema)

        # 处理函数工具
        for func_name, func_info in self._functions.items():
            parameters = self._extract_function_parameters(func_info["func"])
            tool_schema = self._build_tool_schema(func_name, func_info["description"], parameters)
            tools_list.append(tool_schema)

        return tools_list

    def _build_tool_schema(self, name: str, description: str, parameters: List) -> Dict[str, Any]:
        """
        构建OpenAI Function Calling格式的工具schema

        Args:
            name: 工具名称
            description: 工具描述
            parameters: 参数列表（ToolParameter对象或字典）

        Returns:
            符合OpenAI API格式的工具定义字典
        """
        properties = {}
        required = []

        for param in parameters:
            # 处理ToolParameter对象和字典两种情况
            if hasattr(param, 'dict'):
                param_dict = param.dict()
            else:
                param_dict = param

            param_name = param_dict.get('name', '')
            param_type = param_dict.get('type', 'string')
            param_desc = param_dict.get('description', '')
            is_required = param_dict.get('required', True)

            properties[param_name] = {
                "type": param_type,
                "description": param_desc
            }

            if is_required:
                required.append(param_name)

        return {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

    def _extract_function_parameters(self, func: Callable) -> List[Dict[str, Any]]:
        """
        从函数签名中提取参数信息

        Args:
            func: 函数对象

        Returns:
            参数列表，每个参数包含name、type、description、required等信息
        """
        parameters = []
        sig = inspect.signature(func)

        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue

            param_info = {
                "name": param_name,
                "type": self._get_parameter_type(param.annotation),
                "description": f"参数: {param_name}",
                "required": param.default == inspect.Parameter.empty
            }

            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default

            parameters.append(param_info)

        return parameters

    def _get_parameter_type(self, annotation) -> str:
        """
        根据类型注解转换为OpenAI API支持的类型

        Args:
            annotation: 参数的类型注解

        Returns:
            OpenAI API支持的类型字符串
        """
        if annotation == inspect.Parameter.empty:
            return "string"

        type_str = str(annotation).lower()

        type_mapping = {
            "int": "integer",
            "float": "number",
            "bool": "boolean",
            "str": "string",
            "list": "array",
            "dict": "object",
        }

        for key, value in type_mapping.items():
            if key in type_str:
                return value

        return "string"

    def get_tools_descriptor_list(self) -> List[Dict[str, Any]]:
        """
        获取所有工具的字典列表格式（比JSON字符串更易于编程操作）

        Returns:
            工具列表
        """
        return json.loads(self.get_tools_descriptor())
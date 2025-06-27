# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An image generation agent implemented by assistant"""

import json
import os
import urllib.parse
import base64

import json5
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
from qwen_agent.tools.base import BaseTool, register_tool

ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')


# 更简单的 MCP 图片生成工具
@register_tool('mcp_image_gen')
class MCPImageGen(BaseTool):
    description = 'Call MCP service to generate image and save as file automatically.'
    parameters = [
        {
            'name': 'prompt',
            'type': 'string',
            'description': 'Text description of the image to generate.',
            'required': True
        },
        {
            'name': 'width',
            'type': 'integer',
            'description': 'Width of the image to generate.',
            'required': False
        },
        {
            'name': 'height',
            'type': 'integer',
            'description': 'Height of the image to generate.',
            'required': False
        },
        {
            'name': 'steps',
            'type': 'integer',
            'description': 'Steps of the image to generate.',
            'required': False,
        },
        {
            'name': 'guidance_scale',
            'type': 'float',
            'description': 'Guidance scale of the image to generate.',
            'required': False,
        }
    ]

    def call(self, params: str, **kwargs) -> str:
        import time
        import asyncio
        from qwen_agent.tools.mcp_manager import MCPManager
        
        args = json.loads(params)
        prompt = args['prompt']
        
        try:
            # 获取 MCP 管理器
            mcp_manager = MCPManager()
            
            # 假设你的 MCP 服务有一个名为 'generate_image' 的工具
            # 你需要根据实际的 MCP 工具名称调整
            target_tool_name = 'generate_image'  # 替换为你的实际工具名
            
            # 查找目标工具
            target_client = None
            target_tool = None
            
            for client_id, client in mcp_manager.clients.items():
                if hasattr(client, 'tools') and client.tools:
                    for tool in client.tools:
                        if tool.name == target_tool_name:
                            target_client = client
                            target_tool = tool
                            break
                    if target_client:
                        break
            
            if not target_client:
                return "Error: MCP image generation tool not found"
            
            # 调用 MCP 工具
            tool_args = {"prompt": prompt}
            future = asyncio.run_coroutine_threadsafe(
                target_client.execute_function(target_tool_name, tool_args),
                mcp_manager.loop
            )
            
            # 获取结果
            result = future.result()
            
            # 假设结果包含 base64 数据
            # 你需要根据实际返回格式调整解析逻辑
            if isinstance(result, str):
                base64_str = result
            else:
                # 如果结果是 JSON 或其他格式，需要解析
                base64_str = str(result)
            
            # 保存为文件
            timestamp = int(time.time())
            filename = f"mcp_generated_{timestamp}.png"
            
            if ',' in base64_str:
                base64_str = base64_str.split(',')[1]
            
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(base64_str))
            
            return f"Image generated via MCP and saved as: {filename}"
            
        except Exception as e:
            return f"Error calling MCP service: {str(e)}"


def init_agent_service():
    llm_cfg = { 'model': 'qwen-max-latest',
               'model_type': 'qwen_dashscope',
               'api_key': 'sk-20140248ea1544d0855b515aac4a576b'}
    system = ("You are an AI assistant that generates images. When you need to generate an image: "
              "1. Use the 'smart_image_gen' tool to generate and save the image as a file. "
              "2. The tool will return a file path instead of base64 data. "
              "3. Use the file path with code_interpreter to process the image. "
              "4. Never pass large base64 strings to code_interpreter - always use file paths.")

    tools = [
        'mcp_image_gen',    # 直接调用 MCP 服务生成图片
        'code_interpreter',
        {
            "mcpServers": {
                "demo":{
                    "type":"sse",
                    "url": "http://10.240.243.203:30505/sse"
                    }
                }
        }
    ]
    bot = Assistant(
        llm=llm_cfg,
        name='AI painting',
        description='AI painting service',
        system_message=system,
        function_list=tools,
        files=[os.path.join(ROOT_RESOURCE, 'guide.md')],
    )

    return bot


def test(query: str = 'draw a dog'):
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = [{'role': 'user', 'content': query}]
    for response in bot.run(messages=messages):
        print('bot response:', response)


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    while True:
        query = input('user question: ')
        messages.append({'role': 'user', 'content': query})
        response = []
        for response in bot.run(messages=messages):
            print('bot response:', response)
        messages.extend(response)


def app_gui():
    # Define the agent
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [
            '画一只猫的图片',
            '画一只可爱的小腊肠狗',
            '画一幅风景画，有湖有山有树',
        ]
    }
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()

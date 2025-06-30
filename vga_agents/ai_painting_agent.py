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

import json5
import pathlib

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
from qwen_agent.tools.base import BaseTool, register_tool

ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')
SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), 'system_prompt.md')


def read_system_prompt():
    with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def init_agent_service():
    llm_cfg = {
        'model': '/models/Qwen3-32B/Qwen3-32B',
        'model_server': 'http://10.240.243.203:30038/v1',  # base_url，也称为 api_base
        'api_key': 'EMPTY'
    }
    system = read_system_prompt()

    tools = [
        'code_interpreter',
        {
            "mcpServers": {
                "demo":{
                    "type":"sse",
                    "url": "http://10.240.243.203:30505/sse"
                    }
                }
        }
    ]  # code_interpreter is a built-in tool in Qwen-Agent
    bot = Assistant(
        llm=llm_cfg,
        name='AI painting',
        description='AI painting service',
        system_message=system,
        function_list=tools,
        files=[
            os.path.join(ROOT_RESOURCE, 'proceed_img_guide.md'),
            os.path.join(ROOT_RESOURCE, 'flux_tool_guide.md')
        ],
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
    ).run(server_name="0.0.0.0",erver_port=7860)


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()

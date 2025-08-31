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

import os
import sys
import subprocess
import json
from typing import Union

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
from qwen_agent.tools.base import BaseTool, register_tool
from dotenv import load_dotenv
load_dotenv()


ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')
SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), 'system_prompt.md')


@register_tool('image_generation')
class ImageGenerationTool(BaseTool):
    """
    图片生成工具，通过调用 image_gen_run.py 脚本生成图片
    """
    description = 'Generate images using ComfyUI workflow with custom prompts and resolution'
    parameters = [{
        'name': 'prompt',
        'type': 'string',
        'description': 'The prompt for image generation',
        'required': True
    }, {
        'name': 'width',
        'type': 'integer',
        'description': 'Image width in pixels (default: 1024)',
        'required': False
    }, {
        'name': 'height',
        'type': 'integer',
        'description': 'Image height in pixels (default: 1024)',
        'required': False
    }, {
        'name': 'output_dir',
        'type': 'string',
        'description': 'Output directory for generated images (optional)',
        'required': False
    }]

    def call(self, params: Union[str, dict], **kwargs) -> dict:
        """
        调用图片生成脚本
        """
        # 处理参数格式 - 可能是字符串或字典
        if isinstance(params, str):
            try:
                params_dict = json.loads(params)
            except json.JSONDecodeError:
                return {'error': f'Invalid JSON format in params: {params}'}
        elif isinstance(params, dict):
            params_dict = params
        else:
            return {'error': f'Unsupported params type: {type(params)}'}

        prompt = params_dict.get('prompt', '')
        width = params_dict.get('width', 1024)
        height = params_dict.get('height', 1024)
        output_dir = params_dict.get('output_dir', './generated_images')

        if not prompt:
            return {'error': 'Prompt is required for image generation'}

        # 验证分辨率参数
        try:
            width = int(width) if width is not None else 1024
            height = int(height) if height is not None else 1024
        except (ValueError, TypeError):
            return {'error': 'Width and height must be valid integers'}

        # 检查分辨率范围 (ComfyUI/Flux 的合理范围)
        if width < 256 or width > 2048:
            return {'error': 'Width must be between 256 and 2048 pixels'}
        if height < 256 or height > 2048:
            return {'error': 'Height must be between 256 and 2048 pixels'}

        # 确保是16的倍数 (Flux模型要求)
        width = (width // 16) * 16
        height = (height // 16) * 16

        # 验证所有必需的参数都不为 None
        if sys.executable is None:
            return {'error': 'Python executable not found'}

        try:
            # 获取 image_gen_run.py 的路径
            image_gen_script = os.path.join(os.path.dirname(__file__), 'image_gen', 'image_gen_run.py')

            # 验证脚本文件存在
            if not os.path.exists(image_gen_script):
                return {'error': f'Image generation script not found: {image_gen_script}'}

            # 确保所有参数都是字符串
            prompt = str(prompt) if prompt is not None else ''
            output_dir = str(output_dir) if output_dir is not None else './generated_images'

            # 构建命令 - 确保所有元素都是字符串
            cmd = [
                str(sys.executable),
                str(image_gen_script),
                '--prompt', prompt,
                '--width', str(width),
                '--height', str(height),
                '--output_dir', output_dir
            ]

            # 执行命令
            print(f"Executing: {' '.join(str(x) for x in cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1200  # 20分钟超时
            )

            if result.returncode == 0:
                # 解析输出中的生成文件列表
                output_lines = result.stdout.strip().split('\n')
                generated_files = []
                for line in output_lines:
                    if line.startswith('Generated files:'):
                        # 解析生成的JSON格式的文件列表
                        try:
                            files_str = line.replace('Generated files:', '').strip()
                            generated_files = json.loads(files_str)
                        except:
                            # 如果解析失败，手动查找输出文件
                            pass
                    elif 'saved:' in line or 'downloaded:' in line:
                        file_path = line.split(':')[1].strip()
                        generated_files.append(file_path)

                return {
                    'success': True,
                    'message': f'Successfully generated {len(generated_files)} image(s)',
                    'generated_files': generated_files,
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': f'Image generation failed: {result.stderr}',
                    'output': result.stdout
                }

        except subprocess.TimeoutExpired:
            return {'error': 'Image generation timed out'}
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'}


def read_system_prompt():
    with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def init_agent_service():
    # llm_cfg = {
    #     'model': '/models/Qwen3-32B/Qwen3-32B',
    #     'model_server': 'http://10.240.243.203:30038/v1',  # base_url，也称为 api_base
    #     'api_key': 'EMPTY'
    # }
    #
    llm_cfg = { 'model': 'qwen-max-latest',
               'model_type': 'qwen_dashscope',
               'api_key': 'sk-20140248ea1544d0855b515aac4a576b'}
    system = read_system_prompt()

    # tools = [
    #     'code_interpreter',
    #     'video_gen',
    #     {
    #         "mcpServers": {
    #             "text2image": {
    #                 "type": "sse",
    #                 "url": "http://10.240.243.203:30787/sse"
    #             },
    #             "image_editing": {
    #                 "type": "sse",
    #                 "url": "http://10.240.243.203:32074/sse"
    #             }
    #         }
    #     }
    # ]
    tools = [
        'image_generation',
        'code_interpreter'
    ]
    # code_interpreter is a built-in tool in Qwen-Agent
    bot = Assistant(
        llm=llm_cfg,
        name='AI HMI Agent',
        description='动态生成AI HMI的智能体',
        system_message=system,
        function_list=tools,
        files=[
            os.path.join(ROOT_RESOURCE, 'proceed_img_guide.md')
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
            '生成一张桌面壁纸，3D可爱卡通风'
        ]
    }
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run(server_name="0.0.0.0", erver_port=7860)


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()

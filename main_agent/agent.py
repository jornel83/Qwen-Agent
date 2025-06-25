import os

from qwen_agent.agents import Assistant

# import MyImageGen to register the tool when this module is imported
import tools  # noqa: F401

ROOT_DIR = os.path.dirname(__file__)
ROOT_RESOURCE = os.path.join(ROOT_DIR, 'resource')
SYSTEM_PROMPT_FILE = os.path.join(ROOT_DIR, 'system_prompt.md')


def init_agent_service():
    """Initialize the image generation agent."""
    llm_cfg = {'model': 'qwen-max-latest',
               'model_type': 'qwen_dashscope',
               'api_key': 'sk-20140248ea1544d0855b515aac4a576b'}
    with open(SYSTEM_PROMPT_FILE, 'r', encoding='utf-8') as f:
        system = f.read()

    tool_list = [
        'my_image_gen',
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
        function_list=tool_list,
        files=[os.path.join(ROOT_RESOURCE, 'guide.md')],
    )
    return bot
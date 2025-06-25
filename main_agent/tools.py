import json
import urllib.parse

import json5

from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('my_image_gen')
class MyImageGen(BaseTool):
    """Generate image via Pollinations API."""

    description = ('AI painting (image generation) service, input text description, and return '
                   'the image URL drawn based on text information.')
    parameters = [{
        'name': 'prompt',
        'type': 'string',
        'description': 'Detailed description of the desired image content, in English',
        'required': True,
    }]

    def call(self, params: str, **kwargs) -> str:
        prompt = json5.loads(params)['prompt']
        prompt = urllib.parse.quote(prompt)
        url = 'https://image.pollinations.ai/prompt/{}'.format(prompt)
        return json.dumps(
            {
                'image_url': url,
            },
            ensure_ascii=False,
        )
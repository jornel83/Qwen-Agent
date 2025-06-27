import json
import base64
import os
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('base64_to_file')
class Base64ToFileTool(BaseTool):
    description = 'Convert base64 string to a local file and return the file path.'
    parameters = [{
        'name': 'base64_str',
        'type': 'string',
        'description': 'The base64-encoded string of the image.',
        'required': True,
    }, {
        'name': 'filename',
        'type': 'string',
        'description': 'The output file name (e.g., output.png).',
        'required': True,
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params)
        base64_str = args['base64_str']
        filename = args['filename']
        
        # Remove prefix if present
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        
        # Decode and save
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(base64_str))
        
        return f"File saved as: {filename}"
from qwen_agent.gui import WebUI

from agent import init_agent_service


def app_gui():
    """Launch the WebUI for chatting with the agent."""
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
    app_gui()
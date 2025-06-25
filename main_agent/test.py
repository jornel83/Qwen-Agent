from .agent import init_agent_service


def test(query: str = 'draw a dog'):
    """Simple test interface for the agent."""
    bot = init_agent_service()
    messages = [{'role': 'user', 'content': query}]
    for response in bot.run(messages=messages):
        print('bot response:', response)


if __name__ == '__main__':
    test()
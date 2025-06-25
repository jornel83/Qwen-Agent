from .agent import init_agent_service


def app_tui():
    """Interactive text-based chat."""
    bot = init_agent_service()

    messages = []
    while True:
        query = input('user question: ')
        messages.append({'role': 'user', 'content': query})
        responses = []
        for resp in bot.run(messages=messages):
            print('bot response:', resp)
            responses.append(resp)
        messages.extend(responses)


if __name__ == '__main__':
    app_tui()
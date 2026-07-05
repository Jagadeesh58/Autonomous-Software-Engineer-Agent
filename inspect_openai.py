import openai
import requests
import rich
print('openai', getattr(openai, '__version__', 'unknown'))
print('openai file', openai.__file__)
print('requests', getattr(requests, '__version__', 'unknown'))
print('rich', getattr(rich, '__version__', 'unknown'))
try:
    from openai import OpenAI
    print('OpenAI constructor ok')
    print('OpenAI class', OpenAI)
    # See if chat.completions exists
    print('has chat', hasattr(OpenAI, 'chat'))
except Exception as e:
    print('OpenAI inspect failed', type(e).__name__, e)

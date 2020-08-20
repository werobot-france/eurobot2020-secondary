import random
import time
import re
import sys
import pygments

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text

from src.WordCompleter import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style

from pygments.lexers.python import Python3Lexer

from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import style_from_pygments_cls

#from pygson.json_lexer import JSONLexer
from pygments.styles import get_style_by_name
from pygments.token import Token

from src.WebSocketClient import WebSocketClient
from src.OutputLexer import OutputLexer
from src.InputLexer import InputLexer

import json

from websocket import create_connection

uri = sys.argv[1] if len(sys.argv) > 1 else "ws://192.168.1.128:8082"

print('> Using uri:', uri)

client = WebSocketClient(uri)
client.start()

data = client.send('listCommands', {}, True)
data = list(map (lambda c: c['name'], data))

sql_completer = WordCompleter(data, ignore_case=True)

style = Style.from_dict({
  'completion-menu.completion': 'bg:#008888 #ffffff',
  'completion-menu.completion.current': 'bg:#00aaaa #000000',
  'scrollbar.background': 'bg:#88aaaa',
  'scrollbar.button': 'bg:#222222',
})

session = PromptSession(
  history=FileHistory('./.main-prompt-history'),
  lexer=PygmentsLexer(InputLexer),
  completer=sql_completer,
  style=style_from_pygments_cls(get_style_by_name(u'monokai')),
  reserve_space_for_menu=2
)

while True:
  try:
    text = session.prompt('>>> ', auto_suggest=AutoSuggestFromHistory())
  except KeyboardInterrupt:
    continue
  except EOFError:
    break
  else:
    #print('You entered:', text)
    res = client.send('execCommand', {'payload': text}, True)
    res = json.dumps(res, indent=4)
    # if res[0:2] == '["' or res[0:2] == '{"':
      
    # else:
    #   print(res)
    tokens = list(pygments.lex(res, lexer=OutputLexer()))
    res = PygmentsTokens(tokens)
    res.token_list.pop()
    print_formatted_text(res, style=style_from_pygments_cls(get_style_by_name(u'monokai')))
    
print('GoodBye!')
client.stop()
sys.exit()

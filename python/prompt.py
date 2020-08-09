import random
import time
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.sql import SqlLexer

from src.WebSocketClient import WebSocketClient

import json

from websocket import create_connection

ws = create_connection(
  "ws://localhost:8082/?identifier=" + str(random.randint(1000, 9999)) + '_' + str(round(time.time(), 3))
)

ws.send(json.dumps({'command': 'listCommands', 'args': {}}))

res = ws.recv()
data = list(map (lambda c: c['name'], json.loads(res)['data']))

sql_completer = WordCompleter(data, ignore_case=True)

style = Style.from_dict({
  'completion-menu.completion': 'bg:#008888 #ffffff',
  'completion-menu.completion.current': 'bg:#00aaaa #000000',
  'scrollbar.background': 'bg:#88aaaa',
  'scrollbar.button': 'bg:#222222',
})

session = PromptSession(
  history=FileHistory('./.main-prompt-history'),
  lexer=PygmentsLexer(SqlLexer),
  completer=sql_completer,
  style=style
)

while True:
  try:
    text = session.prompt('> ', auto_suggest=AutoSuggestFromHistory())
  except KeyboardInterrupt:
    continue
  except EOFError:
    break
  else:
    #print('You entered:', text)
    ws.send(json.dumps({'command': 'execCommand', 'args': {'payload': text}}))
    res = ws.recv()
    res = json.dumps(json.loads(res)['data'], indent=4)
    if res[0:2] == '["' or res[0:2] == '{"':
      print(res)
    else:
      print(res)
    
print('GoodBye!')
ws.close()
sys.exit()
from pygments.lexer import include, RegexLexer

from pygments.token import Token
import re


# The JSONLexer is an attempt at parsing JSON that is more JSON-aware
# than the JavaScript lexer.  The key difference is that it makes an attempt
# to distinguish between attribute names and values to provide more useful
# syntax highlighting than would be available when parsed as a JavaScript
# expression

class InputLexer(RegexLexer):
    name = 'Diff'
    aliases = ['diff']
    filenames = ['*.diff']

    tokens = {
        'root': [
            (r'[a-zA-Z_]+=', Token.Comment),
            (r'-?[0-9.]+', Token.Number.Integer),
            (r'(true|false|null)\b', Token.Keyword.Constant),
            (r'[a-zA-Z]{0,}\S', Token.Name.Builtin),
            (r'\s', Token.Text),
        ]
    }
    
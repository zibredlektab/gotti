import re

tokens_rx = re.compile(r"""(?x)
    (?P<open>\[(?P<name>\w+)\s*)    |       # open bracket with word
    (?P<close>])                    |       # close bracket
    (?P<other>[^][]+)                       # anything else
    """)

def markup_to_django(text):
    # Cases:
    #
    #   [robert]
    #   {% card "robert" %}
    #
    #   [robert King Baratheon]
    #   {% card "robert" "King Baratheon" %}
    #
    #   [1002 Cersei is killed.]
    #   {% if pos >= 1002 %}Cersei is killed.{% endif %}
    #
    #   [if pos < 1023]foo[endif]
    #   {% if pos < 1023 %}foo{% endif %}
    #
    #   [if pos < 1023]foo[else]bar[endif]
    #   {% if pos < 1023 %}foo{% else %}bar{% endif %}

    closes = []
    pieces = []
    for match in tokens_rx.finditer(text):
        tokname = match.lastgroup
        tok = match.group(0)
        #print "%s: %r" % (tokname, tok)
        if tokname == 'open':
            name = match.group("name")
            try:
                pos = int(name)
            except ValueError:
                pos = None

            if pos is not None:
                pieces.append('{% if pos >= ')
                pieces.append(name)
                pieces.append(' %}')
                closes.append('{% endif %}')
            elif name in ["if", "endif", "else", "elif"]:
                pieces.append('{% ')
                pieces.append(name)
                pieces.append(' ')
                closes.append(' %}')
            else:
                pieces.append('{% card "')
                pieces.append(name)
                pieces.append('" "')
                closes.append('" %}')
        elif tokname == 'close':
            pieces.append(closes.pop())
        elif tokname == 'other':
            pieces.append(tok)
        else:
            pieces.append("(unknown token: %r %r)" % (tokname, tok))

    return ''.join(pieces)


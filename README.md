# Grex

Search for patterns in a unix-like way.

Basic usage:

```py
text = """
Hello, world!
Welcome to the world of Python!
This is a grex example.
I am a grex.
We are grex.
"""

print(text | grep(r'i', ignore_case=True))
```

```sh
This is a grex example.
I am a grex.
```

The `pattern` argument is handled as a regular expression.

You can pipe multiple greps.

```py
"""
follow
hello
yellow
""" | grep("ello") | grep('w')
```

```sh
yellow
```

Use `colored=True` to highlight the matches.

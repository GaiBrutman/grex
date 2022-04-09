import re
from typing import Iterable, Union

import colorama


class GrexHit:
    """
    A Grex matched string.
    """

    def __init__(self, string, matches: Iterable[re.Match], colored=False):
        """
        A Grex matched line.

        :param string: The matched string.
        :param matches: The regex matches in the string.
        :param colored: Whether to color the string, defaults to False.
        """

        self.string = string
        self.matches = matches
        self.colored = colored

    def colored_string(self) -> str:
        """
        Construct the matched string with colored matches.

        :return: The colored string.
        """

        colored_string = self.string
        for match in self.matches:
            colored_string = colored_string.replace(
                match.group(), colorama.Fore.RED + match.group() + colorama.Style.RESET_ALL)
        return colored_string

    def __repr__(self):
        if self.colored:
            return self.colored_string()
        else:
            return self.string


class GrexHits:
    """
    A list of 'GrexHit's.
    """

    def __init__(self, hits: Iterable[re.Match]):
        self.hits = hits

    def __iter__(self):
        return self.hits.__iter__()

    def __repr__(self):
        return "\n".join(map(str, self))


class Grex:
    def __init__(self, pattern: Union[str, re.Pattern], colored=False):
        self.pattern = pattern if isinstance(
            pattern, re.Pattern) else re.compile(pattern)
        self.colored = colored

    def find(self, text: str) -> GrexHits:
        """
        Find all matches in a text, returning the hits.

        :param text: The text to search in.
        :return: A GrexHits object with the hits.
        """

        matches = []
        for line in text.splitlines():
            re_matches = list(self.pattern.finditer(line))
            if re_matches:
                matches.append(
                    GrexHit(line, re_matches, colored=self.colored))
        return GrexHits(matches)

    def __ror__(self, other: str) -> str:
        """
        Use find as a pipe operator.

        :param other: The text to search in.
        :raises TypeError: Accept only str objects.
        :return: A GrexHits object with the hits.

        :example:
        >>> grex = Grex("ll", colored=True)
        >>> "Hello, world!" | grex
        """

        if not isinstance(other, str):
            raise TypeError(f"Can't use '|' operator with {type(other)}")

        return self.find(other)


def grex(pattern: Union[str, re.Pattern], ignore_case=False, colored=False) -> Grex:
    """
    A wrapper for the 'Grex' class.

    :param pattern: The pattern to match.
    :param ignore_case: Whether to ignore cases when searching, defaults to False.
    :param colored: Whether to color the output hits, defaults to False.
    :return: The grex object.
    """

    if ignore_case:
        pattern = re.compile(pattern, re.IGNORECASE)
    return Grex(pattern, colored)


# For compatibility with the unix clone.
grep = grex

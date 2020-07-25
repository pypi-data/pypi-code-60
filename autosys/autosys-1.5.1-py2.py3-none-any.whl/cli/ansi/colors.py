# -*- coding: utf-8 -*-

# 'Standard Library'
import re
import sys

from functools import partial

# 'package imports'
from autosys.csscolors import css_colors, parse_rgb

# _PY2 = sys.version_info[0] == 2
# string_types = basestring if _PY2 else str
# Python 2.x no longer supported ... string_types is a passthrough now
string_types = str

template = "\x1b[{0}m{1}\x1b[0m"

# ANSI color names. There is also a "default"
COLORS = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
)

# ANSI style names
STYLES = (
    "none",
    "bold",
    "faint",
    "italic",
    "underline",
    "blink",
    "blink2",
    "negative",
    "concealed",
    "crossed",
)


def is_string(obj):
    """
    Is the given object a string?
    """
    return isinstance(obj, string_types)


def _join(*values):
    """
    Join a series of values with semicolons. The values
    are either integers or strings, so stringify each for
    good measure. Worth breaking out as its own function
    because semicolon-joined lists are core to ANSI coding.
    """
    return ";".join(str(v) for v in values)


def _color_code(spec, base):
    """
    Workhorse of encoding a color. Give preference to named colors from
    ANSI, then to specific numeric or tuple specs. If those don't work,
    try looking up CSS color names or parsing CSS color specifications
    (hex or rgb).

    :param str|int|tuple|list spec: Unparsed color specification
    :param int base: Either 30 or 40, signifying the base value
        for color encoding (foreground and background respectively).
        Low values are added directly to the base. Higher values use `
        base + 8` (i.e. 38 or 48) then extended codes.
    :returns: Discovered ANSI color encoding.
    :rtype: str
    :raises: ValueError if cannot parse the color spec.
    """
    if is_string(spec):
        spec = spec.strip().lower()

    if spec == "default":
        return _join(base + 9)
    elif spec in COLORS:
        return _join(base + COLORS.index(spec))
    elif isinstance(spec, int) and 0 <= spec <= 255:
        return _join(base + 8, 5, spec)
    elif isinstance(spec, (tuple, list)):
        return _join(base + 8, 2, _join(*spec))
    else:
        rgb = parse_rgb(spec)
        # parse_rgb raises ValueError if cannot parse spec
        # or returns an rgb tuple if it can
        return _join(base + 8, 2, _join(*rgb))


def color(s, fg=None, bg=None, style=None):
    """
    Add ANSI colors and styles to a string.

    :param str s: String to format.
    :param str|int|tuple fg: Foreground color specification.
    :param str|int|tuple bg: Background color specification.
    :param str: Style names, separated by '+'
    :returns: Formatted string.
    :rtype: str (or unicode in Python 2, if s is unicode)
    """
    codes = []

    if fg:
        codes.append(_color_code(fg, 30))
    if bg:
        codes.append(_color_code(bg, 40))
    if style:
        for style_part in style.split("+"):
            if style_part in STYLES:
                codes.append(STYLES.index(style_part))
            else:
                raise ValueError('Invalid style "%s"' % style_part)

    if codes:
        template = "\x1b[{0}m{1}\x1b[0m"
        # Python 2.x no longer supported
        # if _PY2 and isinstance(s, unicode):
        # Take care in PY2 to return str if str is given, or unicode if
        # unicode given. A pain, but PY2's fragility with Unicode makes it
        # important to avoid disruptions (including gratuitous up-casting
        # of str to unicode) that might trigger downstream errors.
        # template = unicode(template)
        return template.format(_join(*codes), s)
    else:
        return s


def strip_color(s):
    """
    Remove ANSI color/style sequences from a string. The set of all possible
    ANSI sequences is large, so does not try to strip every possible one. But
    does strip some outliers seen not just in text generated by this module, but
    by other ANSI colorizers in the wild. Those include `\x1b[K` (aka EL or
    erase to end of line) and `\x1b[m`, a terse version of the more common
    `\x1b[0m`.
    """
    return re.sub("\x1b\\[(K|.*?m)", "", s)


def ansilen(s):
    """
    Given a string with embedded ANSI codes, what would its
    length be without those codes?
    """
    return len(strip_color(s))


# Foreground color shortcuts
black = partial(color, fg="black")
red = partial(color, fg="red")
green = partial(color, fg="green")
yellow = partial(color, fg="yellow")
blue = partial(color, fg="blue")
magenta = partial(color, fg="magenta")
cyan = partial(color, fg="cyan")
white = partial(color, fg="white")

# Style shortcuts
bold = partial(color, style="bold")
none = partial(color, style="none")
faint = partial(color, style="faint")
italic = partial(color, style="italic")
underline = partial(color, style="underline")
blink = partial(color, style="blink")
blink2 = partial(color, style="blink2")
negative = partial(color, style="negative")
concealed = partial(color, style="concealed")
crossed = partial(color, style="crossed")

if __name__ == "__main__":
    pass

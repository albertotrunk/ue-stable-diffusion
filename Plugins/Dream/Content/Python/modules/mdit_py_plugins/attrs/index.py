from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from .parse import ParseError, parse


def attrs_plugin(md: MarkdownIt, *, after=("image", "code_inline")):
    """Parse inline attributes that immediately follow certain inline elements::

        ![alt](https://image.com){#id .a b=c}

    Inside the curly braces, the following syntax is possible:

    - `.foo` specifies foo as a class.
      Multiple classes may be given in this way; they will be combined.
    - `#foo` specifies foo as an identifier.
      An element may have only one identifier;
      if multiple identifiers are given, the last one is used.
    - `key="value"` or `key=value` specifies a key-value attribute.
       Quotes are not needed when the value consists entirely of
       ASCII alphanumeric characters or `_` or `:` or `-`.
       Backslash escapes may be used inside quoted values.
    - `%` begins a comment, which ends with the next `%` or the end of the attribute (`}`).

    **Note:** This plugin is currently limited to "self-closing" elements,
    such as images and code spans. It does not work with links or emphasis.

    :param md: The MarkdownIt instance to modify.
    :param after: The names of inline elements after which attributes may be specified.
    """

    def attr_rule(state: StateInline, silent: bool):
        if state.pending or not state.tokens:
            return False
        token = state.tokens[-1]
        if token.type not in after:
            return False
        try:
            new_pos, attrs = parse(state.src[state.pos :])
        except ParseError:
            return False
        state.pos += new_pos + 1
        if not silent:
            if "class" in attrs and "class" in token.attrs:
                attrs["class"] = f"{token.attrs['class']} {attrs['class']}"
            token.attrs.update(attrs)

        return True

    md.inline.ruler.push("attr", attr_rule)

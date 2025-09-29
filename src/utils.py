import re


def slugify(string: str) -> str:
    """
    Convert string to slug: remove extra spaces, convert to lowercase,
    and replace all non-word characters with underscores.
    """
    string = string.strip().lower()
    string = re.sub(r"\W+", "_", string)
    string = string.strip("_")

    return string

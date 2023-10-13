def to_camel(string: str) -> str:
    """
    Convert snake case to camel case.

    :param string: string.
    :return: camel case string.
    """
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])

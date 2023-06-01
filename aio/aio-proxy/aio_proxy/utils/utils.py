def str_to_list(string_values: str) -> list[str] | None:
    if string_values is None:
        return None
    values_list = string_values.split(",")
    return values_list

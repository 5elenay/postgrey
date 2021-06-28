def raise_error(variable, name, check) -> None:
    if isinstance(check, tuple):
        if not type(variable) in check:
            raise TypeError(
                f"Argument '{name}' type must be {' / '.join([i.__name__ if i != None else 'None' for i in check])}, not {type(variable).__name__}.")
    else:
        if not isinstance(variable, check):
            raise TypeError(
                f"Argument '{name}' type must be {check.__name__ if check != None else 'None'}, not {type(variable).__name__}.")


def parse_data(data) -> tuple:
    d_keys, d_values, d_count = [], [], 1

    for key in data.keys():
        if not key.startswith("__") and not key.endswith("__"):
            d_keys.append(
                f"{key} {data.get(f'__{key}__') or '='} ${d_count}")
            d_values.append(data.get(key))
            d_count += 1

    return d_keys, d_values, d_count

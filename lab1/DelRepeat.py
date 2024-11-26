def validate_field(value, field_name, expected_type):
    if not isinstance(value, expected_type) or not value.strip():
        raise ValueError(f"{field_name} должно быть типа {expected_type.__name__}.")
    return value.strip()

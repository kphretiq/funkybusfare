"""
Shamelessly copied from https://github.com/benhodgson/protobuf-to-dict

No modifications to code other some linter-suggested safety-clownage,
this message and running 2to3 on it.

Should probably refactor docstrings for consistency.
"""

from google.protobuf.message import Message
from google.protobuf.descriptor import FieldDescriptor


__all__ = [
    "protobuf_to_dict",
    "TYPE_CALLABLE_MAP",
    "dict_to_protobuf",
    "REVERSE_TYPE_CALLABLE_MAP",
]


EXTENSION_CONTAINER = "___X"


TYPE_CALLABLE_MAP = {
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_INT64: int,
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_UINT64: int,
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SINT64: int,
    FieldDescriptor.TYPE_FIXED32: int,
    FieldDescriptor.TYPE_FIXED64: int,
    FieldDescriptor.TYPE_SFIXED32: int,
    FieldDescriptor.TYPE_SFIXED64: int,
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_BYTES: lambda b: b.encode("base64"),
    FieldDescriptor.TYPE_ENUM: int,
}


def repeated(type_callable):
    """
    Flatten redundant labels.
    """
    return lambda value_list: [type_callable(value) for value in value_list]


def enum_label_name(field, value):
    """
    Extract label name
    """
    return field.enum_type.values_by_number[int(value)].name


def protobuf_to_dict(_pb, type_callable_map=None, use_enum_labels=False):
    """
    Convert protobuf object to a dictionary.
    """
    if not type_callable_map:
        type_callable_map = TYPE_CALLABLE_MAP
    result_dict = {}
    extensions = {}
    for field, value in _pb.ListFields():
        type_callable = _get_field_value_adaptor(
            _pb, field, type_callable_map, use_enum_labels
        )
        if field.label == FieldDescriptor.LABEL_REPEATED:
            type_callable = repeated(type_callable)

        if field.is_extension:
            extensions[str(field.number)] = type_callable(value)
            continue

        result_dict[field.name] = type_callable(value)

    if extensions:
        result_dict[EXTENSION_CONTAINER] = extensions
    return result_dict

def _get_field_value_adaptor(_pb, field, type_callable_map={}, use_enum_labels=False):

    """
    Args:
        _pb (tgfs_realtime_pb2.*): ProtocolMessage
        field (tgfs_realtime_pb2.*): ProtocolMessage
        type_callable_map (dict): Enumerated ``<class 'type'>`` objects
        use_enum_labels (bool)
    """

    if not type_callable_map:
        type_callable_map = TYPE_CALLABLE_MAP

    if field.type == FieldDescriptor.TYPE_MESSAGE:
        # recursively encode protobuf sub-message
        return lambda _pb: protobuf_to_dict(
            _pb, type_callable_map=type_callable_map, use_enum_labels=use_enum_labels
        )

    if use_enum_labels and field.type == FieldDescriptor.TYPE_ENUM:
        return lambda value: enum_label_name(field, value)

    if field.type in type_callable_map:
        return type_callable_map[field.type]

    raise TypeError(
        "Field %s.%s has unrecognised type id %d"
        % (_pb.__class__.__name__, field.name, field.type)
    )


def get_bytes(value):
    """
    Decode base64 encoded value.
    """
    return value.decode("base64")


REVERSE_TYPE_CALLABLE_MAP = {
    FieldDescriptor.TYPE_BYTES: get_bytes,
}


def dict_to_protobuf(
    pb_klass_or_instance,
    values,
    type_callable_map=None,
    strict=True,
):
    """Populates a protobuf model from a dictionary.

    :param pb_klass_or_instance: a protobuf message class, or an protobuf instance
    :type pb_klass_or_instance: a type or instance of a subclass of google.protobuf.message.Message
    :param dict values: a dictionary of values. Repeated and nested values are
       fully supported.
    :param dict type_callable_map: a mapping of protobuf types to callables for setting
       values on the target instance.
    :param bool strict: complain if keys in the map are not fields on the message.
    """
    if not type_callable_map:
        type_callable_map = REVERSE_TYPE_CALLABLE_MAP
    if isinstance(pb_klass_or_instance, Message):
        instance = pb_klass_or_instance
    else:
        instance = pb_klass_or_instance()
    return _dict_to_protobuf(instance, values, type_callable_map, strict)


def _get_field_mapping(_pb, dict_value, strict):
    field_mapping = []
    for key, value in list(dict_value.items()):
        if key == EXTENSION_CONTAINER:
            continue
        if key not in _pb.DESCRIPTOR.fields_by_name:
            if strict:
                raise KeyError(
                    f"{_pb} does not have a field called {key}"
                ) from KeyError
            continue
        field_mapping.append(
            (_pb.DESCRIPTOR.fields_by_name[key], value, getattr(_pb, key, None))
        )

    for ext_num, ext_val in list(dict_value.get(EXTENSION_CONTAINER, {}).items()):
        try:
            ext_num = int(ext_num)
        except ValueError:
            raise ValueError("Extension keys must be integers.") from ValueError
        if ext_num not in _pb._extensions_by_number:
            if strict:
                message = f"""{_pb} does not have a extension with number {ext_num}.
                Perhaps you forgot to import it?"""
                raise KeyError(message) from KeyError
            continue
        ext_field = _pb._extensions_by_number[ext_num]
        _pb_val = None
        _pb_val = _pb.Extensions[ext_field]
        field_mapping.append((ext_field, ext_val, _pb_val))

    return field_mapping


def _dict_to_protobuf(_pb, value, type_callable_map, strict):
    fields = _get_field_mapping(_pb, value, strict)

    for field, input_value, _pb_value in fields:
        if field.label == FieldDescriptor.LABEL_REPEATED:
            for item in input_value:

                if field.type == FieldDescriptor.TYPE_MESSAGE:
                    message = _pb_value.add()
                    _dict_to_protobuf(message, item, type_callable_map, strict)
                elif field.type == FieldDescriptor.TYPE_ENUM and isinstance(item, str):
                    _pb_value.append(_string_to_enum(field, item))
                else:
                    _pb_value.append(item)
            continue

        if field.type == FieldDescriptor.TYPE_MESSAGE:
            _dict_to_protobuf(_pb_value, input_value, type_callable_map, strict)
            continue

        if field.type in type_callable_map:
            input_value = type_callable_map[field.type](input_value)

        if field.is_extension:
            _pb.Extensions[field] = input_value
            continue

        if field.type == FieldDescriptor.TYPE_ENUM and isinstance(input_value, str):
            input_value = _string_to_enum(field, input_value)

        setattr(_pb, field.name, input_value)

    return _pb


def _string_to_enum(field, input_value):
    enum_dict = field.enum_type.values_by_name
    try:
        input_value = enum_dict[input_value].number
    except KeyError:
        raise KeyError(
            "`%s` is not a valid value for field `%s`" % (input_value, field.name)
        ) from KeyError
    return input_value

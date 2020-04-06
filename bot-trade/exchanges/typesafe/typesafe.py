BASIC_DATA_TYPE = (int, str, float)
BASIC_DATA_TYPE_BOOL = bool

TYPE_BASIC = "type_basic"
TYPE_BOOL = "type_bool"
TYPE_OBJECT = "type_object"
TYPE_LIST = "type_list"
TYPE_DICT = "type_dict"
TYPE_UNDEFINED = "type_undefined"


class TypeCheck:
    @staticmethod
    def is_list(obj):
        return type(obj) == list and isinstance(obj, list)

    @staticmethod
    def is_dict(obj):
        return type(obj) == dict and isinstance(obj, dict)

    @staticmethod
    def is_object(obj):
        return isinstance(obj, object)

    @staticmethod
    def is_basic(obj):
        return isinstance(obj, BASIC_DATA_TYPE)

    @staticmethod
    def is_bool(obj):
        return isinstance(obj, bool)

    @staticmethod
    def get_obj_type(obj):
        if TypeCheck.is_basic(obj):
            return TYPE_BASIC
        elif TypeCheck.is_bool(obj):
            return TYPE_BOOL
        elif TypeCheck.is_list(obj):
            return TYPE_LIST
        elif TypeCheck.is_dict(obj):
            return TYPE_DICT
        elif TypeCheck.is_object(obj):
            return TYPE_OBJECT
        else:
            return TYPE_UNDEFINED


if __name__ == "__main__":
    pass

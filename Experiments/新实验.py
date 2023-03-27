class test:
    pass


class_dict = {key: var for key, var in locals().items() if isinstance(var, type)}
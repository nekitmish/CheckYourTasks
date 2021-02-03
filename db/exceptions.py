class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBEmployeeExistsException(Exception):
    pass


class DBEmployeeNotExistsException(Exception):
    pass


class DBMessageNotExistsException(Exception):
    pass

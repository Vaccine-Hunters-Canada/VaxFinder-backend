class DBException(Exception):
    pass

class InvalidIDException(DBException):
    pass

def add_location(name, region, url, number, org):
    #TODO: Add location to database, return id...
    return 1
from pyCode.setupConnection import conn
db = conn['admin']

def update():
    #while True:
    #    rs_status = db.command({'replSetGetStatus': 1})
    #    print(rs_status)
    rs_status = db.command({'replSetGetStatus': 1})
    return rs_status
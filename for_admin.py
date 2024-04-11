from src.database import Database

db = Database()
# TODO need to check if the courses are available
db.enrollment.populate("douglas", "098.765.432.12", "adm")
db.enrollment.populate("maria", "028.745.462.18", "mat")
db.enrollment.populate("joana", "038.745.452.19", "port")
db.enrollment.populate("any", "123.456.789-10", "any")

db.course.populate("adm")
db.course.populate("mat")
db.course.populate("port")
db.course.populate("any")
db.course.populate("noise")

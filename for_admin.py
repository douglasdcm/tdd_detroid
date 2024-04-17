from src.database import Database

db = Database()
# TODO need to check if the courses are available
db.enrollment.populate("douglas", "098.765.432.12", "mat")
db.enrollment.populate("maria", "028.745.462.18", "mat")
db.enrollment.populate("aline", "028.745.462.18", "adm")
db.enrollment.populate("joana", "038.745.452.19", "port")
db.enrollment.populate(
    "any", "123.456.789-10", "any"
)  # 290f2113c2e6579c8bb6ec395ea56572

db.course.populate("adm")
db.course.populate("mat")
db.course.populate("port")
db.course.populate("any")
db.course.populate("noise")
db.course.populate("deact")
db.course.populate("act")

db.subject.populate("any", "any1")  # e4c858cd917f518194c9d93c9d13def8
db.subject.populate("any", "any2")  # 283631d2292c54879b9aa72e27a1b4ff
db.subject.populate("any", "any3")  # 0eaaeb1a39ed5d04a62b31cd951f34ce
db.subject.populate("any", "any4", 0)  # ef15a071407953bd858cfca59ad99056
db.subject.populate("adm", "management")
db.subject.populate("mat", "calculus")
db.subject.populate("mat", "algebra")
db.subject.populate("mat", "analysis")
db.subject.populate("mat", "geometry")

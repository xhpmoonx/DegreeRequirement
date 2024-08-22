from Db.database import Base
from sqlalchemy import Column,String,Integer,Float,Boolean,REAL,JSON

class CourseSet(Base):
    __tablename__ = "CourseSet"

    id= Column (Integer,primary_key=True)
    name= Column (String)
    description=Column(String)
    credit_hours= Column (Float)
    course_reqs=Column(JSON)
    #course_reqs=Column(List[Tuple[Course,Grade]])
    course_catalog=Column(JSON)
    #course_catalog=Column(Dict{Integer,Course})
    prefix_regex=Column(String)
    num_regex=Column(String)
    min_grade=Column(Integer)
    double_count=Column(Boolean)

    def __init__(self, id:int,  name: str,description:str, credit_hours:float, course_reqs:list,
                 course_catalog: dict, prefix_regex: str, num_regex:str ,min_grade: str, double_count: bool):
        self.id= id
        self.name=name
        self.description=description
        self.credit_hours=credit_hours
        self.course_reqs=course_reqs
        self.course_catalog=course_catalog
        self.prefix_regex=prefix_regex
        self.num_regex=num_regex
        self.min_grade=min_grade
        self.double_count=double_count

class RequirementSet(Base):
    __tablename__ = "RequirementSet"

    id= Column(Integer,primary_key=True,default=True)
    name= Column(String)
    credit_hours= Column(REAL)
    description=Column(String)
    requirements=Column(JSON)
    satisfy=Column(Integer)

    def __init__(self,id:int, name: str, credit_hours:float,
                 description:str,requirements:list,satisfy:int):
        self.id=id
        self.name=name
        self.credit_hours=credit_hours
        self.description=description
        self.requirements=requirements
        self.satisfy=satisfy

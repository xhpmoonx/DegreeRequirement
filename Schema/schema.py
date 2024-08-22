from pydantic import BaseModel,Field,root_validator
from typing import List,Tuple,Dict,Union,Optional,Any
from fastapi import HTTPException
import re
from enum import Enum
class Grade(str, Enum):
    A_plus = "A➕"
    A = "A"
    A_minus = "A➖"
    B_plus = "B➕"
    B = "B"
    B_minus = "B➖"
    C_plus = "C➕"
    C = "C"
    C_minus = "C➖"
    D_plus = "D➕"
    D = "D"
    D_minus = "D➖"
    P = "P"
    F = "F"
    I = "I"
    WP = "WP"
    W = "W"
    WF = "WF"
def l_to_g(letter_grade: str) -> int:
    grades = {
        "A➕": 13, "A": 12, "A➖": 11,
        "B➕": 10, "B": 9, "B➖": 8,
        "C➕": 7, "C": 6, "C➖": 5,
        "D➕": 4, "D": 3, "D➖": 2,
        "P": 0, "F": 0, "I": 0,
        "WP": 0, "W": 0, "WF": 0
    }
    try:
        return grades[letter_grade]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Letter grade {letter_grade} is not supported")


def g_to_l(int_grade: int) -> str:
    letters = {
        13: "A➕", 12: "A", 11: "A➖",
        10: "B➕", 9: "B", 8: "B➖",
        7: "C➕", 6: "C", 5: "C➖",
        4: "D➕", 3: "D", 2: "D➖",
        0: "F"
    }
    try:
        return letters[int_grade]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Grade value {int_grade} is not supported")


class LearningOutcome(BaseModel):
    id: Optional[int] = None
    vertex_id: Dict[int, int] = {}
    name: str
    description: str
    hours: int = 0
    requisites: Dict[int, str] = {}
    affinity: Dict[int, float] = {}
    metrics: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}

class Course(BaseModel):
    id: Optional[int] = None
    name:str
    credit_hours: float
    prefix: Optional[str] =""
    num: Optional[str] =""
    institution:Optional[str] =""
    college: Optional[str] =""
    department: Optional[str] =""
    cross_listed: Optional[List['Course']]=[]
    canonical_name: Optional[str] =""
    passrate: Optional[float] = 0.5
    requisites: Optional[Dict[int, str]] = {}
    learning_outcomes: Optional[List['LearningOutcome']] = []
    metrics: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}

class CourseCatalog(BaseModel):
    id: Optional[int] = None
    name: str
    institution: str
    date_range: Optional[Tuple[str, str]] = ()
    catalog: Dict[int, Course] = {}

class AbstractRequirement(BaseModel):
    pass

class CourseSet(AbstractRequirement):
    #id: Optional[int] = None
    name: str
    credit_hours: float
    description: Optional[str]=""
    course_reqs: List[Tuple[Course, Grade]] = []
    course_catalog: Optional[CourseCatalog]= None
    prefix_regex: str = Field(default=r".^", alias="prefix_regex")
    num_regex: str = Field(default=r".^", alias="num_regex")
    min_grade: Grade = Field(default=Grade.D)
    double_count: bool = False
    class Config:
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def validate_and_compile_regex(cls, values):
        values['prefix_regex_compiled'] = re.compile(values.get('prefix_regex', r".^"))
        values['num_regex_compiled'] = re.compile(values.get('num_regex', r".^"))
        return values

    def __post_init__(self):
        # This method will be called after initialization
        self.search_course_catalog()
        self.check_credit_hours()

    def search_course_catalog(self):
        for course_id, course in self.course_catalog.catalog.items():
            if self.prefix_regex_compiled.search(course.prefix) and self.num_regex_compiled.search(course.num):
                self.course_reqs.append((course, self.min_grade))

    def check_credit_hours(self):
        total_hours = sum(course.credit_hours for course, _ in self.course_reqs)
        if total_hours < self.credit_hours:
            print(f"Warning: Course set {self.name} is improperly specified. Required: {self.credit_hours} credits, Available: {total_hours} credits.")

class RequirementSet(AbstractRequirement):
    #id: Optional[int] = None
    name: str
    description: str = ""
    credit_hours: float
    requirements: List[Union['CourseSet', 'RequirementSet']]
    satisfy: int = 0
    class Config:
        arbitrary_types_allowed = True
    def __init__(self,**data):
        super().__init__(**data)
        self.satisfy_validity()

    def satisfy_validity(self):
        if self.satisfy<0:
            raise ValueError(f"WARNING: RequirementSet {self.name},satisfy cannot be a negative number")
        if self.satisfy==0:
            self.satisfy=len(self.requirements)
        elif self.satisfy > len(self.requirements):
            raise ValueError(f"satisfy cannot be greater than the number of available requirements ({len(self.requirements)})")
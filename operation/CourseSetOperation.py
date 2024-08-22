from sqlalchemy.ext.asyncio import AsyncSession
from Db.models import CourseSet
import hashlib
from fastapi.encoders import jsonable_encoder

class Operation():
    def __init__(self, db_session: AsyncSession)-> None:
        self.db_session = db_session
    async def create(self, data:CourseSet ):
        CourseSet_set_data = jsonable_encoder(data)
        unique_string = f"{CourseSet_set_data['name']}{CourseSet_set_data['description']}{CourseSet_set_data['credit_hours']}"
        unique_id = int(hashlib.sha256(unique_string.encode()).hexdigest(), 16) % (10 ** 8)

        createCourseSet= CourseSet(
            id=unique_id,
            name=CourseSet_set_data['name'],
            credit_hours=CourseSet_set_data['credit_hours'],
            description=CourseSet_set_data['description'],
            course_reqs=CourseSet_set_data['course_reqs'],
            course_catalog=CourseSet_set_data['course_catalog'],
            prefix_regex=CourseSet_set_data['prefix_regex'],
            num_regex=CourseSet_set_data['num_regex'],
            min_grade=CourseSet_set_data['min_grade'],
            double_count=CourseSet_set_data['double_count']

        )

        async with self.db_session as session:
            session.add(createCourseSet)
            await session.commit()
        return createCourseSet




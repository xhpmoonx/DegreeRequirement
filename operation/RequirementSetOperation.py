import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from Db.models import RequirementSet
from fastapi.encoders import jsonable_encoder
from Db.models import CourseSet
from Schema.schema import AbstractRequirement
from typing import List, Callable, Union
from itertools import combinations
from fastapi import HTTPException


class Operation():
    def __init__(self, db_session: AsyncSession)-> None:
        self.db_session = db_session

    async def create(self, data:RequirementSet ):
        requirement_set_data = jsonable_encoder(data)
        unique_string = f"{requirement_set_data['name']}{requirement_set_data['description']}{requirement_set_data['credit_hours']}"
        unique_id = int(hashlib.sha256(unique_string.encode()).hexdigest(), 16) % (10 ** 8)

        createRequirementSet = RequirementSet(
            id=unique_id,
            name=requirement_set_data['name'],
            credit_hours=requirement_set_data['credit_hours'],
            description=requirement_set_data['description'],
            requirements=requirement_set_data['requirements'],
            satisfy=requirement_set_data['satisfy']
        )
        self.satisfy = requirement_set_data['satisfy'] if requirement_set_data['satisfy'] >= 0 and requirement_set_data[
            'satisfy'] <= len(requirement_set_data['requirements']) else len(requirement_set_data['requirements'])

        async with self.db_session as session:
            session.add(createRequirementSet)
            await session.commit()
        return createRequirementSet
    async def validate_requirement_set(self, data:RequirementSet ):
        async def preorder_traversal(root:AbstractRequirement,visit: Callable[[AbstractRequirement],None]=lambda x:None) -> List[AbstractRequirement]:
            #Preorder
            """
            Perform a preorder traversal of the requirement tree.

            Parameters:
            - root: The root of the requirement tree.
            - visit: A function to call on each node (default does nothing).

            Returns:
            - A list of requirements in preorder.
            """
            #TODO:  root.requirements
            if isinstance(root, CourseSet) or not root.requirements:
                return [root]

            stack = [root]
            visit_order = []

            while stack:
                req = stack.pop()
                visit(req)
                visit_order.append(req)
                if isinstance(req, RequirementSet):  # course-set requirements have no children
                    stack.extend(reversed(req.requirements))

            return visit_order


        async def nonunique(x: List[AbstractRequirement]) -> List[AbstractRequirement]:
            uniqueset = set()
            duplicateset = set()
            for item in x:
                if item in uniqueset:
                    duplicateset.add(item)
                else:
                    uniqueset.add(item)
            return list(duplicateset)

        async def is_valid(root:AbstractRequirement) ->bool:
            validity=True
            error_msgs=[]
            reqs=preorder_traversal(root)
            dups=nonunique(reqs)

            if dups:
                validity=False
                error_msgs.append(f"RequirementSet: {root.name} is not a tree, it contains duplicate requirements:\n")
                for d in dups:
                    error_msgs.append(f"\t {d.name}\n")

            for r in reqs:
                credit_total=0
                if isinstance(r,CourseSet):
                    for course,_ in r.course_reqs:
                        credit_total+=course.credit_hours
                    if r.credit_hours>credit_total:
                        validity=False
                        error_msgs.append(f"\t {d.name}\n")

                elif isinstance(r, RequirementSet):
                    if r.satisfy == 0:
                        validity = False
                        error_msgs.append(f"RequirementSet: {r.name} is unsatisfiable, cannot satisfy 0 requirements\n")

                    elif r.satisfy > len(r.requirements):
                        validity = False
                        error_msgs.append(f"RequirementSet: {r.name} is unsatisfiable, satisfy variable cannot be greater than the number of available requirements\n")

                    else:
                        credit_ary = [child.credit_hours for child in r.requirements]
                        max_credits = 0
                        for comb in combinations(credit_ary, r.satisfy):
                            max_credits = max(max_credits, sum(comb))

                        if r.credit_hours > max_credits:
                            validity = False
                            error_msgs.append(f"RequirementSet: {r.name} is unsatisfiable,\n\t {r.credit_hours} credits are required from sub-requirements that can provide at most {max_credits} credit hours.\n")

            if not validity:
                raise HTTPException(status_code=400, detail="".join(error_msgs))
            return validity

        is_valid(data)


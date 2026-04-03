from typing import List

from .User import User


class Request:
    def __init__(self, req_id: int, user: User, desc):
        self.req_id = req_id
        self.user = user
        self.desc = desc


class TeamRequest(Request):
    def __init__(self, req_id: int, user: User, desc: str, user_roles: List[str], user_lns: List[str]):
        super().__init__(req_id, user, desc)
        self.user_roles = user_roles
        self.user_lns = user_lns


class CoteamateRequest(Request):
    def __init__(self, req_id: int, user: User, desc: str, nd_roles: List[str], nd_lns: List[str]):
        super().__init__(req_id, user, desc)
        self.user_roles = nd_roles
        self.user_lns = nd_lns
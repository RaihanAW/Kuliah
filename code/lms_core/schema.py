from ninja import Schema
from typing import Optional
from datetime import datetime

from django.contrib.auth.models import User

class UserOut(Schema):
    id: int
    email: str
    first_name: str
    last_name: str


class CourseSchemaOut(Schema):
    id: int
    name: str
    description: str
    price: int
    image : Optional[str]
    teacher: UserOut
    created_at: datetime
    updated_at: datetime

class CourseMemberOut(Schema):
    id: int 
    course_id: CourseSchemaOut
    user_id: UserOut
    roles: str
    # created_at: datetime


class CourseSchemaIn(Schema):
    name: str
    description: str
    price: int


class CourseContentMini(Schema):
    id: int
    name: str
    description: str
    course_id: CourseSchemaOut
    created_at: datetime
    updated_at: datetime


class CourseContentFull(Schema):
    id: int
    name: str
    description: str
    video_url: Optional[str]
    file_attachment: Optional[str]
    course_id: CourseSchemaOut
    created_at: datetime
    updated_at: datetime

class CourseCommentOut(Schema):
    id: int
    content_id: CourseContentMini
    member_id: CourseMemberOut
    comment: str
    created_at: datetime
    updated_at: datetime

class CourseCommentIn(Schema):
    comment: str

class UserProfileOut(Schema):
    phone: Optional[str]
    bio: Optional[str]
    photo: Optional[str]

class UserFullProfile(Schema):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    bio: Optional[str]
    photo: Optional[str]
    courses_joined: list[CourseSchemaOut]
    courses_created: list[CourseSchemaOut]

class EditProfileIn(Schema):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    bio: Optional[str]

class AnnouncementIn(Schema):
    title: str
    message: str
    show_at: datetime

class AnnouncementOut(Schema):
    id: int
    title: str
    message: str
    show_at: datetime
    created_by: UserOut
    created_at: datetime

class BookmarkOut(Schema):
    id: int
    content: CourseContentMini
    student: UserOut

class EnrollIn(Schema):
    course_id: int
    student_ids: list[int]
from ninja import NinjaAPI, UploadedFile, File, Form
from ninja.responses import Response
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja.pagination import paginate, PageNumberPagination
from lms_core.models import *
from lms_core.schema import *
from django.db.models import Count
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

apiv1 = NinjaAPI()
apiv1.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@apiv1.post("/register")
def register_user(request, username: str = Form(...), password: str = Form(...),
                  email: str = Form(...), first_name: str = Form(...), last_name: str = Form(...)):
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)
    user = User.objects.create_user(username=username, password=password,
                                    email=email, first_name=first_name, last_name=last_name)
    UserProfile.objects.create(user=user)
    return {"message": "User registered successfully"}

@apiv1.post("/course/batch-enroll", auth=apiAuth)
def batch_enroll(request, payload: EnrollIn):
    course = get_object_or_404(Course, id=payload.course_id)
    if course.teacher != request.user:
        return Response({"error": "Unauthorized"}, status=403)
    count = 0
    for uid in payload.student_ids:
        if not CourseMember.objects.filter(course_id=course, user_id=uid).exists():
            CourseMember.objects.create(course_id=course, user_id_id=uid, roles='std')
            count += 1
    return {"enrolled": count}

@apiv1.get("/user/dashboard", auth=apiAuth)
def user_dashboard(request):
    user = request.user
    total_joined = CourseMember.objects.filter(user_id=user).count()
    total_created = Course.objects.filter(teacher=user).count()
    total_comments = Comment.objects.filter(member_id__user_id=user).count()
    return {
        "courses_joined": total_joined,
        "courses_created": total_created,
        "comments_written": total_comments,
    }

@apiv1.get("/course/{course_id}/analytics", auth=apiAuth)
def course_analytics(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher != request.user:
        return Response({"error": "Unauthorized"}, status=403)
    total_member = CourseMember.objects.filter(course_id=course).count()
    total_content = CourseContent.objects.filter(course_id=course).count()
    total_comments = Comment.objects.filter(content_id__course_id=course).count()
    return {
        "total_member": total_member,
        "total_content": total_content,
        "total_comments": total_comments,
    }

@apiv1.get("/user/{user_id}/profile", response=UserFullProfile)
def show_profile(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    profile = UserProfile.objects.get(user=user)
    courses_joined = CourseMember.objects.filter(user_id=user).values_list('course_id', flat=True)
    joined = Course.objects.filter(id__in=courses_joined)
    created = Course.objects.filter(teacher=user)
    return UserFullProfile(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=profile.phone,
        bio=profile.bio,
        photo=profile.photo.url if profile.photo else None,
        courses_joined=joined,
        courses_created=created
    )

@apiv1.put("/user/edit-profile", auth=apiAuth)
def edit_profile(request, data: EditProfileIn):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    for attr, value in data.dict().items():
        if value is not None:
            if hasattr(user, attr):
                setattr(user, attr, value)
            elif hasattr(profile, attr):
                setattr(profile, attr, value)
    user.save()
    profile.save()
    return {"message": "Profile updated"}

@apiv1.post("/course/{course_id}/announcement", auth=apiAuth)
def create_announcement(request, course_id: int, data: AnnouncementIn):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    a = Announcement.objects.create(course=course, created_by=request.user, **data.dict())
    return {"id": a.id}

@apiv1.get("/course/{course_id}/announcement", response=list[AnnouncementOut], auth=apiAuth)
def list_announcements(request, course_id: int):
    announcements = Announcement.objects.filter(course_id=course_id)
    return announcements

@apiv1.put("/announcement/{announcement_id}", auth=apiAuth)
def update_announcement(request, announcement_id: int, data: AnnouncementIn):
    a = get_object_or_404(Announcement, id=announcement_id, created_by=request.user)
    for attr, val in data.dict().items():
        setattr(a, attr, val)
    a.save()
    return {"message": "Announcement updated"}

@apiv1.delete("/announcement/{announcement_id}", auth=apiAuth)
def delete_announcement(request, announcement_id: int):
    a = get_object_or_404(Announcement, id=announcement_id, created_by=request.user)
    a.delete()
    return {"message": "Announcement deleted"}

@apiv1.post("/bookmark/{content_id}", auth=apiAuth)
def add_bookmark(request, content_id: int):
    if not CourseContent.objects.filter(id=content_id).exists():
        return Response({"error": "Content not found"}, status=404)
    Bookmark.objects.get_or_create(student=request.user, content_id=content_id)
    return {"message": "Bookmarked"}

@apiv1.get("/bookmark", response=list[BookmarkOut], auth=apiAuth)
def get_bookmarks(request):
    bookmarks = Bookmark.objects.filter(student=request.user)
    return bookmarks

@apiv1.delete("/bookmark/{content_id}", auth=apiAuth)
def delete_bookmark(request, content_id: int):
    Bookmark.objects.filter(student=request.user, content_id=content_id).delete()
    return {"message": "Bookmark removed"}

@apiv1.put("/content/{content_id}/publish", auth=apiAuth)
def update_publish(request, content_id: int, publish: bool):
    content = get_object_or_404(CourseContent, id=content_id)
    if content.course_id.teacher != request.user:
        return Response({"error": "Unauthorized"}, status=403)
    content.is_published = publish
    content.save()
    return {"message": "Content updated"}

@apiv1.put("/content/{content_id}/edit", auth=apiAuth)
def edit_content(request, content_id: int, data: CourseContentFull):
    content = get_object_or_404(CourseContent, id=content_id)
    if content.course_id.teacher != request.user:
        return Response({"error": "Unauthorized"}, status=403)
    for attr, val in data.dict().items():
        if val is not None:
            setattr(content, attr, val)
    content.save()
    return {"message": "Content updated"}
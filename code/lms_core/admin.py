from django.contrib import admin
from .models import (
    Course, CourseMember, CourseContent, Comment,
    UserProfile, Announcement, Bookmark
)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'teacher')

@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'user_id', 'roles', 'created_at')
    list_filter = ('roles',)

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_id', 'is_published', 'created_at')
    list_filter = ('course_id', 'is_published')
    search_fields = ('name', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_id', 'member_id', 'created_at')
    search_fields = ('comment',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'bio')
    search_fields = ('user__username', 'phone', 'bio')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'show_at', 'created_by', 'created_at')
    list_filter = ('show_at', 'course')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'content', 'created_at')
    search_fields = ('student__username', 'content__name')
from django.utils.html import mark_safe
from django.contrib import admin
from .models import Student, SignupRequest

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'is_approved', 'joined_at')
    list_filter = ('is_approved',)
    actions = ['approve_students']

    def approve_students(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} student(s) approved.")
    approve_students.short_description = "Approve selected students"

@admin.register(SignupRequest)
class SignupRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'phone_number', 'is_approved', 'joined_at')
    list_filter = ('is_approved',)
    actions = ['approve_signup_requests']
    readonly_fields = ('student_id_image_link', 'joined_at')
    fields = ('email', 'first_name', 'phone_number', 'student_id_image_link', 'is_approved', 'joined_at')

    def student_id_image_link(self, obj):
        if obj.student_id_image:
            return mark_safe(f'<a href="{obj.student_id_image.url}" target="_blank">View ID Image</a>')
        return "No ID image"
    student_id_image_link.short_description = "Student ID Image"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_approved=False)

    def approve_signup_requests(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} signup request(s) approved.")
    approve_signup_requests.short_description = "Approve selected signup requests"

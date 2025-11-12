from django.utils.html import mark_safe
from django.contrib import admin
from .models import Student, SignupRequest, WalletTransaction

@admin.register(Student)#student model to view student details
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'is_approved', 'joined_at')#feilds to display in list view
    list_filter = ('is_approved',)#filter option
    actions = ['approve_students']#available action

    def approve_students(self, request, queryset):#method for approving students
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} student(s) approved.")
    approve_students.short_description = "Approve selected students"

@admin.register(SignupRequest)#student proxy model for authorizing signup requests
class SignupRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'phone_number', 'is_approved', 'joined_at')#feilds to display in list view
    list_filter = ('is_approved',)#filter option
    actions = ['approve_signup_requests']#custom action
    readonly_fields = ('student_id_image_link', 'joined_at')#cant be edited in admin 
    fields = ('email', 'first_name', 'phone_number', 'student_id_image_link', 'is_approved', 'joined_at')#fields to shown in single signup request

    def student_id_image_link(self, obj):#method for clickable link for id image
        if obj.student_id_image:
            return mark_safe(f'<a href="{obj.student_id_image.url}" target="_blank">View ID Image</a>')
        return "No ID image"
    student_id_image_link.short_description = "Student ID Image"

    def get_queryset(self, request):#method to make this view only for pending signup requests
        qs = super().get_queryset(request)
        return qs.filter(is_approved=False)

    def approve_signup_requests(self, request, queryset):#method for custom action
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} signup request(s) approved.")
    approve_signup_requests.short_description = "Approve selected signup requests"

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'timestamp', 'description')  
    list_filter = ('user',)

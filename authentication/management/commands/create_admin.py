"""
Management command to create a superuser automatically
Usage: python manage.py create_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a superuser automatically with environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from environment variables or use defaults
        email = os.environ.get('ADMIN_EMAIL', 'admin@swapex.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        
        # Check if superuser already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Admin user with email {email} already exists'))
            return
        
        # Create superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {email}'))
            self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
            self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))

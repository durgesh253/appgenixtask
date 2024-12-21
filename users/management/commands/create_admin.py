from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Create a default admin user if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():  # generate a random password
            admin = User.objects.create_superuser(
                email='admin@example.com',  # set a default admin email
                password="adminpassword",
                username='admin'
            )
            self.stdout.write(self.style.SUCCESS(f"Admin created with email: admin@example.com"))
        else:
            self.stdout.write(self.style.SUCCESS("Admin already exists"))

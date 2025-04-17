from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    # Create "Admin" and "User" groups
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='User')

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_appointment_family_name_alter_appointment_name'),  # Replace with the previous migration file name
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
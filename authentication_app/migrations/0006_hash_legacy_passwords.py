from django.contrib.auth.hashers import identify_hasher, make_password
from django.db import migrations


def hash_legacy_passwords(apps, schema_editor):
    User = apps.get_model("authentication_app", "User")
    database = schema_editor.connection.alias

    users = User.objects.using(database).only("pk", "password").iterator()
    for user in users:
        try:
            identify_hasher(user.password)
        except ValueError:
            user.password = make_password(user.password)
            user.save(using=database, update_fields=["password"])


class Migration(migrations.Migration):

    dependencies = [
        ("authentication_app", "0005_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.RunPython(
            hash_legacy_passwords,
            migrations.RunPython.noop,
        ),
    ]

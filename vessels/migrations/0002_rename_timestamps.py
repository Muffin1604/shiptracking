import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vessels", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vesselinfo",
            old_name="fetched_at",
            new_name="created_at",
        ),
        migrations.AlterField(
            model_name="vesselinfo",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name="vesselinfo",
            name="updated_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="vesselinfo",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RenameField(
            model_name="vessellocation",
            old_name="recorded_at",
            new_name="created_at",
        ),
        migrations.AlterModelOptions(
            name="vessellocation",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RenameField(
            model_name="vesselweather",
            old_name="recorded_at",
            new_name="created_at",
        ),
        migrations.AlterModelOptions(
            name="vesselweather",
            options={
                "ordering": ["-created_at"],
                "verbose_name_plural": "vessel weather",
            },
        ),
    ]

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('newsbot', '0002_dictentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleexample',
            name='bias_class',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]

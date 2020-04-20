from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('newsbot', '0003_articleexample_bias_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleexample',
            name='quality_class',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]

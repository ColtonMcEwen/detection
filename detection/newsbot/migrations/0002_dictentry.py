from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('newsbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DictEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canonWord', models.TextField()),
            ],
        ),
    ]

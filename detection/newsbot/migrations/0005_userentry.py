from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('newsbot', '0004_articleexample_quality_class'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entryURL', models.URLField(verbose_name='URL of news article')),
            ],
        ),
    ]

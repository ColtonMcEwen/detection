from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleExample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_text', models.TextField()),
                ('bias_score', models.FloatField()),
                ('quality_score', models.FloatField()),
                ('origin_url', models.TextField()),
                ('origin_source', models.TextField()),
            ],
        ),
    ]

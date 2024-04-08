# Generated by Django 5.0.1 on 2024-04-07 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picApp', '0003_missingchild_gender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoundPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=100)),
                ('image', models.ImageField(upload_to='found_person')),
                ('place_found', models.CharField(max_length=100)),
                ('date_found', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O', max_length=1)),
                ('time_found', models.TimeField()),
                ('samaritan_name', models.CharField(max_length=100)),
                ('samaritan_contact', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='missingchild',
            name='age',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
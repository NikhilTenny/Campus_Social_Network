# Generated by Django 4.0 on 2022-02-16 15:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_delete_student_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bio', models.CharField(max_length=400)),
                ('Profile_pic', models.BinaryField()),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^(\\+91[\\-\\s]?)?[0]?(91)?[789]\\d{9}$')])),
                ('Designation', models.CharField(max_length=50)),
                ('Address', models.CharField(max_length=300)),
                ('Friends', models.CharField(max_length=50)),
                ('Posts', models.CharField(max_length=50)),
                ('Dept', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.department')),
                ('User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.customeusers')),
                ('Yr', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.year')),
            ],
        ),
    ]
# Generated by Django 4.1a1 on 2022-12-22 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('salary', models.IntegerField()),
                ('jobType', models.CharField(choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Contract', 'Contract'), ('Internship', 'Internship'), ('Remote', 'Remote')], default='Full Time', max_length=20)),
                ('jobLevel', models.CharField(choices=[('Entry Level', 'Entry Level'), ('Mid Level', 'Mid Level'), ('Senior Level', 'Senior Level')], default='Mid Level', max_length=20)),
                ('applicationDeadline', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.companyprofile')),
            ],
        ),
    ]
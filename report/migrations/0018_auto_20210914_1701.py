# Generated by Django 3.2.6 on 2021-09-14 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0017_auto_20210914_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionrankstatus',
            name='section_ranking',
            field=models.ManyToManyField(blank=True, to='report.SectionRankStatus'),
        ),
        migrations.AddField(
            model_name='termrankingaccount',
            name='section_ranking',
            field=models.ManyToManyField(blank=True, to='report.SectionRankStatus'),
        ),
    ]

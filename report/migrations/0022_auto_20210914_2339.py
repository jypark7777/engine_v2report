# Generated by Django 3.2.6 on 2021-09-14 23:39

from django.db import migrations, models
import django.db.models.deletion
import report.models.rank


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0021_componentrankstatus_section_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='termrankingaccount',
            name='section_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='report.categorysection'),
        ),
        migrations.AddField(
            model_name='termrankingaccount',
            name='section_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='report.countrysection'),
        ),
        migrations.AddField(
            model_name='termrankingaccount',
            name='section_follower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='report.followersection'),
        ),
        migrations.AddField(
            model_name='termrankingaccount',
            name='section_platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='report.platformsection'),
        ),
        migrations.AlterField(
            model_name='termrankingaccount',
            name='define_date',
            field=models.DateField(default=report.models.rank.get_current_definedate, verbose_name='기준날짜 (매주 월요일)'),
        ),
        migrations.AlterUniqueTogether(
            name='termrankingaccount',
            unique_together={('ig_userinfo', 'tk_userinfo', 'yt_channelinfo', 'section_follower', 'section_category', 'section_country', 'define_date')},
        ),
    ]

# Generated by Django 3.2.6 on 2021-09-14 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0019_auto_20210914_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audienceindicator',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='audienceindicator',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='audienceindicator',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='audienceindicator',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='audienceindicator',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='audienceindicator',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='audiencequality',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='audiencequality',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='audiencequality',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='audiencequality',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='audiencequality',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='audiencequality',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicsage',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='demographicsage',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicsage',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='demographicsage',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicsage',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='demographicsage',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicsgender',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='demographicsgender',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicsgender',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='demographicsgender',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicsgender',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='demographicsgender',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicslanguages',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='demographicslanguages',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicslanguages',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='demographicslanguages',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='demographicslanguages',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='demographicslanguages',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='featuringscore',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='featuringscore',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='featuringscore',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='featuringscore',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='featuringscore',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='featuringscore',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='reachscore',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='reachscore',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='reachscore',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='reachscore',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='reachscore',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='reachscore',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='realinfluencescore',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='realinfluencescore',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='realinfluencescore',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='realinfluencescore',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='realinfluencescore',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='realinfluencescore',
            name='section_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='trend',
            name='estimate_ranking',
        ),
        migrations.RemoveField(
            model_name='trend',
            name='estimate_ranking_rate',
        ),
        migrations.RemoveField(
            model_name='trend',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='trend',
            name='ranking_rate',
        ),
        migrations.RemoveField(
            model_name='trend',
            name='section_ranking',
        ),
        migrations.RemoveField(
            model_name='trend',
            name='section_ranking_rate',
        ),
        migrations.CreateModel(
            name='ComponentRankStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)')),
                ('ranking_rate', models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)')),
                ('section_ranking', models.BigIntegerField(blank=True, null=True, verbose_name='섹션(팔로워,카테고리,국가) 디비 순위 (전체)')),
                ('section_ranking_rate', models.FloatField(blank=True, null=True, verbose_name='섹션(팔로워,카테고리,국가) 디비 순위 백분위 (상위)(전체)')),
                ('estimate_ranking', models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (플랫폼 전체 풀)(전체)')),
                ('estimate_ranking_rate', models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(플랫폼 전체 풀)(전체)')),
                ('section_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='report.categorysection')),
                ('section_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='report.countrysection')),
                ('section_follower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='report.followersection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='audienceindicator',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='audiencequality',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='demographicsage',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='demographicsgender',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='demographicslanguages',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='engagement',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='featuringscore',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='reachscore',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='realinfluencescore',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
        migrations.AddField(
            model_name='trend',
            name='rankstatuses',
            field=models.ManyToManyField(blank=True, to='report.ComponentRankStatus'),
        ),
    ]
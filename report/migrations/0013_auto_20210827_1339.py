# Generated by Django 3.2.6 on 2021-08-27 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0012_auto_20210827_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorysection',
            name='category_code',
            field=models.CharField(default='', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='countrysection',
            name='title',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='iguserinfo',
            name='section_shortcut',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='report.sectionshortcut'),
        ),
        migrations.AddField(
            model_name='platformsection',
            name='platform_code',
            field=models.CharField(choices=[('ig', 'Instagram'), ('yt', 'Youtube'), ('tk', 'Tiktok')], default='', max_length=5, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audienceindicator',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='audienceindicator',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='audienceindicator',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='audienceindicator',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='audiencequality',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='audiencequality',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='audiencequality',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='audiencequality',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicsage',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicsage',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicsage',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='demographicsage',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicsgender',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicsgender',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicsgender',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='demographicsgender',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicslanguages',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicslanguages',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='demographicslanguages',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='demographicslanguages',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='featuringscore',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='featuringscore',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='featuringscore',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='featuringscore',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='platformsection',
            name='type',
            field=models.IntegerField(choices=[(0, '인스타그램'), (1, '유튜브'), (2, '틱톡')], unique=True),
        ),
        migrations.AlterField(
            model_name='reachscore',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='reachscore',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='reachscore',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='reachscore',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='realinfluencescore',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='realinfluencescore',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='realinfluencescore',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='realinfluencescore',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='termrankingaccount',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='termrankingaccount',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='termrankingaccount',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='termrankingaccount',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
        migrations.AlterField(
            model_name='trend',
            name='estimate_ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='추정 순위 (인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='trend',
            name='estimate_ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='추정 순위 백분위(인스타 전체 풀)(전체)'),
        ),
        migrations.AlterField(
            model_name='trend',
            name='ranking',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='디비 순위 (전체)'),
        ),
        migrations.AlterField(
            model_name='trend',
            name='ranking_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='디비 순위 백분위 (상위)(전체)'),
        ),
    ]

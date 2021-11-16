# Generated by Django 3.2.6 on 2021-08-25 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_auto_20210825_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audienceindicator',
            name='accuracy',
            field=models.IntegerField(blank=True, choices=[(0, '매우낮음'), (1, '낮음'), (2, '중간'), (3, '높음'), (4, '매우 높음')], default=-1, verbose_name='정확도'),
        ),
        migrations.AlterField(
            model_name='audienceindicator',
            name='version',
            field=models.IntegerField(blank=True, choices=[(0, '도달수 기반 계산'), (1, '기존 피처링 엔진'), (2, '수집된 데이터 기반')], default=-1),
        ),
        migrations.AlterField(
            model_name='audienceindicator',
            name='version_calculate',
            field=models.IntegerField(blank=True, default=-1, verbose_name='적용된 계산식 버전'),
        ),
        migrations.AlterField(
            model_name='audiencequality',
            name='accuracy',
            field=models.IntegerField(blank=True, choices=[(0, '매우낮음'), (1, '낮음'), (2, '중간'), (3, '높음'), (4, '매우 높음')], default=-1, verbose_name='정확도'),
        ),
        migrations.AlterField(
            model_name='audiencequality',
            name='version',
            field=models.IntegerField(blank=True, choices=[(0, '도달수 기반 계산'), (1, '기존 피처링 엔진'), (2, '수집된 데이터 기반')], default=-1),
        ),
        migrations.AlterField(
            model_name='audiencequality',
            name='version_calculate',
            field=models.IntegerField(blank=True, default=-1, verbose_name='적용된 계산식 버전'),
        ),
        migrations.AlterField(
            model_name='demographicsage',
            name='accuracy',
            field=models.IntegerField(blank=True, choices=[(0, '매우낮음'), (1, '낮음'), (2, '중간'), (3, '높음'), (4, '매우 높음')], default=-1, verbose_name='정확도'),
        ),
        migrations.AlterField(
            model_name='demographicsage',
            name='version',
            field=models.IntegerField(blank=True, choices=[(0, '도달수 기반 계산'), (1, '기존 피처링 엔진'), (2, '수집된 데이터 기반')], default=-1),
        ),
        migrations.AlterField(
            model_name='demographicsage',
            name='version_calculate',
            field=models.IntegerField(blank=True, default=-1, verbose_name='적용된 계산식 버전'),
        ),
        migrations.AlterField(
            model_name='demographicsgender',
            name='accuracy',
            field=models.IntegerField(blank=True, choices=[(0, '매우낮음'), (1, '낮음'), (2, '중간'), (3, '높음'), (4, '매우 높음')], default=-1, verbose_name='정확도'),
        ),
        migrations.AlterField(
            model_name='demographicsgender',
            name='version',
            field=models.IntegerField(blank=True, choices=[(0, '도달수 기반 계산'), (1, '기존 피처링 엔진'), (2, '수집된 데이터 기반')], default=-1),
        ),
        migrations.AlterField(
            model_name='demographicsgender',
            name='version_calculate',
            field=models.IntegerField(blank=True, default=-1, verbose_name='적용된 계산식 버전'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='accuracy',
            field=models.IntegerField(blank=True, choices=[(0, '매우낮음'), (1, '낮음'), (2, '중간'), (3, '높음'), (4, '매우 높음')], default=-1, verbose_name='정확도'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='version',
            field=models.IntegerField(blank=True, choices=[(0, '도달수 기반 계산'), (1, '기존 피처링 엔진'), (2, '수집된 데이터 기반')], default=-1),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='version_calculate',
            field=models.IntegerField(blank=True, default=-1, verbose_name='적용된 계산식 버전'),
        ),
        migrations.AlterField(
            model_name='featuringscore',
            name='accuracy',
            field=models.IntegerField(blank=True, choices=[(0, '매우낮음'), (1, '낮음'), (2, '중간'), (3, '높음'), (4, '매우 높음')], default=-1, verbose_name='정확도'),
        ),
        migrations.AlterField(
            model_name='featuringscore',
            name='version',
            field=models.IntegerField(blank=True, choices=[(0, '도달수 기반 계산'), (1, '기존 피처링 엔진'), (2, '수집된 데이터 기반')], default=-1),
        ),
        migrations.AlterField(
            model_name='featuringscore',
            name='version_calculate',
            field=models.IntegerField(blank=True, default=-1, verbose_name='적용된 계산식 버전'),
        ),
        migrations.AlterField(
            model_name='reachscore',
            name='accuracy',
            field=models.IntegerField(blank=True, choices=[(0, '매우낮음'), (1, '낮음'), (2, '중간'), (3, '높음'), (4, '매우 높음')], default=-1, verbose_name='정확도'),
        ),
        migrations.AlterField(
            model_name='reachscore',
            name='version',
            field=models.IntegerField(blank=True, choices=[(0, '도달수 기반 계산'), (1, '기존 피처링 엔진'), (2, '수집된 데이터 기반')], default=-1),
        ),
        migrations.AlterField(
            model_name='reachscore',
            name='version_calculate',
            field=models.IntegerField(blank=True, default=-1, verbose_name='적용된 계산식 버전'),
        ),
        migrations.AlterField(
            model_name='realinfluencescore',
            name='accuracy',
            field=models.IntegerField(blank=True, choices=[(0, '매우낮음'), (1, '낮음'), (2, '중간'), (3, '높음'), (4, '매우 높음')], default=-1, verbose_name='정확도'),
        ),
        migrations.AlterField(
            model_name='realinfluencescore',
            name='version',
            field=models.IntegerField(blank=True, choices=[(0, '도달수 기반 계산'), (1, '기존 피처링 엔진'), (2, '수집된 데이터 기반')], default=-1),
        ),
        migrations.AlterField(
            model_name='realinfluencescore',
            name='version_calculate',
            field=models.IntegerField(blank=True, default=-1, verbose_name='적용된 계산식 버전'),
        ),
    ]

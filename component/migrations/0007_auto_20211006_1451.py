# Generated by Django 3.2.6 on 2021-10-06 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0006_alter_igstatisticscontent_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('desc', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='desc',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='component.category', verbose_name='분류 태그'),
        ),
        migrations.AddField(
            model_name='tag',
            name='attributes',
            field=models.ManyToManyField(to='component.Attribute', verbose_name='속성 태그'),
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-29 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='BasicOperation',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unnamed', max_length=10000)),
                ('operation_chain', models.ManyToManyField(to='wander_sample.basicoperation')),
            ],
        ),
        migrations.CreateModel(
            name='InformationPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unnamed', max_length=10000)),
                ('attribute_chain', models.ManyToManyField(to='wander_sample.attribute')),
            ],
        ),
        migrations.AddField(
            model_name='attribute',
            name='operation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wander_sample.operation'),
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together={('operation', 'result')},
        ),
    ]
# Generated by Django 2.2.5 on 2019-10-02 17:31

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20191002_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='country',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='address',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='member',
            name='city',
            field=models.CharField(default='Windsor', max_length=20),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.IntegerField(choices=[(0, 'Purchase'), (1, 'Borrow')], default=1)),
                ('order_date', models.DateField(default=datetime.datetime(2019, 10, 2, 17, 31, 32, 22225, tzinfo=utc))),
                ('books', models.ManyToManyField(to='myapp.Book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='myapp.Member')),
            ],
        ),
    ]

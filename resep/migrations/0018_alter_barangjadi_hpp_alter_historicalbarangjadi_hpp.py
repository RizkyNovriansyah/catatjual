# Generated by Django 4.2.9 on 2024-06-25 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resep', '0017_alter_resepbahanjadi_barang_jadi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangjadi',
            name='hpp',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='historicalbarangjadi',
            name='hpp',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

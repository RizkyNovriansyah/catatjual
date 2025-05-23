# Generated by Django 4.2.9 on 2024-06-25 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resep', '0016_historicalresepolahanjadi_jumlah_pemakaian_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resepbahanjadi',
            name='barang_jadi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resep_bahanjadi_jadi', to='resep.barangjadi'),
        ),
        migrations.AlterField(
            model_name='resepbahanjadi',
            name='master_bahan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resep_bahanjadi_bahan', to='resep.masterbahan'),
        ),
        migrations.AlterField(
            model_name='resepolahanjadi',
            name='bahan_olahan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resep_olahanjadi_olahan', to='resep.bahanolahan'),
        ),
        migrations.AlterField(
            model_name='resepolahanjadi',
            name='barang_jadi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resep_olahanjadi_jadi', to='resep.barangjadi'),
        ),
        migrations.CreateModel(
            name='ResepBahanOlahan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah_pemakaian', models.IntegerField(blank=True, default=0, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('bahan_olahan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resep_bahanolahan_olahan', to='resep.bahanolahan')),
                ('master_bahan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resep_bahanolahan_bahan', to='resep.masterbahan')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalResepBahanOlahan',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('jumlah_pemakaian', models.IntegerField(blank=True, default=0, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bahan_olahan', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='resep.bahanolahan')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('master_bahan', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='resep.masterbahan')),
            ],
            options={
                'verbose_name': 'historical resep bahan olahan',
                'verbose_name_plural': 'historical resep bahan olahans',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-25 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_remove_skreadings_bytes_received_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='skreadings',
            name='bytes_received',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skreadings',
            name='bytes_sent',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skreadings',
            name='connected_clients',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skreadings',
            name='messages_received',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skreadings',
            name='messages_sent',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skreadings',
            name='sub_count',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skreadings',
            name='total_clients',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
    ]

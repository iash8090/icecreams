# Generated by Django 4.2.1 on 2023-05-21 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_alter_icdetails_t_price_alter_icdetails_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icdetails',
            name='T_price',
        ),
    ]
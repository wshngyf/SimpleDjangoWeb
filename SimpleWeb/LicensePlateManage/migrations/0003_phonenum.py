# Generated by Django 2.0.5 on 2018-05-22 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LicensePlateManage', '0002_auto_20180422_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNum', models.CharField(max_length=13)),
                ('province', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=10)),
                ('createDate', models.DateField(null=True)),
            ],
        ),
    ]
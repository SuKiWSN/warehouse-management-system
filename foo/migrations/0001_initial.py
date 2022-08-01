# Generated by Django 2.2.4 on 2022-07-09 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=15)),
                ('addressDesc', models.CharField(max_length=50)),
                ('postCode', models.CharField(max_length=15)),
                ('tel', models.CharField(max_length=20)),
                ('createdBy', models.BigIntegerField()),
                ('creationDate', models.DateTimeField()),
                ('modifyBy', models.BigIntegerField()),
                ('modifyDate', models.DateTimeField()),
                ('userId', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='alarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alarmCode', models.CharField(max_length=15)),
                ('deviceCode', models.CharField(max_length=15)),
                ('deviceName', models.CharField(max_length=20)),
                ('alarmDate', models.DateTimeField(auto_now=True)),
                ('alarmType', models.CharField(max_length=15)),
                ('processDate', models.DateTimeField(null=True)),
                ('processState', models.BooleanField()),
                ('imgPath', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billCode', models.CharField(max_length=20)),
                ('productName', models.CharField(max_length=20)),
                ('productDesc', models.CharField(max_length=50)),
                ('productUnit', models.CharField(max_length=10)),
                ('productCount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=20)),
                ('isPayment', models.IntegerField(null=True)),
                ('createdBy', models.BigIntegerField()),
                ('creationDate', models.DateTimeField(auto_now=True)),
                ('modifyBy', models.BigIntegerField(null=True)),
                ('modifyDate', models.DateTimeField(null=True)),
                ('providerId', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departCode', models.CharField(max_length=15)),
                ('departName', models.CharField(max_length=10)),
                ('memberNum', models.BigIntegerField()),
                ('departManager', models.CharField(max_length=10)),
                ('departPhone', models.CharField(max_length=20)),
                ('createdBy', models.BigIntegerField(default=1)),
                ('creationDate', models.DateTimeField(auto_now=True)),
                ('modifyBy', models.BigIntegerField(null=True)),
                ('modifyDate', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proCode', models.CharField(max_length=20)),
                ('proName', models.CharField(max_length=20)),
                ('proDesc', models.CharField(max_length=50)),
                ('proContact', models.CharField(max_length=20)),
                ('proPhone', models.CharField(max_length=20)),
                ('proAddress', models.CharField(max_length=50)),
                ('proFax', models.CharField(max_length=20)),
                ('createdBy', models.BigIntegerField()),
                ('creationDate', models.DateTimeField()),
                ('modifyDate', models.DateTimeField()),
                ('modifyBy', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roleCode', models.CharField(max_length=15)),
                ('roleName', models.CharField(max_length=15)),
                ('createdBy', models.BigIntegerField()),
                ('creationDate', models.DateTimeField(auto_now=True)),
                ('modifyBy', models.BigIntegerField()),
                ('modifyDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userCode', models.CharField(max_length=20)),
                ('userName', models.CharField(max_length=20, null=True)),
                ('userPassword', models.CharField(max_length=15)),
                ('gender', models.IntegerField(default=1)),
                ('birthday', models.DateTimeField(null=True)),
                ('department', models.IntegerField(null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('address', models.CharField(max_length=30, null=True)),
                ('userRole', models.BigIntegerField(default=3)),
                ('createdBy', models.BigIntegerField(default=1)),
                ('creationDate', models.DateTimeField(auto_now=True)),
                ('modifyBy', models.BigIntegerField(null=True)),
                ('modifyDate', models.DateTimeField(null=True)),
                ('idPicPath', models.CharField(max_length=200, null=True)),
                ('workPicPath', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='vertifyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userCode', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=10)),
                ('time', models.IntegerField()),
            ],
        ),
    ]
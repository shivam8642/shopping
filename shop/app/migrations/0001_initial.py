# Generated by Django 4.0.2 on 2022-03-02 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(default='', upload_to='products')),
                ('description', models.CharField(max_length=100)),
                ('is_featured', models.BooleanField(verbose_name='featured')),
                ('is_new_stock', models.BooleanField(verbose_name='new stock')),
                ('is_sale_available', models.BooleanField(verbose_name='sale')),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('sub_title', models.CharField(max_length=100)),
                ('describe', models.CharField(max_length=200)),
                ('image_1', models.ImageField(default='', upload_to='products')),
            ],
        ),
    ]
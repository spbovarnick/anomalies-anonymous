# Generated by Django 4.1.7 on 2023-04-08 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('shape', models.CharField(choices=[('UNK', 'unknown'), ('CYL', 'cylinder'), ('LIG', 'light'), ('CIR', 'circle'), ('SPH', 'sphere'), ('DIS', 'disc'), ('CIG', 'cigar'), ('FIR', 'fireball'), ('OVA', 'oval'), ('REC', 'rectangle'), ('OTH', 'other'), ('CHE', 'chevron'), ('TRI', 'triangle'), ('FOR', 'formation'), ('CHA', 'changing'), ('FLA', 'flash'), ('DIA', 'diamond'), ('EGG', 'egg'), ('TEA', 'teardrop'), ('CON', 'cone'), ('CRE', 'crescent'), ('CRO', 'cross'), ('HEX', 'hexagon'), ('ROU', 'round'), ('DEL', 'delta'), ('DOM', 'dome'), ('PYR', 'pyramid'), ('FLA', 'flare')], default='UNK', max_length=3)),
                ('duration', models.DurationField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('description', models.TextField(max_length=300)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('sighting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.sighting')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(max_length=300)),
                ('sighting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.sighting')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]

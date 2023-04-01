from django.db import models


# Create your models here.
class Sighting(models.Model):
    STATE_CHOICES = (
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('DC', 'District of Columbia'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    )
    SHAPE_CHOICES = (
        ('UNK', 'unknown'),
        ('CYL', 'cylinder'),
        ('LIG', 'light'),
        ('CIR', 'circle'),
        ('SPH', 'sphere'),
        ('DIS', 'disc'),
        ('CIG', 'cigar'),
        ('FIR', 'fireball'),
        ('OVA', 'oval'),
        ('REC', 'rectangle'),
        ('OTH', 'other'),
        ('CHE', 'chevron'),
        ('TRI', 'triangle'),
        ('FOR', 'formation'),
        ('CHA', 'changing'),
        ('FLA', 'flash'),
        ('DIA', 'diamond'),
        ('EGG', 'egg'),
        ('TEA', 'teardrop'),
        ('CON', 'cone'),
        ('CRE', 'crescent'),
        ('CRO', 'cross'),
        ('HEX', 'hexagon'),
        ('ROU', 'round'),
        ('DEL', 'delta'),
        ('DOM', 'dome'),
        ('PYR', 'pyramid'),
        ('FLA', 'flare'),
    )
    datetime = models.DateTimeField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    shape = models.CharField(max_length=3, choices=SHAPE_CHOICES, default=SHAPE_CHOICES[0][0])
    duration = models.DurationField()
    date_posted = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=8, decimal_places=6)
    description = models.TextField(max_length=300)

class Comment(models.Model):
    sighting = models.ForeignKey('Sighting')
    date_posted = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=300)

from django.db.models import BooleanField, CharField, Model, IntegerField, ForeignKey, CASCADE, BinaryField, OneToOneField

class Ticket(Model):
    PASSENGER_STATES = [
        ("0", "Absent"     ),
        ("1", "Checked in" ),
        ("2", "Closed zone"),
        ("3", "Boarded"    ),
    ]
    passenger_name = CharField(max_length=64)
    passenger_state = CharField(max_length=1, choices=PASSENGER_STATES);
    biometrics = CharField(max_length=27330) # length of a base64 encoded array of 512 floats
    flight = IntegerField()


from django.forms import ChoiceField, Form, FileField, CharField, IntegerField, ValidationError
import base64
import struct

class TicketUploadForm(Form):
    file = FileField()
    passenger_name = CharField()
    flight_id = IntegerField()

# class Base64FloatArrayField(CharField):
#     def to_python(self, value):
#         if not value:
#             return None
#         try:
#             byte_data = base64.b64decode(value)
#             float_list = struct.unpack('f' * 512, byte_data)
#             return list(float_list)
#         except (TypeError, ValueError, struct.error) as e:
#             raise ValidationError("Invalid data format: %s" % e)

class CameraForm(Form):
    CAMERA_LOCATIONS = [
        ("1", "Check-in"   ),
        ("2", "Closed zone"),
        ("3", "Boarding"   ),
    ]
    flight = IntegerField();
    location = ChoiceField(choices=CAMERA_LOCATIONS)
    passenger_biometrics = CharField(max_length=10000)


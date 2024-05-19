from django.apps import AppConfig
import identity


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    db_path = "face_encodings.db"
    def ready(self):
        identity.initialize_database(self.db_path)


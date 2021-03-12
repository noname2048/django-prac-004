from django.conf import settings

use_db = settings.USE_DB


class AccountRouter:
    use_db = use_db
    route_app_labels = {
        "auth",
        "contenttypes",
        "account",
        "admin",
        "sessions",
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.use_db
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.use_db
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # print(f"{db} {app_label} {self.use_db} HEY!!!!!!!!!!!!!!", end=" ")
        if app_label in self.route_app_labels:
            # print(db == "dev")
            return db == self.use_db
        return None

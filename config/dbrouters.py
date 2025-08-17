class AuthRouter:
    route_app_labels = {"auth", "contenttypes", "sessions", "admin"}

    def db_for_read(self, model, **hints):
        return "auth_db" if model._meta.app_label in self.route_app_labels else "default"

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == "auth_db"
        return db == "default"

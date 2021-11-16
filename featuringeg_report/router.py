from report.models.report import *


class FeaturingEngineRouter:

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'component':
            return 'eg_report'

        if model._meta.app_label == 'report':
            return 'eg_report'

        if model._meta.app_label == 'instagram_score':
            return 'score_report'


        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'component':
            return 'eg_report'

        if model._meta.app_label == 'report':
            return 'eg_report'

        if model._meta.app_label == 'instagram_score':
            return 'score_report'
        

        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'component':
            return db == 'eg_report'

        if app_label == 'report':
            return db == 'eg_report'

        if app_label == 'instagram_score':
            return db == 'score_report'

        if app_label == 'auth' or app_label == 'admin' or app_label == 'contenttypes' \
            or app_label == 'sessions':
            return False

        return None

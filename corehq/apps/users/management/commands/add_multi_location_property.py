from django.core.management.base import BaseCommand

from corehq.apps.es import UserES, filters
from corehq.apps.es import users as user_filters
from corehq.apps.users.models import CouchUser
from corehq.apps.users.util import user_location_data
from corehq.util.couch import DocUpdate, iter_update
from corehq.util.log import with_progress_bar


class Command(BaseCommand):
    help = ("(Migration) Autofill the new field assigned_location_ids to existing users")

    def handle(self, **options):
        self.options = options
        user_ids = with_progress_bar(self.get_user_ids())
        iter_update(CouchUser.get_db(), self.migrate_user, user_ids, verbose=True)

    def migrate_user(self, doc):
        if doc['doc_type'] == 'WebUser':
            return self.migrate_web_user(doc)
        elif doc['doc_type'] == 'CommCareUser':
            return self.migrate_cc_user(doc)

    @classmethod
    def migrate_cc_user(cls, doc):

        # skip if doesn't have location
        if not doc.get('location_id'):
            return

        # skip if already migrated
        if doc['location_id'] in doc.get('assigned_location_ids', []):
            user_data = doc.get('user_data', {})
            expected = user_location_data(doc['assigned_location_ids'])
            actual = user_data.get('commcare_location_ids', None)
            if expected == actual:
                return

        apply_migration(doc)
        apply_migration(doc['domain_membership'])
        if doc['assigned_location_ids']:
            doc['user_data'].update({
                'commcare_location_ids': user_location_data(doc['assigned_location_ids'])
            })
        return DocUpdate(doc)

    @classmethod
    def migrate_web_user(cls, doc):
        def should_skip(dm):
            if not dm.get('location_id'):
                return True

            if dm['location_id'] in dm.get('assigned_location_ids', []):
                return True

        if all([should_skip(dm) for dm in doc['domain_memberships']]):
            return

        for membership in doc['domain_memberships']:
            if not should_skip(membership):
                apply_migration(membership)

        return DocUpdate(doc)

    def get_user_ids(self):
        res = (UserES()
               .OR(filters.AND(user_filters.mobile_users(), filters.non_null('location_id')),
                   filters.AND(user_filters.web_users(), filters.non_null('domain_memberships.location_id')))
               .exclude_source()
               .run())
        return list(res.doc_ids)


def apply_migration(doc):
    # doc can be a user dict or a domain_membership dict
    location_id = doc.get('location_id')
    if location_id:
        assigned_location_ids = doc.get('assigned_location_ids', [])
        if location_id not in assigned_location_ids:
            assigned_location_ids.append(location_id)

        doc['assigned_location_ids'] = assigned_location_ids

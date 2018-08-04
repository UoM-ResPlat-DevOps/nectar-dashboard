import re
import logging

from keystoneauth1 import loading
from keystoneauth1 import session
from nectarallocationclient import client

from django.conf import settings

LOG = logging.getLogger('nectar_dashboard.rcallocation')

def user_is_allocation_admin(user):
    return user.has_perm('openstack.roles.allocationadmin')

def get_project_prefix():
    """Returns the setting ALLOCATIONS_PROJECT_PREFIX.
    """
    try:
        prefix = settings.ALLOCATIONS_PROJECT_PREFIX
        regex = re.compile("^[a-zA-Z][-_a-zA-Z0-9]{1,15}$")
        if regex.match(prefix) is None:
            LOG.error("Django setting 'ALLOCATIONS_PROJECT_PREFIX = {0}' is "
                "invalid. Must start with a letter and only contain letters, "
                "numbers, hyphens and underscores (16 chars max)."
                "".format(prefix))
            prefix = ''
        if prefix.startswith('pt-'):
            LOG.warning("Note that NeCTAR trial projects are prefixed with pt-"
                ". Check that this prefix is appropriate for use.")
    except AttributeError:
        LOG.debug("Django setting ALLOCATIONS_PROJECT_PREFIX not set.")
        prefix = ''
    except Exception as e:
        LOG.critical("Unexpected exception: " + str(e))
        raise
    return prefix

def get_nectar_client():
    try:
        auth_options = dict(settings.ALLOCATIONS_KEYSTONE)
        nectar_client_vers = settings.ALLOCATIONS_NECTAR_CLIENT_VERS
        # TODO: Consider validating settings
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(**auth_options)
        sess = session.Session(auth=auth)
        nectar = client.Client(nectar_client_vers, session=sess)
        # TODO: Are any exceptions actually thrown? Or do we need to stat
        # something to see if the session and client are valid?
        # `public endpoint for allocations service not found`
    except Exception as e:
        msg = ("Keystone authentication failed. Exception raised: {0}"
            "".format(str(e)))
        LOG.critical(msg)
        raise

    # Check that the auth has the correct role for managing allocations
    try:
        admin_role = settings.ALLOCATIONS_NECTAR_ADMIN_ROLE
        auth_ref = auth.get_auth_ref(sess)
        roles = auth_ref.role_names
        if not admin_role in roles:
            raise Exception("User {0} does not have the required role "
                "({1}) to manage allocations: {2}".format(
                auth_options['username'], admin_role, str(roles)))
    except Exception as e:
        LOG.critical(e.message)
        raise

    return nectar

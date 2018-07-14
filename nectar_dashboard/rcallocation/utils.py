import re
import logging

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

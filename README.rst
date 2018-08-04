===============================
uom-cloud-dashboard
===============================

Forked from `NeCTAR-RC/nectar-dashboard`_.

* Free software: GPLv3+ license

local_settings.py
-----------------

The following settings are required for UoM-specific features to work::

  ####################
  # UoM settings     #
  ####################

  HORIZON_CONFIG['navbar_support_links'] = [
      {
          'text': 'Submit a ticket',
          'icon': 'fa-ticket',
          'url': 'https://unimelb.service-now.com/research'
      },
      {
          'text': 'Training',
          'icon': 'fa-group',
          'url': 'https://research.unimelb.edu.au/infrastructure/research-platform-services/training/research-cloud'
      },
      '-',
      {
          'text': 'Research Platform Services website',
          'icon': 'fa-external-link',
          'url': 'https://research.unimelb.edu.au/infrastructure/research-platform-services'
      },
  ]

  ALLOCATIONS_PROJECT_PREFIX = 'unimelb-'

  ALLOCATIONS_KEYSTONE = (
      ('auth_url', OPENSTACK_KEYSTONE_URL),
      ('username', ''),
      ('password', ''),
      ('project_name', ''),
      ('user_domain_id', 'default'),
      ('project_domain_id', 'default'),
  )

  ALLOCATIONS_NECTAR_ADMIN_ROLE = 'AllocationAdmin'

  ALLOCATIONS_NECTAR_CLIENT_VERS = '1'

  ALLOCATIONS_NECTAR_SOURCE = 'uom'


For configuring ``navbar_support_links`` the ``icon`` field is optional. Visit
the `Font Awesome website`_ to see available icons. To add a divider between
links add ``'-'`` to the list in place of a dict, as shown above.

Ensure the ``ALLOCATIONS_KEYSTONE`` is configured (i.e. fill in the fields that
were left blank above) for the rcallocation ``provision`` command to work.


.. _`NeCTAR-RC/nectar-dashboard`: https://github.com/NeCTAR-RC/nectar-dashboard
.. _`Font Awesome website`: https://fontawesome.com/v4.7.0/icons/

=============================
RC Allocation Web Application
=============================

Introduction
============

This site handles the application for allocations on the
`NeCTAR Research Cloud`_ cloud by members of the research community.

University of Melbourne fields
==============================

The list of UniMelb Department Numbers were gathered `from ServiceNow`_.

To update the database after modifying fields::

  sudo /path/to/horizon-manage.py makemigrations
  sudo /path/to/horizon-manage.py showmigrations
  sudo /path/to/horizon-manage.py migrate rcallocation <new migration name>

See the `Django documentation`_ for more information and on these commands and
their options.

Todo
====

* Add better table handling to the allocation request list template.

Notes
=====

Users should extend Django users - and not be separate as they currently are?
See `User authentication in Django`_.


.. _`NeCTAR Research Cloud`: http://nectar.org.au/research-cloud/
.. _`from ServiceNow`: https://unimelb.service-now.com/it?id=kb_article&sys_id=6e48710adb55bac0ef18f389bf96199d
.. _`Django documentation`: https://docs.djangoproject.com/en/2.0/ref/django-admin/
.. _`User authentication in Django`: https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users

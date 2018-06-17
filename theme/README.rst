=============
Unimelb Theme
=============

Todo
====

* ``templates/header/_header.html`` and ``templates/auth/_login.html``: Make
  the brand name (hardcoded as 'Melbourne Research Cloud') load from
  ``{% site_branding %}``.
* ``templates/header/_header.html``: Safe load support link as a variable set
  in HORIZON_CONFIG.

Development
===========

This theme is adapted from the `Unimelb Design System`_. The Unimelb Design
System on GitHub: `unimelb/unimelb-design-system`_. The commit referenced
during the original development of this dashboard theme (June 2018)
was `unimelb/unimelb-design-system@aa5958f5fa`_.

The base custom Horizon theme that the Unimelb Design System was adapted on top
of was `NeCTAR-RC/nectar-dashboard@5bebde360f`_. Note that `nectar.scss`_
needed to be removed from the rcallocation dashboard because it was setting
header and footer styles when enabled.

The Horizon Queens repo used is `NeCTAR/horizon (nectar/queens)`_. In
particular the following files are directories in /openstack_dashboard are
useful references for theme development:

* The templates that are inherited or overridden are located in
  `templates`_.
* The styles that are loaded by default are defined in
  `templates/_stylesheets.html`_ (and hence
  `templates/themes/themes.scss`_). This includes the
  directories `themes/default`_ and `static/dashboard/scss`_.

Information about developing custom themes for Horizon Queens can be found in
the `OpenStack Documentation`_.

Theme structure
---------------

There is one variables file (``_variables.scss``). This contains bootstrap
overrides, and in addition the `globals`_ which are defined in the Unimelb
Design System.

All styles (.scss files) are located in the ``/static`` directory. The names of
the files correspond to the names of the templates which they primarily style.
The exceptions are ``_mixins.scss`` (for global mixins) and ``_layout.scss``
(for styles relating to the full page layout).

The templates in ``/templates`` override the default theme templates and mostly
generate the ``<body>`` markup. In addition, there are two special custom
templates:

* To insert custom meta tags into the ``<head>`` use
  ``templates/horizon/_custom_meta.html``.
* To insert custom script tags into the ``<head>`` use
  ``templates/horizon/_custom_head_js.html``.

Approach to adapting Unimelb Design System
------------------------------------------

HTML markup has been copied from the Design System for the header and footers.
All classes taken from the Design System are prefixed with ``uomt-`` (i.e.
**U**niversity **o**f **M**elbourne **T**emplate) to prevent any unintentional
element targeting (e.g. ``.nav`` is a class used in both the Design System and
Horizon bootstrap). This maintains provenance in the markup so it can be easily
traced to its source. In some instances elements have also been defined as an
ID because IDs take precedence over classes in styling, so this helps override
any ID-targeted bootstrap rules set for higher-level elements.

Instances where CSS rules are adapted from the Design System, but the targeting
does not correspond to the appropriate ``uomt-*`` class are explained in the
inline comments.

Sizes in the Design System CSS (e.g. font-size, height, width, margin,
padding) are mostly defined in ``rem`` rather than ``px``. The ``rem`` values
set in the Design System do not translate into Horizon cleanly because the
bootstrap sets ``html { font-size: 10px; }``. The variable ``$uomt-scale`` was
defined to overcome this issue (set at ``1.6``) which any ``rem`` value taken
from the Design System is then multiplied by. This maintains the readability of
the CSS set in this theme so values can be easily compared to its source.

Where deemed appropriate, external links to .css files on the Design System
GitHub are included in inline comments in the .scss theme files for easy
reference.

Mobile browser support
----------------------

The mobile browsing experience is not ideal, and it is difficult to provide
full responsiveness for the dashboard, but best efforts have been taken. The
responsiveness of the Design System header and footer have been carried over,
and the sidebar transitions into a top nav.

Additional resources
--------------------

This section outlines some additional resources that were used in the
development of this theme.

* The login/splash page and the 'User' header button were based on:
  https://web.unimelb.edu.au/layouts/with-login/
* The login/splash page and the sidebar were based on:
  https://research.unimelb.edu.au/infrastructure/research-platform-services/services/research-cloud

Browser compatibility *(incomplete)*
====================================

This theme is compatible with the minimum versions of the following browsers:

+------------------+------------------------------------+---------------+
| Operating system | Browser                            | Support       |
+==================+====================================+===============+
| Windows          | Internet Explorer 8-10             | untested      |
+------------------+------------------------------------+---------------+
|                  | Internet Explorer 11               | untested      |
+------------------+------------------------------------+---------------+
|                  | Edge                               | untested      |
+------------------+------------------------------------+---------------+
|                  | Google Chrome                      | untested      |
+------------------+------------------------------------+---------------+
|                  | Mozilla Firefox                    | untested      |
+------------------+------------------------------------+---------------+
| macOS            | Safari 9 and later                 | untested      |
+------------------+------------------------------------+---------------+
|                  | Google Chrome 67.0+                | compliant     |
+------------------+------------------------------------+---------------+
|                  | Mozilla Firefox                    | untested      |
+------------------+------------------------------------+---------------+
| iOS              | Safari for iOS 9.3 and later       | untested      |
+------------------+------------------------------------+---------------+
|                  | Google Chrome                      | untested      |
+------------------+------------------------------------+---------------+
| Android          | Google Chrome                      | untested      |
+------------------+------------------------------------+---------------+
|                  | Samsung Internet                   | untested      |
+------------------+------------------------------------+---------------+

The above list was adapted from `gov.uk`_.

Options for third column: untested, functional, compliant.

Testing process *(incomplete)*
------------------------------

The process should involve testing an unknown configuration against a compliant
and stable implementation of the theme. In particular, look at the following
features (broken down by page section):

**Header**

* Scroll down and check the header becoming fixed. Check the transitions and
  vertical text alignment.


.. _`Unimelb Design System`: https://web.unimelb.edu.au/getting-started/
.. _`unimelb/unimelb-design-system`: https://github.com/unimelb/unimelb-design-system
.. _`unimelb/unimelb-design-system@aa5958f5fa`: https://github.com/unimelb/unimelb-design-system/tree/aa5958f5fa6f34338fd6d8a600fa49cf87d5f0b1
.. _`NeCTAR-RC/nectar-dashboard@5bebde360f`: https://github.com/NeCTAR-RC/nectar-dashboard/tree/5bebde360ff95b8b6a92e4f8954dedb515a740af/theme
.. _`nectar.scss`: https://github.com/NeCTAR-RC/nectar-dashboard/blob/5bebde360ff95b8b6a92e4f8954dedb515a740af/nectar_dashboard/rcallocation/static/rcportal/scss/nectar.scss
.. _`OpenStack Documentation`: https://docs.openstack.org/horizon/queens/configuration/themes.html
.. _`NeCTAR/horizon (nectar/queens)`: https://github.com/NeCTAR-RC/horizon/tree/nectar/queens
.. _`templates`: https://github.com/NeCTAR-RC/horizon/tree/nectar/queens/openstack_dashboard/templates
.. _`templates/_stylesheets.html`: https://github.com/NeCTAR-RC/horizon/blob/nectar/queens/openstack_dashboard/templates/_stylesheets.html
.. _`templates/themes/themes.scss`: https://github.com/NeCTAR-RC/horizon/blob/nectar/queens/openstack_dashboard/templates/themes/themes.scss
.. _`themes/default`: https://github.com/NeCTAR-RC/horizon/tree/nectar/queens/openstack_dashboard/themes/default
.. _`static/dashboard/scss`: https://github.com/NeCTAR-RC/horizon/tree/nectar/queens/openstack_dashboard/static/dashboard/scss
.. _`globals`: https://github.com/unimelb/unimelb-design-system/blob/aa5958f5fa6f34338fd6d8a600fa49cf87d5f0b1/assets/shared/_globals.css
.. _`gov.uk`: https://www.gov.uk/service-manual/technology/designing-for-different-browsers-and-devices#browsers-to-test-in
.. _`NeCTAR-RC/horizon`: https://github.com/NeCTAR-RC/horizon

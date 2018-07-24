# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def migrate_quota_groups(apps, schema_editor):

    Zone = apps.get_model('rcallocation', 'Zone')
    Resource = apps.get_model('rcallocation', 'Resource')
    ServiceType = apps.get_model('rcallocation', 'ServiceType')

    # Note: Use objects.delete() to remove Resources <https://docs.djangoproject.com/en/2.0/ref/models/querysets/#delete>

    # Melbourne zones
    zone_melbourne, created = Zone.objects.update_or_create(name='melbourne', defaults={'display_name': 'Melbourne'})

    # Legacy NeCTAR zones
    zone_nectar, created = Zone.objects.update_or_create(name='nectar', defaults={'display_name': 'NeCTAR'})
    zone_auckland, created = Zone.objects.update_or_create(name='auckland', defaults={'display_name': 'Auckland (NZ)'})
    zone_intersect, created = Zone.objects.update_or_create(name='intersect', defaults={'display_name': 'Intersect (NSW)'})
    zone_monash, created = Zone.objects.update_or_create(name='monash', defaults={'display_name': 'Monash (VIC)'})
    zone_NCI, created = Zone.objects.update_or_create(name='NCI', defaults={'display_name': 'NCI (ACT)'})
    zone_QRIScloud, created = Zone.objects.update_or_create(name='QRIScloud', defaults={'display_name': 'QRIScloud'})
    zone_QRIScloud_rds, created = Zone.objects.update_or_create(name='QRIScloud-rds', defaults={'display_name': 'QRIScloud RDS'})
    zone_sa, created = Zone.objects.update_or_create(name='sa', defaults={'display_name': 'South Australia'})
    zone_swinburne, created = Zone.objects.update_or_create(name='swinburne', defaults={'display_name': 'Swinburne (VIC)'})
    zone_tasmania, created = Zone.objects.update_or_create(name='tasmania', defaults={'display_name': 'Tasmania'})

    # Compute Service

    st_compute, created = ServiceType.objects.update_or_create(
        catalog_name='compute',
        defaults={
            'name': 'Compute Resources',
            'description': """The maximum number of instances and virtual cores that you think your project will require at any one time.""",
            'index': 0,
            'required': True
        }
    )

    st_compute.zones.clear()
    st_compute.zones.add(zone_nectar)

    core_resource, created = Resource.objects.update_or_create(
        quota_name='cores',
        service_type=st_compute,
        defaults={
            'name': 'Virtual Cores',
            'unit': 'VCPUs',
            'requestable': True,
            'help_text': None,
            'service_type': st_compute
        }
    )

    instance_resource, created = Resource.objects.update_or_create(
        quota_name='instances',
        service_type=st_compute,
        defaults={
            'name': 'Instances',
            'unit': 'servers',
            'requestable': True,
            'help_text': None,
            'service_type': st_compute
        }
    )

    ram_resource, created = Resource.objects.update_or_create(
        quota_name='ram',
        service_type=st_compute,
        defaults={
            'name': 'RAM',
            'unit': 'GiB',
            'requestable': False,
            'help_text': "Set RAM quota or leave as 0 to apply 4GiB of ram per core",
            'service_type': st_compute
        }
    )

    # Object Service

    st_object, created = ServiceType.objects.update_or_create(
        catalog_name='object',
        defaults={
            'name': 'Object Storage',
            'description': """Object Storage is a large accessible online storage location that you can reach from most machines with internet connectivity. Object Storage requires cloud native applications for access. Specify the total size in gigabytes that the project will need.""",
            'index': 2,
            'required': False
        }
    )

    st_object.zones.clear()
    st_object.zones.add(zone_nectar)

    object_resource, created = Resource.objects.update_or_create(
        quota_name='object',
        service_type=st_object,
        defaults={
            'name': 'Object storage',
            'unit': 'GiB',
            'requestable': True,
            'help_text': None,
            'service_type': st_object
        }
    )

    # Volume Service

    st_volume, created = ServiceType.objects.update_or_create(
        catalog_name='volume',
        defaults={
            'name': 'Volume Storage',
            'description': """A persistent volume looks and acts like a hard drive that can be attached to your virtual machine instances. Volumes and their data persist independently of virtual machine instances and volumes can be dynamically attached and detached to/from different virtual machine instances. Specify the total size in gigabytes that the project will need.""",
            'index': 1,
            'required': False
        }
    )

    st_volume.zones.clear()
    st_volume.zones.add(zone_melbourne)

    gigabytes_resource, created = Resource.objects.update_or_create(
        quota_name='gigabytes',
        service_type=st_volume,
        defaults={
            'name': 'Volume storage',
            'unit': 'GiB',
            'requestable': True,
            'help_text': None,
            'service_type': st_volume
        }
    )

    # Advanced Networking

    st_network, created = ServiceType.objects.update_or_create(
        catalog_name='network',
        defaults={
            'name': 'Advanced Networking',
            'description': """Virtual resources for building more advanced network topologies for your instances, including routers, load balancers and private networks.""",
            'index': 3,
            'required': False
        }
    )

    st_network.zones.clear()
    st_network.zones.add(zone_nectar)

    network_resource, created = Resource.objects.update_or_create(
        quota_name='network',
        service_type=st_network,
        defaults={
            'name': 'Networks',
            'unit': 'Networks',
            'requestable': True,
            'help_text': None,
            'service_type': st_network
        }
    )

    router_resource, created = Resource.objects.update_or_create(
        quota_name='router',
        service_type=st_network,
        defaults={
            'name': 'Routers',
            'unit': 'Routers',
            'requestable': True,
            'help_text': None,
            'service_type': st_network
        }
    )

    floatingip_resource, created = Resource.objects.update_or_create(
        quota_name='floatingip',
        service_type=st_network,
        defaults={
            'name': 'Floating IPs',
            'unit': 'Floating IPs',
            'requestable': True,
            'help_text': None,
            'service_type': st_network
        }
    )

    loadbalancer_resource, created = Resource.objects.update_or_create(
        quota_name='loadbalancer',
        service_type=st_network,
        defaults={
            'name': 'Load Balancers',
            'unit': 'Load Balancers',
            'requestable': True,
            'help_text': None,
            'service_type': st_network
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('rcallocation', '0018_unimelb-changes-init'),
    ]

    operations = [
        migrations.RunPython(migrate_quota_groups)
    ]

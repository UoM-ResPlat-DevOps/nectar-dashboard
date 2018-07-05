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
            'description': """The maximum number of instances and virtual cores that you think your project will require at any one time. Please consult the <a href="#">flavour list</a> to see the relationship between number of instances and virtual cores.""",
            'index': 0,
            'required': True
        }
    )

    st_compute.zones.clear()
    st_compute.zones.add(zone_melbourne)

    core_resource, created = Resource.objects.update_or_create(
        quota_name='cores',
        service_type=st_compute,
        defaults={
            'unit': 'VCPUs',
            'name': 'Virtual Cores',
            'help_text': """This is the maximum number of cores you'd like to use at any one time across all instances. For example, if you'd like to be able to run two "XXL Sized" instances at once (each has 16 CPU cores), you should specify 32 here.""",
            'service_type': st_compute
        }
    )

    ram_resource, created = Resource.objects.update_or_create(
        quota_name='ram',
        service_type=st_compute,
        defaults={
            'unit': 'GB',
            'name': 'RAM',
            'service_type': st_compute
        }
    )

    instance_resource, created = Resource.objects.update_or_create(
        quota_name='instances',
        service_type=st_compute,
        defaults={
            'unit': 'servers',
            'name': 'Instances',
            'help_text': """The maximum number of instances that you think your project will require at any one time.""",
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
    st_object.zones.add(zone_melbourne)

    object_resource, created = Resource.objects.update_or_create(
        quota_name='object',
        service_type=st_object,
        defaults={
            'unit': 'GB',
            'name': 'Storage',
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
            'unit': 'GB',
            'name': 'Storage',
            'service_type': st_volume
        }
    )

    # Advanced Networking

    st_network, created = ServiceType.objects.update_or_create(
        catalog_name='network',
        defaults={
            'name': 'Advanced Networking',
            'description': """Virtual resources for building more advanced network topologies for your instances, including routers, loadbalancers and private networks.""",
            'index': 3,
            'required': False
        }
    )

    st_network.zones.clear()
    st_network.zones.add(zone_melbourne)

    networks_resource, created = Resource.objects.update_or_create(
        quota_name='networks',
        service_type=st_network,
        defaults={
            'unit': 'Networks',
            'name': 'Networks',
            'service_type': st_network
        }
    )

    routers_resource, created = Resource.objects.update_or_create(
        quota_name='routers',
        service_type=st_network,
        defaults={
            'unit': 'Routers',
            'name': 'Routers',
            'service_type': st_network
        }
    )

    floating_ips_resource, created = Resource.objects.update_or_create(
        quota_name='floating_ips',
        service_type=st_network,
        defaults={
            'unit': 'Floating IPs',
            'name': 'Floating IPs',
            'service_type': st_network
        }
    )

    load_balancers_resource, created = Resource.objects.update_or_create(
        quota_name='load_balancers',
        service_type=st_network,
        defaults={
            'unit': 'Load Balancers',
            'name': 'Load Balancers',
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

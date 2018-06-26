# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('rcallocation', '0017_grant-type-change'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocationrequest',
            name='accepted_terms',
            field=models.CharField(max_length=255, choices=[(b'yes', b'Yes'), (b'no', b'No')], null=True, verbose_name=b'I have read and accepted the <a href="/terms" target="_blank">\n            University of Melbourne - Terms and Conditions</a>', validators=[django.core.validators.RegexValidator(regex=b'^yes$', message=b'You must accept the Terms and Conditions.')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_dept',
            field=models.CharField(help_text=b'Select the main department this project is for.', max_length=255, null=True, verbose_name=b'Department this project is for', choices=[(b'0000', b'0000 - University General'), (b'0060', b"0060 - Vice-Chancellor's Office"), (b'0380', b'0380 - The Ian Potter Museum of Art'), (b'0920', b'0920 - Asialink'), (b'0950', b'0950 - Advancement'), (b'1000', b'1000 - Arts'), (b'1030', b'1030 - Arts Business Centre'), (b'1060', b'1060 - Culture and Communication'), (b'1100', b'1100 - Asia Institute'), (b'1120', b'1120 - Arts & Music Student Centre'), (b'1140', b'1140 - Graduate School of Humanities and Social Sciences'), (b'1190', b'1190 - School of Language and Linguistics'), (b'1310', b'1310 - School of Historical and Philosophical Studies'), (b'1510', b'1510 - Melbourne School of Government'), (b'1660', b'1660 - School of Social and Political Sciences'), (b'1942', b'1942 - Australian Mathematical Sciences Institute'), (b'1960', b'1960 - Social Work'), (b'2070', b'2070 - Resource Management and Geography'), (b'2080', b'2080 - Agriculture and Food Systems'), (b'2200', b'2200 - Forest and Ecosystem Science'), (b'2510', b'2510 - Veterinary and Agricultural Sciences Faculty'), (b'2860', b'2860 - Veterinary Hospital'), (b'3000', b'3000 - Faculty of Business and Economics'), (b'3040', b'3040 - Graduate School of Business and Economics'), (b'3060', b'3060 - Accounting'), (b'3160', b'3160 - Economics'), (b'3200', b'3200 - Business Administration'), (b'3250', b'3250 - Management & Marketing'), (b'3330', b'3330 - Finance'), (b'3360', b'3360 - Melbourne Institute of Applied Economic and Social Research'), (b'3510', b'3510 - The Melbourne Business School'), (b'4000', b'4000 - Engineering'), (b'4110', b'4110 - Chemical and Biomolecular Engineering'), (b'4180', b'4180 - Computing and Information Systems'), (b'4310', b'4310 - Engineering and Electrical Engineering'), (b'4320', b'4320 - Infrastructure Engineering'), (b'4360', b'4360 - Mechanical Engineering'), (b'4600', b'4600 - Melbourne Graduate School of Education'), (b'5000', b'5000 - Medicine Dentistry and Health Sciences'), (b'5000', b'5000 - MDHS Faculty IT'), (b'5000', b'5000 - VLSCI'), (b'5010', b'5010 - Peter Doherty Institute'), (b'5040', b'5040 - Rural Health Academic Centre'), (b'5050', b'5050 - Melbourne School of Population and Global Health'), (b'5070', b'5070 - Centre for Youth Mental Health'), (b'5080', b'5080 - Centre for Neuroscience Research'), (b'5090', b'5090 - Nossal Institute for Global Health'), (b'5100', b'5100 - Melbourne Medical School'), (b'5110', b'5110 - Melbourne Dental School'), (b'5120', b'5120 - Melbourne School of Psychological Sciences'), (b'5130', b'5130 - Physiotherapy'), (b'5140', b'5140 - Nursing'), (b'5160', b'5160 - Anatomy and Neuroscience'), (b'5200', b'5200 - Otolaryngology'), (b'5210', b'5210 - Biochemistry and Molecular Biology'), (b'5260', b'5260 - Microbiology and Immunology'), (b'5270', b'5270 - MDU Microbiology'), (b'5300', b'5300 - School Of Biomedical Sciences'), (b'5310', b'5310 - Pathology'), (b'5340', b'5340 - Pharmacology and Therapeutics'), (b'5360', b'5360 - Physiology'), (b'5400', b'5400 - Austin Academic Centre'), (b'5430', b'5430 - Medicine - Austin Health'), (b'5460', b'5460 - Surgery - Austin Health'), (b'5480', b'5480 - Clinical School - Austin Health'), (b'5500', b'5500 - Royal Melbourne Hospital Academic Centre'), (b'5510', b'5510 - Medical Education'), (b'5520', b'5520 - Surgery'), (b'5530', b'5530 - Medicine Royal Melbourne Hospital'), (b'5540', b'5540 - Psychiatry'), (b'5550', b'5550 - Radiology'), (b'5560', b'5560 - Surgery - Royal Melbourne Hospital'), (b'5570', b'5570 - Medicine and Radiology'), (b'5580', b'5580 - Clinical School - Royal Melbourne Hospital'), (b'5600', b'5600 - Eastern Hill Academic Centre'), (b'5630', b"5630 - Medicine - St Vincent's Hospital"), (b'5660', b"5660 - Surgery - St Vincent's Hospital"), (b'5680', b"5680 - Clinical School - St Vincent's Hospital"), (b'5700', b'5700 - School of Health Sciences'), (b'5710', b"5710 - Paediatrics Royal Children's Hospital"), (b'5760', b'5760 - Ophthalmology Eye and Ear Hospital'), (b'5770', b'5770 - Audiology and Speech Pathology'), (b'5790', b"5790 - Obstetrics and Gynaecology Royal Women's Hospital"), (b'5850', b'5850 - General Practice'), (b'5870', b'5870 - Rural Clinical School'), (b'5900', b'5900 - North West Academic Centre'), (b'5950', b'5950 - Clinical and Biomedical Sciences'), (b'5970', b'5970 - Medical Biology (W.E.H.I)'), (b'6030', b'6030 - Science, Faculty Secretariat'), (b'6040', b'6040 - Australian Mathematical Sciences Institute'), (b'6100', b'6100 - Chemistry'), (b'6150', b'6150 - Information Systems - HISTORICAL'), (b'6200', b'6200 - Mathematics and Statistics'), (b'6250', b'6250 - Earth Sciences'), (b'6300', b'6300 - School of Biosciences'), (b'6400', b'6400 - Physics'), (b'6500', b'6500 - Biology Laboratory'), (b'6550', b'6550 - Optometry and Vision Sciences'), (b'7020', b'7020 - Architecture, Building and Planning'), (b'7320', b'7320 - Law'), (b'7410', b'7410 - VCA and MCM'), (b'7420', b'7420 - Melbourne Conservatorium of Music'), (b'7500', b'7500 - Victorian College of the Arts'), (b'7890', b'7890 - Bio21 Institute'), (b'8130', b'8130 - Melbourne University of Publishing'), (b'8140', b'8140 - Grattan Institute'), (b'8240', b'8240 - Medley Hall'), (b'8300', b'8300 - Application Services'), (b'8490', b'8490 - Melbourne University Sport'), (b'8650', b'8650 - CERA Ltd'), (b'8670', b'8670 - Bio21 Australia Ltd'), (b'8800', b"8800 - Children's Services"), (b'8840', b'8840 - Nossal Institute Ltd'), (b'9110', b'9110 - Australian Music Examinations'), (b'9310', b'9310 - Administration and Finance'), (b'9320', b'9320 - Engagement'), (b'9330', b'9330 - Policy and Projects'), (b'9330', b'9330 - Carlton Connect'), (b'9340', b'9340 - Provost'), (b'9340', b'9340 - Murrup Barak Institute'), (b'9350', b'9350 - Research'), (b'9510', b'9510 - Sir Peter MacCullum - Department of Oncology'), (b'9520', b'9520 - Florey Department of Neuroscience and Mental Health'), (b'9560', b'9560 - Medical Bionics Department'), (b'9700', b'9700 - University Services'), (b'9710', b'9710 - Research, Industry & Commercialisation '), (b'9720', b'9720 - University Procurement'), (b'9730', b'9730 - Academic Services'), (b'9730', b'9730 - Research and Collections'), (b'9730', b'9730 - Scholarly Information'), (b'9730', b'9730 - Learning Environments'), (b'9740', b'9740 - Business Intelligence & Reporting'), (b'9750', b'9750 - External Relations'), (b'9760', b'9760 - Finance & Employee Services'), (b'9770', b'9770 - Infrastructure Services'), (b'9780', b'9780 - Legal Services & Governance'), (b'9790', b'9790 - Project Services')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_faculty',
            field=models.CharField(help_text=b'', max_length=255, null=True, verbose_name=b'Faculty this project is for', choices=[(b'fabp', b'Faculty of Architecture, Building and Planning'), (b'arts', b'Faculty of Arts'), (b'fbe', b'Faculty of Business and Economics'), (b'finearts-music', b'Faculty of Fine Arts and Music'), (b'mdhs', b'Faculty of Medicine, Dentistry and Health Sciences'), (b'science', b'Faculty of Science'), (b'fvas', b'Faculty of Veterinary and Agricultural Sciences'), (b'mgse', b'Melbourne Graduate School of Education'), (b'mls', b'Melbourne Law School'), (b'engineering', b'Melbourne School of Engineering')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_name',
            field=models.CharField(help_text=b'Name of the requester.', max_length=255, null=True, verbose_name=b'Name of requester'),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_phone',
            field=models.CharField(help_text=b'Phone number of requester.', max_length=255, null=True, verbose_name=b'Contact phone number'),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_role',
            field=models.CharField(help_text=b'', max_length=255, null=True, verbose_name=b'Your role', choices=[(b'professor', b'Professor'), (b'student-masters', b'Student - Masters by Research'), (b'student-phd', b'Student - PhD'), (b'era', b'ERA'), (b'techical-support-staff', b'Technical support staff')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='use_category',
            field=models.CharField(help_text=b'', max_length=255, null=True, verbose_name=b'Category of work', choices=[(b'research', b'Research'), (b'teaching', b'Teaching/Training'), (b'support', b'Support/Other')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='use_other',
            field=models.TextField(help_text=b'e.g. AWS, Google compute, Nectar, other NCRIS platforms,\n            ...', max_length=1024, verbose_name=b'List other capabilities you use/intend to use with this project', blank=True),
        ),
        migrations.AddField(
            model_name='chiefinvestigator',
            name='requester_is_ci',
            field=models.CharField(max_length=255, null=True, verbose_name=b'I am the Chief Investigator', choices=[(b'yes', b'Yes'), (b'no', b'No')]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='allocation_home',
            field=models.CharField(default=b'melbourne', help_text=b'You can provide a primary location where you expect to\n                use most resources, effectively the main Nectar site for your\n                allocation. Use of other locations is still possible.\n                This can also indicate a specific arrangement with a\n                Nectar site, for example where you obtain support, or if\n                your institution is a supporting member of that site.\n                Select unassigned if you have no preference.\n                ', max_length=128, verbose_name=b'Allocation home location', choices=[(b'national', b'Unassigned'), (b'nci', b'Australian Capital Territory (NCI)'), (b'intersect', b'New South Wales (Intersect)'), (b'qcif', b'Queensland (QCIF)'), (b'ersa', b'South Australia (eRSA)'), (b'tpac', b'Tasmania (TPAC)'), (b'uom', b'Victoria (Melbourne)'), (b'monash', b'Victoria (Monash)'), (b'swinburne', b'Victoria (Swinburne)'), (b'auckland', b'Auckland Uni (New Zealand)')]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='geographic_requirements',
            field=models.TextField(help_text=b'Indicate to the allocations committee any special\n                geographic requirements that you may need, e.g. to run\n                at more than one node.', max_length=1024, verbose_name=b'Special requirements', blank=True),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='use_case',
            field=models.TextField(help_text=b'Provide a very brief overview of your research project,\n        and how you will use the cloud to support your project.', max_length=4096, verbose_name=b'Use case'),
        ),
    ]

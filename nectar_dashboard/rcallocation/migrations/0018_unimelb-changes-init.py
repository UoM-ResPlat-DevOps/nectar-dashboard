# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('rcallocation', '0017_grant-type-change'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocationrequest',
            name='accepted_terms',
            field=models.CharField(choices=[(b'yes', b'Yes'), (b'no', b'No')], max_length=255, validators=[django.core.validators.RegexValidator(regex=b'^yes$', message=b'You must accept the Terms and Conditions.')], help_text=b'Users of The University of Melbourne Research Cloud must\n                     read and accept the Terms and Conditions.', null=True, verbose_name=b'I have read and accepted the <a href="/terms" target="_blank">\n            University of Melbourne - Terms and Conditions</a>'),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='project_dept',
            field=models.CharField(help_text=b'Select the main department this project is for.\n                  <br><br>If you cannot find your department, school\n                  or faculty listed here, please select "0000 -\n                  University General".\n                  ', max_length=255, null=True, verbose_name=b'Department this project is for', choices=[(b'0000', b'0000 - University General'), (b'0060', b"0060 - Vice-Chancellor's Office"), (b'0380', b'0380 - The Ian Potter Museum of Art'), (b'0920', b'0920 - Asialink'), (b'0950', b'0950 - Advancement'), (b'1000', b'1000 - Arts'), (b'1030', b'1030 - Arts Business Centre'), (b'1060', b'1060 - Culture and Communication'), (b'1100', b'1100 - Asia Institute'), (b'1120', b'1120 - Arts & Music Student Centre'), (b'1140', b'1140 - Graduate School of Humanities and Social Sciences'), (b'1190', b'1190 - School of Language and Linguistics'), (b'1310', b'1310 - School of Historical and Philosophical Studies'), (b'1510', b'1510 - Melbourne School of Government'), (b'1660', b'1660 - School of Social and Political Sciences'), (b'1942', b'1942 - Australian Mathematical Sciences Institute'), (b'1960', b'1960 - Social Work'), (b'2070', b'2070 - Resource Management and Geography'), (b'2080', b'2080 - Agriculture and Food Systems'), (b'2200', b'2200 - Forest and Ecosystem Science'), (b'2510', b'2510 - Veterinary and Agricultural Sciences Faculty'), (b'2860', b'2860 - Veterinary Hospital'), (b'3000', b'3000 - Faculty of Business and Economics'), (b'3040', b'3040 - Graduate School of Business and Economics'), (b'3060', b'3060 - Accounting'), (b'3160', b'3160 - Economics'), (b'3200', b'3200 - Business Administration'), (b'3250', b'3250 - Management & Marketing'), (b'3330', b'3330 - Finance'), (b'3360', b'3360 - Melbourne Institute of Applied Economic and Social Research'), (b'3510', b'3510 - The Melbourne Business School'), (b'4000', b'4000 - Engineering'), (b'4110', b'4110 - Chemical and Biomolecular Engineering'), (b'4180', b'4180 - Computing and Information Systems'), (b'4310', b'4310 - Engineering and Electrical Engineering'), (b'4320', b'4320 - Infrastructure Engineering'), (b'4360', b'4360 - Mechanical Engineering'), (b'4600', b'4600 - Melbourne Graduate School of Education'), (b'5000', b'5000 - Medicine Dentistry and Health Sciences'), (b'5000', b'5000 - MDHS Faculty IT'), (b'5000', b'5000 - VLSCI'), (b'5010', b'5010 - Peter Doherty Institute'), (b'5040', b'5040 - Rural Health Academic Centre'), (b'5050', b'5050 - Melbourne School of Population and Global Health'), (b'5070', b'5070 - Centre for Youth Mental Health'), (b'5080', b'5080 - Centre for Neuroscience Research'), (b'5090', b'5090 - Nossal Institute for Global Health'), (b'5100', b'5100 - Melbourne Medical School'), (b'5110', b'5110 - Melbourne Dental School'), (b'5120', b'5120 - Melbourne School of Psychological Sciences'), (b'5130', b'5130 - Physiotherapy'), (b'5140', b'5140 - Nursing'), (b'5160', b'5160 - Anatomy and Neuroscience'), (b'5200', b'5200 - Otolaryngology'), (b'5210', b'5210 - Biochemistry and Molecular Biology'), (b'5260', b'5260 - Microbiology and Immunology'), (b'5270', b'5270 - MDU Microbiology'), (b'5300', b'5300 - School Of Biomedical Sciences'), (b'5310', b'5310 - Pathology'), (b'5340', b'5340 - Pharmacology and Therapeutics'), (b'5360', b'5360 - Physiology'), (b'5400', b'5400 - Austin Academic Centre'), (b'5430', b'5430 - Medicine - Austin Health'), (b'5460', b'5460 - Surgery - Austin Health'), (b'5480', b'5480 - Clinical School - Austin Health'), (b'5500', b'5500 - Royal Melbourne Hospital Academic Centre'), (b'5510', b'5510 - Medical Education'), (b'5520', b'5520 - Surgery'), (b'5530', b'5530 - Medicine Royal Melbourne Hospital'), (b'5540', b'5540 - Psychiatry'), (b'5550', b'5550 - Radiology'), (b'5560', b'5560 - Surgery - Royal Melbourne Hospital'), (b'5570', b'5570 - Medicine and Radiology'), (b'5580', b'5580 - Clinical School - Royal Melbourne Hospital'), (b'5600', b'5600 - Eastern Hill Academic Centre'), (b'5630', b"5630 - Medicine - St Vincent's Hospital"), (b'5660', b"5660 - Surgery - St Vincent's Hospital"), (b'5680', b"5680 - Clinical School - St Vincent's Hospital"), (b'5700', b'5700 - School of Health Sciences'), (b'5710', b"5710 - Paediatrics Royal Children's Hospital"), (b'5760', b'5760 - Ophthalmology Eye and Ear Hospital'), (b'5770', b'5770 - Audiology and Speech Pathology'), (b'5790', b"5790 - Obstetrics and Gynaecology Royal Women's Hospital"), (b'5850', b'5850 - General Practice'), (b'5870', b'5870 - Rural Clinical School'), (b'5900', b'5900 - North West Academic Centre'), (b'5950', b'5950 - Clinical and Biomedical Sciences'), (b'5970', b'5970 - Medical Biology (W.E.H.I)'), (b'6030', b'6030 - Science, Faculty Secretariat'), (b'6040', b'6040 - Australian Mathematical Sciences Institute'), (b'6100', b'6100 - Chemistry'), (b'6150', b'6150 - Information Systems - HISTORICAL'), (b'6200', b'6200 - Mathematics and Statistics'), (b'6250', b'6250 - Earth Sciences'), (b'6300', b'6300 - School of Biosciences'), (b'6400', b'6400 - Physics'), (b'6500', b'6500 - Biology Laboratory'), (b'6550', b'6550 - Optometry and Vision Sciences'), (b'7020', b'7020 - Architecture, Building and Planning'), (b'7320', b'7320 - Law'), (b'7410', b'7410 - VCA and MCM'), (b'7420', b'7420 - Melbourne Conservatorium of Music'), (b'7500', b'7500 - Victorian College of the Arts'), (b'7890', b'7890 - Bio21 Institute'), (b'8130', b'8130 - Melbourne University of Publishing'), (b'8140', b'8140 - Grattan Institute'), (b'8240', b'8240 - Medley Hall'), (b'8300', b'8300 - Application Services'), (b'8490', b'8490 - Melbourne University Sport'), (b'8650', b'8650 - CERA Ltd'), (b'8670', b'8670 - Bio21 Australia Ltd'), (b'8800', b"8800 - Children's Services"), (b'8840', b'8840 - Nossal Institute Ltd'), (b'9110', b'9110 - Australian Music Examinations'), (b'9310', b'9310 - Administration and Finance'), (b'9320', b'9320 - Engagement'), (b'9330', b'9330 - Policy and Projects'), (b'9330', b'9330 - Carlton Connect'), (b'9340', b'9340 - Provost'), (b'9340', b'9340 - Murrup Barak Institute'), (b'9350', b'9350 - Research'), (b'9510', b'9510 - Sir Peter MacCullum - Department of Oncology'), (b'9520', b'9520 - Florey Department of Neuroscience and Mental Health'), (b'9560', b'9560 - Medical Bionics Department'), (b'9700', b'9700 - University Services'), (b'9710', b'9710 - Research, Industry & Commercialisation '), (b'9720', b'9720 - University Procurement'), (b'9730', b'9730 - Academic Services'), (b'9730', b'9730 - Research and Collections'), (b'9730', b'9730 - Scholarly Information'), (b'9730', b'9730 - Learning Environments'), (b'9740', b'9740 - Business Intelligence & Reporting'), (b'9750', b'9750 - External Relations'), (b'9760', b'9760 - Finance & Employee Services'), (b'9770', b'9770 - Infrastructure Services'), (b'9780', b'9780 - Legal Services & Governance'), (b'9790', b'9790 - Project Services')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_dept',
            field=models.CharField(help_text=b'Select the department you belong to.\n                  <br><br>If you cannot find your department, school\n                  or faculty listed here, please select "0000 -\n                  University General".\n                  ', max_length=255, null=True, verbose_name=b'Your department', choices=[(b'0000', b'0000 - University General'), (b'0060', b"0060 - Vice-Chancellor's Office"), (b'0380', b'0380 - The Ian Potter Museum of Art'), (b'0920', b'0920 - Asialink'), (b'0950', b'0950 - Advancement'), (b'1000', b'1000 - Arts'), (b'1030', b'1030 - Arts Business Centre'), (b'1060', b'1060 - Culture and Communication'), (b'1100', b'1100 - Asia Institute'), (b'1120', b'1120 - Arts & Music Student Centre'), (b'1140', b'1140 - Graduate School of Humanities and Social Sciences'), (b'1190', b'1190 - School of Language and Linguistics'), (b'1310', b'1310 - School of Historical and Philosophical Studies'), (b'1510', b'1510 - Melbourne School of Government'), (b'1660', b'1660 - School of Social and Political Sciences'), (b'1942', b'1942 - Australian Mathematical Sciences Institute'), (b'1960', b'1960 - Social Work'), (b'2070', b'2070 - Resource Management and Geography'), (b'2080', b'2080 - Agriculture and Food Systems'), (b'2200', b'2200 - Forest and Ecosystem Science'), (b'2510', b'2510 - Veterinary and Agricultural Sciences Faculty'), (b'2860', b'2860 - Veterinary Hospital'), (b'3000', b'3000 - Faculty of Business and Economics'), (b'3040', b'3040 - Graduate School of Business and Economics'), (b'3060', b'3060 - Accounting'), (b'3160', b'3160 - Economics'), (b'3200', b'3200 - Business Administration'), (b'3250', b'3250 - Management & Marketing'), (b'3330', b'3330 - Finance'), (b'3360', b'3360 - Melbourne Institute of Applied Economic and Social Research'), (b'3510', b'3510 - The Melbourne Business School'), (b'4000', b'4000 - Engineering'), (b'4110', b'4110 - Chemical and Biomolecular Engineering'), (b'4180', b'4180 - Computing and Information Systems'), (b'4310', b'4310 - Engineering and Electrical Engineering'), (b'4320', b'4320 - Infrastructure Engineering'), (b'4360', b'4360 - Mechanical Engineering'), (b'4600', b'4600 - Melbourne Graduate School of Education'), (b'5000', b'5000 - Medicine Dentistry and Health Sciences'), (b'5000', b'5000 - MDHS Faculty IT'), (b'5000', b'5000 - VLSCI'), (b'5010', b'5010 - Peter Doherty Institute'), (b'5040', b'5040 - Rural Health Academic Centre'), (b'5050', b'5050 - Melbourne School of Population and Global Health'), (b'5070', b'5070 - Centre for Youth Mental Health'), (b'5080', b'5080 - Centre for Neuroscience Research'), (b'5090', b'5090 - Nossal Institute for Global Health'), (b'5100', b'5100 - Melbourne Medical School'), (b'5110', b'5110 - Melbourne Dental School'), (b'5120', b'5120 - Melbourne School of Psychological Sciences'), (b'5130', b'5130 - Physiotherapy'), (b'5140', b'5140 - Nursing'), (b'5160', b'5160 - Anatomy and Neuroscience'), (b'5200', b'5200 - Otolaryngology'), (b'5210', b'5210 - Biochemistry and Molecular Biology'), (b'5260', b'5260 - Microbiology and Immunology'), (b'5270', b'5270 - MDU Microbiology'), (b'5300', b'5300 - School Of Biomedical Sciences'), (b'5310', b'5310 - Pathology'), (b'5340', b'5340 - Pharmacology and Therapeutics'), (b'5360', b'5360 - Physiology'), (b'5400', b'5400 - Austin Academic Centre'), (b'5430', b'5430 - Medicine - Austin Health'), (b'5460', b'5460 - Surgery - Austin Health'), (b'5480', b'5480 - Clinical School - Austin Health'), (b'5500', b'5500 - Royal Melbourne Hospital Academic Centre'), (b'5510', b'5510 - Medical Education'), (b'5520', b'5520 - Surgery'), (b'5530', b'5530 - Medicine Royal Melbourne Hospital'), (b'5540', b'5540 - Psychiatry'), (b'5550', b'5550 - Radiology'), (b'5560', b'5560 - Surgery - Royal Melbourne Hospital'), (b'5570', b'5570 - Medicine and Radiology'), (b'5580', b'5580 - Clinical School - Royal Melbourne Hospital'), (b'5600', b'5600 - Eastern Hill Academic Centre'), (b'5630', b"5630 - Medicine - St Vincent's Hospital"), (b'5660', b"5660 - Surgery - St Vincent's Hospital"), (b'5680', b"5680 - Clinical School - St Vincent's Hospital"), (b'5700', b'5700 - School of Health Sciences'), (b'5710', b"5710 - Paediatrics Royal Children's Hospital"), (b'5760', b'5760 - Ophthalmology Eye and Ear Hospital'), (b'5770', b'5770 - Audiology and Speech Pathology'), (b'5790', b"5790 - Obstetrics and Gynaecology Royal Women's Hospital"), (b'5850', b'5850 - General Practice'), (b'5870', b'5870 - Rural Clinical School'), (b'5900', b'5900 - North West Academic Centre'), (b'5950', b'5950 - Clinical and Biomedical Sciences'), (b'5970', b'5970 - Medical Biology (W.E.H.I)'), (b'6030', b'6030 - Science, Faculty Secretariat'), (b'6040', b'6040 - Australian Mathematical Sciences Institute'), (b'6100', b'6100 - Chemistry'), (b'6150', b'6150 - Information Systems - HISTORICAL'), (b'6200', b'6200 - Mathematics and Statistics'), (b'6250', b'6250 - Earth Sciences'), (b'6300', b'6300 - School of Biosciences'), (b'6400', b'6400 - Physics'), (b'6500', b'6500 - Biology Laboratory'), (b'6550', b'6550 - Optometry and Vision Sciences'), (b'7020', b'7020 - Architecture, Building and Planning'), (b'7320', b'7320 - Law'), (b'7410', b'7410 - VCA and MCM'), (b'7420', b'7420 - Melbourne Conservatorium of Music'), (b'7500', b'7500 - Victorian College of the Arts'), (b'7890', b'7890 - Bio21 Institute'), (b'8130', b'8130 - Melbourne University of Publishing'), (b'8140', b'8140 - Grattan Institute'), (b'8240', b'8240 - Medley Hall'), (b'8300', b'8300 - Application Services'), (b'8490', b'8490 - Melbourne University Sport'), (b'8650', b'8650 - CERA Ltd'), (b'8670', b'8670 - Bio21 Australia Ltd'), (b'8800', b"8800 - Children's Services"), (b'8840', b'8840 - Nossal Institute Ltd'), (b'9110', b'9110 - Australian Music Examinations'), (b'9310', b'9310 - Administration and Finance'), (b'9320', b'9320 - Engagement'), (b'9330', b'9330 - Policy and Projects'), (b'9330', b'9330 - Carlton Connect'), (b'9340', b'9340 - Provost'), (b'9340', b'9340 - Murrup Barak Institute'), (b'9350', b'9350 - Research'), (b'9510', b'9510 - Sir Peter MacCullum - Department of Oncology'), (b'9520', b'9520 - Florey Department of Neuroscience and Mental Health'), (b'9560', b'9560 - Medical Bionics Department'), (b'9700', b'9700 - University Services'), (b'9710', b'9710 - Research, Industry & Commercialisation '), (b'9720', b'9720 - University Procurement'), (b'9730', b'9730 - Academic Services'), (b'9730', b'9730 - Research and Collections'), (b'9730', b'9730 - Scholarly Information'), (b'9730', b'9730 - Learning Environments'), (b'9740', b'9740 - Business Intelligence & Reporting'), (b'9750', b'9750 - External Relations'), (b'9760', b'9760 - Finance & Employee Services'), (b'9770', b'9770 - Infrastructure Services'), (b'9780', b'9780 - Legal Services & Governance'), (b'9790', b'9790 - Project Services')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_given_name',
            field=models.CharField(help_text=b'Your given name.', max_length=255, null=True, verbose_name=b'Given name'),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_is_ci',
            field=models.CharField(help_text=b"Please select 'Yes' if you are the Chief\n            Investigator.<ul><li>For research projects this is the first\n            investigator.</li><li>For higher degree research projects this is\n            the primary supervisor.</li><li>For other activities this is the\n            academic sponsor or head of the managing organisation unit.</li>\n            </ul>", max_length=255, null=True, verbose_name=b'Are you the Chief Investigator?', choices=[(b'yes', b'Yes'), (b'no', b'No')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_phone',
            field=models.CharField(help_text=b'Your preferred contact phone number.', max_length=255, null=True, verbose_name=b'Contact phone number'),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_role',
            field=models.CharField(help_text=b'Select the category that best fits your role in\n            this project.', max_length=255, null=True, verbose_name=b'Your role', choices=[(b'researcher', b'Researcher'), (b'student-research', b'Student - Masters/PhD by Research'), (b'student-coursework', b'Student - Masters by Coursework'), (b'student-undergraduate', b'Student - Undergraduate'), (b'technical-support-staff', b'Technical support staff'), (b'other', b'Other')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_surname',
            field=models.CharField(help_text=b'Your surname.', max_length=255, null=True, verbose_name=b'Surname'),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='requester_title',
            field=models.CharField(help_text=b'Your title.', max_length=60, null=True, verbose_name=b'Title'),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='use_category',
            field=models.CharField(help_text=b'Select the category that this project is primarily for.', max_length=255, null=True, verbose_name=b'Category of work', choices=[(b'research', b'Research'), (b'teaching', b'Teaching/Training'), (b'support', b'Support/Other')]),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='use_other',
            field=models.TextField(help_text=b'e.g. AWS, Google compute, Nectar, other NCRIS platforms,\n            ...', max_length=1024, verbose_name=b'List other capabilities you use/intend to use with this project', blank=True),
        ),
        migrations.AddField(
            model_name='servicetype',
            name='index',
            field=models.IntegerField(default=99),
        ),
        migrations.AddField(
            model_name='servicetype',
            name='required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='allocation_home',
            field=models.CharField(default=b'uom', help_text=b'You can provide a primary location where you expect to\n                use most resources, effectively the main Nectar site for your\n                allocation. Use of other locations is still possible.\n                This can also indicate a specific arrangement with a\n                Nectar site, for example where you obtain support, or if\n                your institution is a supporting member of that site.\n                Select unassigned if you have no preference.\n                ', max_length=128, verbose_name=b'Allocation home location', choices=[(b'national', b'Unassigned'), (b'nci', b'Australian Capital Territory (NCI)'), (b'intersect', b'New South Wales (Intersect)'), (b'qcif', b'Queensland (QCIF)'), (b'ersa', b'South Australia (eRSA)'), (b'tpac', b'Tasmania (TPAC)'), (b'uom', b'Victoria (Melbourne)'), (b'monash', b'Victoria (Monash)'), (b'swinburne', b'Victoria (Swinburne)'), (b'auckland', b'Auckland Uni (New Zealand)')]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='contact_email',
            field=models.EmailField(help_text=b'Please verify that this e-mail address is current and\n            accessible. It will be used to communicate with you about this\n            allocation request.<br><br><strong>Note:</strong> <i>If this is not\n            a valid email address you will not receive communications on any\n            allocation request you make</i>. If invalid please submit a support\n            ticket in ServiceNow (link provided in top navigation bar).', max_length=254, verbose_name=b'Contact e-mail', blank=True),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='estimated_number_users',
            field=models.IntegerField(default=b'1', help_text=b'Estimated number of users, researchers and collaborators\n        to be supported by the project.', error_messages={b'min_value': b'The estimated number of users must be great than 0'}, verbose_name=b'Estimated number of users', validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='estimated_project_duration',
            field=models.IntegerField(default=1, help_text=b'Resources are approved for 12 months at most,\n                    but projects can be extended once they have been\n                    approved.', verbose_name=b'Estimated project duration', choices=[(1, b'1-month'), (3, b'3-months'), (6, b'6-months'), (12, b'12-months')]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='for_percentage_1',
            field=models.IntegerField(default=100, help_text=b'The percentage', blank=True, choices=[(0, b'0%'), (10, b'10%'), (20, b'20%'), (30, b'30%'), (40, b'40%'), (50, b'50%'), (60, b'60%'), (70, b'70%'), (80, b'80%'), (90, b'90%'), (100, b'100%')]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='for_percentage_2',
            field=models.IntegerField(default=0, help_text=b'The percentage', blank=True, choices=[(0, b'0%'), (10, b'10%'), (20, b'20%'), (30, b'30%'), (40, b'40%'), (50, b'50%'), (60, b'60%'), (70, b'70%'), (80, b'80%'), (90, b'90%'), (100, b'100%')]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='for_percentage_3',
            field=models.IntegerField(default=0, blank=True, choices=[(0, b'0%'), (10, b'10%'), (20, b'20%'), (30, b'30%'), (40, b'40%'), (50, b'50%'), (60, b'60%'), (70, b'70%'), (80, b'80%'), (90, b'90%'), (100, b'100%')]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='funding_national_percent',
            field=models.IntegerField(default=b'0', help_text=b'Percentage funded under the National\n                    Allocation Scheme.', error_messages={b'max_value': b'The maximum percent is 100', b'min_value': b'The minimum percent is 0'}, verbose_name=b'Nationally Funded Percentage [0..100]', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='funding_node',
            field=models.CharField(default=b'uom', choices=[(b'nci', b'Australian Capital Territory (NCI)'), (b'intersect', b'New South Wales (Intersect)'), (b'qcif', b'Queensland (QCIF)'), (b'ersa', b'South Australia (eRSA)'), (b'tpac', b'Tasmania (TPAC)'), (b'uom', b'Victoria (Melbourne)'), (b'monash', b'Victoria (Monash)'), (b'swinburne', b'Victoria (Swinburne)'), (b'auckland', b'Auckland Uni (New Zealand)')], max_length=128, blank=True, help_text=b'You can choose the node that complements\n                    the National Funding.', null=True, verbose_name=b'Node Funding Remainder (if applicable)'),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='geographic_requirements',
            field=models.TextField(help_text=b'Describe any special requirements you need for your\n                     project. For example geographical location,\n                     high-memory nodes, or GPU enable nodes.', max_length=1024, verbose_name=b'Special requirements', blank=True),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='ncris_support',
            field=models.CharField(help_text=b'List the names of any NCRIS capabilities supporting this\n            request.', max_length=255, verbose_name=b'List any NCRIS capabilities supporting this request.', blank=True),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='nectar_support',
            field=models.CharField(help_text=b'List the names of any ARDC funded projects.<br><br><strong>\n            Note:</strong> On 1 July 2018 ANDS, Nectar and RDS combined to form\n            the Australian Research Data Commons (ARDC).', max_length=255, verbose_name=b'List any ARDC (formerly ANDS, Nectar and RDS) funded projects\n        supporting this request.', blank=True),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='project_description',
            field=models.CharField(help_text=b'A human-friendly descriptive name for your project.', max_length=200, verbose_name=b'Project allocation title'),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='start_date',
            field=models.DateField(default=datetime.date.today, help_text=b'The day on which you want your project\n            allocation to go live. Format: YYYY-MM-DD.', verbose_name=b'Start date'),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='usage_patterns',
            field=models.TextField(help_text=b'Will your project have many users and small data sets?\n                     Or will it have large data sets with a small number of\n                     users? Will your instances be long running or created\n                     and deleted as needed? <br>\n                     Your answers here will help validate the Instances,\n                     Object Storage and Volume Storages is right for the\n                     project.', max_length=1024, verbose_name=b'Instance, Object Storage and Volumes Storage Usage Patterns', blank=True),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='use_case',
            field=models.TextField(help_text=b'Provide a very brief overview of your project, and how\n                     you will use the cloud to support it.', max_length=4096, verbose_name=b'Use case'),
        ),
        migrations.AlterField(
            model_name='chiefinvestigator',
            name='additional_researchers',
            field=models.TextField(default=b'', help_text=b'Include full names, and the name of their Research\n                     Institution, University or Organisation they\n                     belong to.', max_length=1000, verbose_name=b'Please list all other primary investigators, partner investigators and other research collaborators', blank=True),
        ),
        migrations.AlterField(
            model_name='chiefinvestigator',
            name='email',
            field=models.EmailField(help_text=b"Chief Investigator's institutional email address.", max_length=254, verbose_name=b'Institutional email address'),
        ),
        migrations.AlterField(
            model_name='chiefinvestigator',
            name='institution',
            field=models.CharField(default=b'', help_text=b'The name of the institution or university of\n                    the chief investigator including the schools,\n                    faculty and/or department.', max_length=200, verbose_name=b'Institution', blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(default=b'The University of Melbourne', help_text=b'List one or more Research Institutions and Universities\n                     this project intends to collaborate with. <br>\n                     If this project is just for you, write the name of the\n                     your Reserarch Institution or University. <br>\n                     If you are running a public web service, list the\n                     Research Institutions and Universities that will benefit\n                     the most.', max_length=200, verbose_name=b'Collaborating institutions'),
        ),
    ]

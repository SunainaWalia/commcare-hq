# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-31 20:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0159_update_agg_awc_monthly_view_visit_fields'),
    ]

    operations = [
        migrations.RunSQL('DROP INDEX CONCURRENTLY IF EXISTS "icds_dashboard_growth_monitoring_forms_case_id_ddb22a97_like"'),
        migrations.RunSQL('DROP INDEX CONCURRENTLY IF EXISTS "icds_dashboard_daily_feeding_forms_case_id_114445ac_like"'),
        migrations.RunSQL('DROP INDEX CONCURRENTLY IF EXISTS "icds_dashboard_ccs_record_cf_forms_case_id_c4e821f9_like"'),
        migrations.RunSQL('DROP INDEX CONCURRENTLY IF EXISTS "icds_dashboard_ccs_record_bp_forms_case_id_766b782e_like"'),
        migrations.RunSQL('DROP INDEX CONCURRENTLY IF EXISTS "icds_dashboard_ccs_record_postnatal_forms_case_id_d83b4f04_like"'),
        migrations.RunSQL('DROP INDEX CONCURRENTLY IF EXISTS "icds_dashboard_child_hea_case_id_e6c43f67_like"'),
        migrations.RunSQL('DROP INDEX CONCURRENTLY IF EXISTS "icds_dashboard_comp_feed_form_case_id_3c67578e_like"'),
    ]

from django.db import migrations, models


def backfill_payment_status(apps, schema_editor):
    Customer = apps.get_model('gymapp', 'Customer')
    # If the legacy 'active' column exists, use it to set a human-readable payment_status.
    # Some rows may not have 'active' accessible via the historical model API; guard accordingly.
    try:
        qs_active = Customer.objects.filter(active=True)
        qs_active.update(payment_status='Active')
        qs_inactive = Customer.objects.filter(active=False)
        qs_inactive.update(payment_status='Inactive')
    except Exception:
        # If active isn't present or something goes wrong, leave default 'Pending'.
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0003_rename_legacy_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer', old_name='full_name', new_name='name'
        ),
        migrations.RenameField(
            model_name='customer', old_name='contact_no', new_name='mobile_number'
        ),
        migrations.RenameField(
            model_name='customer', old_name='dob', new_name='date_of_birth'
        ),
        migrations.RenameField(
            model_name='customer', old_name='height_ft', new_name='height'
        ),
        migrations.RenameField(
            model_name='customer', old_name='weight_kg', new_name='weight'
        ),
        migrations.RenameField(
            model_name='customer', old_name='date_enrolled', new_name='enrolled_on'
        ),
        migrations.RenameField(
            model_name='customer', old_name='date_expiry', new_name='expiry_date'
        ),
        migrations.RenameField(
            model_name='customer', old_name='medicalissues', new_name='medical_notes'
        ),
        migrations.RenameField(
            model_name='customer', old_name='biometric_data', new_name='attendance_history'
        ),
        migrations.RenameField(
            model_name='customer', old_name='timeslot', new_name='time_slot'
        ),

        # Add payment_status field with default; we'll backfill from legacy 'active' boolean.
        migrations.AddField(
            model_name='customer',
            name='payment_status',
            field=models.CharField(max_length=100, default='Pending'),
        ),

        migrations.RunPython(backfill_payment_status, reverse_code=migrations.RunPython.noop),
    ]

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0002_backfill_payment_customer'),
    ]

    operations = [
        # Inventory -> Equipment
        migrations.RenameModel(
            old_name='Inventory',
            new_name='Equipment',
        ),
        # Rename Inventory fields to Equipment equivalents
        migrations.RenameField(
            model_name='equipment',
            old_name='total_no',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='notes',
            new_name='description',
        ),

        # MembershipPlan: name -> plan_name, validity_months -> validity_days, amount -> price
        migrations.RenameField(
            model_name='membershipplan',
            old_name='name',
            new_name='plan_name',
        ),
        migrations.RenameField(
            model_name='membershipplan',
            old_name='validity_months',
            new_name='validity_days',
        ),
        migrations.RenameField(
            model_name='membershipplan',
            old_name='amount',
            new_name='price',
        ),

        # Payment: price -> amount, created_at -> paid_on
        migrations.RenameField(
            model_name='payment',
            old_name='price',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='created_at',
            new_name='paid_on',
        ),
    ]

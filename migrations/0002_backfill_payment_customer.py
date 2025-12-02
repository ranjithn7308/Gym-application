from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0001_initial'),
    ]

    operations = [
        # Rename historical model 'Member' -> 'Customer' to match current models.py
        migrations.RenameModel(
            old_name='Member',
            new_name='Customer',
        ),
        # Rename Payment.member field to Payment.customer
        migrations.RenameField(
            model_name='payment',
            old_name='member',
            new_name='customer',
        ),
    ]

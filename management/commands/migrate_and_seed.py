from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run makemigrations, migrate and seed sample data for development.'

    def handle(self, *args, **options):
        self.stdout.write('Running makemigrations for gymapp...')
        call_command('makemigrations', 'gymapp')
        self.stdout.write('Applying migrations...')
        call_command('migrate')

        # Seed sample data if not present
        from gymapp.models import MembershipPlan, Member
        if not MembershipPlan.objects.exists():
            self.stdout.write('Seeding sample membership plans...')
            MembershipPlan.objects.create(name='Monthly', validity_months=1, amount=1299)
            MembershipPlan.objects.create(name='Quarterly', validity_months=3, amount=3000)
            MembershipPlan.objects.create(name='6Months', validity_months=6, amount=5000)

        if not Member.objects.exists():
            self.stdout.write('Seeding a sample member...')
            plan = MembershipPlan.objects.first()
            Member.objects.create(
                full_name='Vishwa Example',
                member_id='001vishwa',
                email='vishwa@example.com',
                contact_no='9999999999',
                plan=plan,
            )

        self.stdout.write(self.style.SUCCESS('Migrations applied and sample data seeded.'))

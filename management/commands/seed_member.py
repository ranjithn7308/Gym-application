from django.core.management.base import BaseCommand
from gymapp.models import Member, MembershipPlan
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed a test member (if none exists)'

    def handle(self, *args, **options):
        if Member.objects.exists():
            self.stdout.write(self.style.WARNING('Members already exist — skipping.'))
            return

        plan = MembershipPlan.objects.first()
        member = Member(
            full_name='Test Member',
            email='testmember@example.com',
            contact_no='0000000000',
            dob=timezone.now().date(),
            plan=plan,
        )
        member.save()
        self.stdout.write(self.style.SUCCESS(f'Created member {member.member_id}'))

from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        # Delete only objects with id not None to avoid unhashable primary key errors
        for model in [Activity, Workout, Leaderboard, User, Team]:
            model.objects.exclude(id=None).delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create Users
        users_data = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': dc, 'is_superhero': True},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': dc, 'is_superhero': True},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': dc, 'is_superhero': True},
        ]
        for user_data in users_data:
            User.objects.create(**user_data)

        # Create Activities
        for user in User.objects.all():
            Activity.objects.create(user=user, type='Running', duration=30, date=timezone.now().date())
            Activity.objects.create(user=user, type='Cycling', duration=45, date=timezone.now().date())

        # Create Workouts
        workout1 = Workout.objects.create(name='Super Strength', description='Strength workout for superheroes')
        workout2 = Workout.objects.create(name='Agility Training', description='Agility workout for superheroes')
        workout1.suggested_for.set([marvel, dc])
        workout2.suggested_for.set([marvel, dc])

        # Create Leaderboards
        Leaderboard.objects.create(team=marvel, total_points=300)
        Leaderboard.objects.create(team=dc, total_points=250)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

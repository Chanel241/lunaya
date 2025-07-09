
from django.db import migrations

def load_initial_wellness_tips(apps, schema_editor):
    WellnessTip = apps.get_model('wellness', 'WellnessTip')
    WellnessTip.objects.create(
        title="Posture de la Lune Douce (Yoga)",
        description="Asseyez-vous en tailleur, placez une main sur votre cœur et l’autre sur votre ventre. Respirez lentement pendant 5 minutes pour apaiser votre esprit. Idéal pendant la pleine lune.",
        type="yoga"
    )
    WellnessTip.objects.create(
        title="Thé à l’Hibiscus",
        description="Faites infuser 2 cuillères de fleurs d’hibiscus séchées dans 1L d’eau chaude pendant 10 minutes. Ajoutez une touche de miel pour un moment apaisant.",
        type="tea"
    )
    WellnessTip.objects.create(
        title="Étirement du Baobab (Yoga)",
        description="Debout, levez les bras comme les branches d’un baobab, étirez-vous vers le ciel, puis penchez-vous doucement d’un côté à l’autre. Visualisez l’énergie de la terre gabonaise.",
        type="yoga"
    )
    WellnessTip.objects.create(
        title="Pause Respiration Calme",
        description="Allongez-vous avec une goutte d’huile de karité sur les poignets. Inspirez profondément pendant 4 secondes, retenez 4 secondes, expirez 6 secondes. Répétez 5 fois.",
        type="relaxation"
    )

class Migration(migrations.Migration):
    dependencies = [('wellness', '0001_initial')]
    operations = [migrations.RunPython(load_initial_wellness_tips)]
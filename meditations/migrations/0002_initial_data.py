from django.db import migrations

def load_initial_meditations(apps, schema_editor):
    Meditation = apps.get_model('meditations', 'Meditation')
    Meditation.objects.create(
        title="Énergie Féminine",
        language="fr",
        audio_file="meditations/energie_feminine.mp3"
    )
    Meditation.objects.create(
        title="Harmonie Lunaire",
        language="fg",
        audio_file="meditations/harmonie_lunaire_fg.mp3"
    )
    Meditation.objects.create(
        title="Connexion Ancestrale",
        language="fr",
        audio_file="meditations/connexion_ancestrale.mp3"
    )

class Migration(migrations.Migration):
    dependencies = [('meditations', '0001_initial')]
    operations = [migrations.RunPython(load_initial_meditations)]
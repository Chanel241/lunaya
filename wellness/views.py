from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WellnessTip
from datetime import date
import random
import logging

logger = logging.getLogger(__name__)

@login_required
def wellness_list(request):
    today = date.today()
    tips = WellnessTip.objects.filter(date=today)
    tip_types = ['yoga', 'tea', 'relaxation']
    predefined_tips = {
        'yoga': [
            {
                'title': 'Salutation au Soleil',
                'description': 'Commencez votre journée avec une série de salutations au soleil pour réveiller votre corps en douceur.',
                'steps': '1. Debout, inspirez en levant les bras. 2. Pliez-vous en avant en expirant. 3. Étirez une jambe en arrière, puis l’autre en position de planche. 4. Descendez en cobra, puis remontez en chien tête en bas. 5. Revenez en position initiale. Répétez 5 fois.',
                'duration': '10-15 minutes',
                'benefits': 'Améliore la flexibilité, tonifie le corps et booste l’énergie.'
            },
            {
                'title': 'Posture de l’Arbre',
                'description': 'Pratiquez la posture de l’arbre pour améliorer votre équilibre et votre concentration.',
                'steps': '1. Tenez-vous droit. 2. Placez un pied contre l’intérieur de la cuisse opposée. 3. Joignez les mains devant le cœur ou au-dessus de la tête. 4. Maintenez 30 secondes par jambe.',
                'duration': '5-10 minutes',
                'benefits': 'Renforce l’équilibre et la concentration mentale.'
            },
            {
                'title': 'Étirement du Chat',
                'description': 'Faites des étirements en posture du chat pour soulager les tensions dorsales.',
                'steps': '1. À quatre pattes, arrondissez le dos en expirant. 2. Creusez le dos en inspirant. 3. Répétez lentement 8-10 fois.',
                'duration': '5 minutes',
                'benefits': 'Soulage les tensions du dos et améliore la posture.'
            },
        ],
        'tea': [
            {
                'title': 'Thé à la Camomille',
                'description': 'Dégustez une infusion de camomille pour calmer vos nerfs et favoriser le sommeil.',
                'steps': '1. Faites bouillir 250 ml d’eau. 2. Ajoutez 1 cuillère à café de fleurs de camomille séchées. 3. Laissez infuser 5 minutes, puis filtrez. 4. Buvez chaud avant de dormir.',
                'duration': '10 minutes',
                'benefits': 'Réduit le stress et favorise un sommeil réparateur.'
            },
            {
                'title': 'Tisane de Mélisse',
                'description': 'Préparez une tisane de mélisse pour réduire le stress et améliorer votre humeur.',
                'steps': '1. Versez 200 ml d’eau chaude sur 1 cuillère à soupe de mélisse séchée. 2. Laissez infuser 7 minutes. 3. Filtrez et ajoutez du miel si désiré.',
                'duration': '10 minutes',
                'benefits': 'Apaise l’anxiété et améliore l’humeur.'
            },
        ],
        'relaxation': [
            {
                'title': 'Méditation Guidée',
                'description': 'Prenez 10 minutes pour une méditation guidée et reconnectez-vous à votre souffle.',
                'steps': '1. Asseyez-vous confortablement. 2. Fermez les yeux et inspirez profondément pendant 4 secondes. 3. Retenez votre souffle 4 secondes, puis expirez sur 6 secondes. 4. Répétez 10 cycles.',
                'duration': '10 minutes',
                'benefits': 'Réduit le stress et améliore la clarté mentale.'
            },
            {
                'title': 'Bain Relaxant',
                'description': 'Préparez un bain chaud avec des huiles essentielles de lavande pour vous détendre.',
                'steps': '1. Remplissez votre baignoire d’eau chaude. 2. Ajoutez 5-10 gouttes d’huile essentielle de lavande. 3. Trempez-vous 15-20 minutes avec une lumière tamisée.',
                'duration': '20 minutes',
                'benefits': 'Détend les muscles et apaise l’esprit.'
            },
        ],
    }

    if not tips.exists():
        for tip_type in tip_types:
            available_tips = predefined_tips.get(tip_type, [])
            if available_tips:
                selected_tip = random.choice(available_tips)
                WellnessTip.objects.create(
                    title=selected_tip['title'],
                    description=selected_tip['description'],
                    type=tip_type,
                    date=today,
                    steps=selected_tip['steps'],
                    duration=selected_tip['duration'],
                    benefits=selected_tip['benefits']
                )
                logger.info(f"Created wellness tip for {tip_type} on {today}: {selected_tip['title']}")
        tips = WellnessTip.objects.filter(date=today)

    return render(request, 'wellness/list.html', {'tips': tips})

def wellness_detail(request, tip_id):
    tip = get_object_or_404(WellnessTip, id=tip_id)
    return render(request, 'wellness/detail.html', {'tip': tip})
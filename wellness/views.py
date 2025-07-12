from django.shortcuts import render
from .models import WellnessTip
from datetime import date
import random
import logging

logger = logging.getLogger(__name__)

def wellness_list(request):
    today = date.today()
    tips = WellnessTip.objects.filter(date=today)
    tip_types = ['yoga', 'tea', 'relaxation']
    predefined_tips = {
        'yoga': [
            {'title': 'Salutation au Soleil', 'description': 'Commencez votre journée avec une série de salutations au soleil pour réveiller votre corps en douceur.'},
            {'title': 'Posture de l’Arbre', 'description': 'Pratiquez la posture de l’arbre pour améliorer votre équilibre et votre concentration.'},
            {'title': 'Étirement du Chat', 'description': 'Faites des étirements en posture du chat pour soulager les tensions dorsales.'},
            {'title': 'Respiration en Lotus', 'description': 'Asseyez-vous en position du lotus et pratiquez une respiration profonde pour vous recentrer.'},
            {'title': 'Chien Tête en Bas', 'description': 'Adoptez la posture du chien tête en bas pour étirer tout votre corps.'},
            {'title': 'Guerrier II', 'description': 'Renforcez vos jambes et votre confiance avec la posture du guerrier II.'},
            {'title': 'Savasana', 'description': 'Terminez votre séance par une relaxation en savasana pour apaiser votre esprit.'},
        ],
        'tea': [
            {'title': 'Thé à la Camomille', 'description': 'Dégustez une infusion de camomille pour calmer vos nerfs et favoriser le sommeil.'},
            {'title': 'Tisane de Mélisse', 'description': 'Préparez une tisane de mélisse pour réduire le stress et améliorer votre humeur.'},
            {'title': 'Thé Vert Sencha', 'description': 'Savourez un thé vert sencha pour un boost d’énergie douce et naturelle.'},
            {'title': 'Infusion de Menthe', 'description': 'Une infusion de menthe fraîche pour rafraîchir votre esprit et votre corps.'},
            {'title': 'Rooibos Vanillé', 'description': 'Détendez-vous avec un rooibos vanillé, sans caféine, pour une soirée paisible.'},
            {'title': 'Tisane de Lavande', 'description': 'Une tisane de lavande pour apaiser vos pensées et favoriser la relaxation.'},
            {'title': 'Thé au Gingembre', 'description': 'Boostez votre énergie avec une infusion de gingembre frais et citron.'},
        ],
        'relaxation': [
            {'title': 'Méditation Guidée', 'description': 'Prenez 10 minutes pour une méditation guidée et reconnectez-vous à votre souffle.'},
            {'title': 'Bain Relaxant', 'description': 'Préparez un bain chaud avec des huiles essentielles de lavande pour vous détendre.'},
            {'title': 'Écoute de la Nature', 'description': 'Marchez dans la nature et écoutez les sons apaisants des oiseaux ou du vent.'},
            {'title': 'Journal Intime', 'description': 'Écrivez vos pensées dans un journal pour libérer votre esprit.'},
            {'title': 'Respiration 4-7-8', 'description': 'Pratiquez la respiration 4-7-8 pour réduire l’anxiété et vous recentrer.'},
            {'title': 'Visualisation Positive', 'description': 'Imaginez un lieu paisible pour apaiser votre esprit et vos émotions.'},
            {'title': 'Étirements Doux', 'description': 'Faites des étirements doux pour relâcher les tensions physiques.'},
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
                    date=today
                )
                logger.info(f"Created wellness tip for {tip_type} on {today}: {selected_tip['title']}")
        tips = WellnessTip.objects.filter(date=today)

    return render(request, 'wellness/list.html', {'tips': tips})
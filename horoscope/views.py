from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Horoscope
from datetime import datetime, date
import requests
import logging
from deep_translator import GoogleTranslator
import os
import pytz
from urllib.parse import quote

logger = logging.getLogger(__name__)

@login_required
def horoscope_view(request):
    sign = request.GET.get('sign', 'aries').lower()
    today = date.today()
    current_datetime = datetime.now(pytz.timezone('Africa/Lagos')).strftime('%Y-%m-%dT%H:%M:%S+01:00')
    encoded_datetime = quote(current_datetime)
    horoscope = None
    error_message = None

    logger.info(f"Processing horoscope request for sign: {sign}, date: {today}")

    try:
        horoscope = Horoscope.objects.filter(sign=sign, date=today).first()
        if horoscope:
            logger.info(f"Horoscope found in database for {sign} on {today}: {horoscope.message[:50]}...")
    except Exception as e:
        logger.error(f"Database error for {sign}: {str(e)}")

    if not horoscope:
        try:
            access_token = os.getenv('PROKARELA_ACCESS_TOKEN')
            if not access_token:
                logger.error("No PROKARELA_ACCESS_TOKEN found")
                error_message = "Configuration de l’API manquante."
                raise ValueError("Missing PROKARELA_ACCESS_TOKEN")
            logger.info(f"Fetching horoscope from Prokerala API for sign: {sign}")
            response = requests.get(
                f'https://api.prokerala.com/v2/horoscope/daily?sign={sign}&datetime={encoded_datetime}',
                timeout=5,
                headers={
                    'User-Agent': 'Lunaya/1.0',
                    'Authorization': f'Bearer {access_token}'
                }
            )
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Prokerala API response: {data}")

            if data.get('status') == 'ok' and 'daily_prediction' in data.get('data', {}):
                prediction = data['data']['daily_prediction']['prediction']
                translated_message = GoogleTranslator(source='en', target='fr').translate(prediction)
                if translated_message and translated_message.strip():
                    horoscope = Horoscope.objects.create(
                        sign=sign,
                        date=today,
                        message=translated_message
                    )
                    logger.info(f"Horoscope created for {sign} on {today}: {translated_message[:50]}...")
                    error_message = None
                else:
                    logger.warning(f"Translation empty for {sign}")
                    error_message = "Erreur lors de la traduction."
            else:
                logger.warning(f"No valid prediction in Prokerala response for {sign}: {data}")
                error_message = "Aucun horoscope disponible via l’API."
        except requests.RequestException as e:
            logger.error(f"Prokerala API request failed for {sign}: {str(e)}")
            error_message = f"Impossible de se connecter à l’API: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error for {sign}: {str(e)}")
            error_message = "Erreur inattendue."

    if not horoscope and error_message:
        horoscope = Horoscope.objects.create(
            sign=sign,
            date=today,
            message=f"{sign.capitalize()}, une journée lumineuse vous attend !"
        )
        logger.info(f"Fallback horoscope created for {sign} on {today}")

    signs = [
        {'value': choice[0], 'label': choice[1]}
        for choice in Horoscope._meta.get_field('sign').choices
    ]

    context = {
        'horoscope': horoscope,
        'signs': signs,
        'selected_sign': sign,
        'today': today,
        'error_message': error_message
    }
    return render(request, 'horoscope/horoscope.html', context)
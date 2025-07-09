from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Horoscope
from datetime import date
import requests
import logging
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

@login_required
def horoscope_view(request):
    sign = request.GET.get('sign', 'aries')
    today = date.today()
    horoscope = None
    try:
        horoscope = Horoscope.objects.get(sign=sign, date=today)
        logger.info(f"Horoscope found in database for {sign} on {today}")
        # Vérifier si le message semble en anglais et retraduire si nécessaire
        if any(word in horoscope.message.lower() for word in ['dear', 'today', 'morning']):
            logger.info(f"Detected English horoscope for {sign}, forcing retranslation")
            horoscope.delete()
            horoscope = None
    except Horoscope.DoesNotExist:
        pass
    if not horoscope:
        try:
            logger.info(f"Fetching horoscope from Ohmanda API for sign: {sign}, date: {today}")
            response = requests.get(
                f'https://ohmanda.com/api/horoscope/{sign}/',
                timeout=5,
                headers={'User-Agent': 'Lunaya/1.0'}
            )
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Ohmanda API response: {data}")
            if 'horoscope' in data and data['horoscope']:
                try:
                    translated_message = GoogleTranslator(source='en', target='fr').translate(data['horoscope'])
                    if translated_message:
                        horoscope = Horoscope.objects.create(
                            sign=sign,
                            date=today,
                            message=translated_message
                        )
                        logger.info(f"Horoscope created for {sign} on {today} with translated message: {translated_message[:50]}...")
                    else:
                        logger.warning(f"Translation returned empty for {sign}")
                        horoscope = None
                except Exception as e:
                    logger.error(f"Translation error for {sign}: {str(e)}")
                    horoscope = None
            else:
                logger.warning(f"No valid 'horoscope' in Ohmanda API response for {sign}: {data}")
                horoscope = None
        except requests.RequestException as e:
            logger.error(f"Ohmanda API request failed for {sign}: {str(e)}")
            horoscope = None
    signs = [
        {'value': choice[0], 'label': choice[1]}
        for choice in Horoscope._meta.get_field('sign').choices
    ]
    return render(request, 'horoscope/horoscope.html', {
        'horoscope': horoscope,
        'signs': signs,
        'selected_sign': sign,
        'today': today,
        'error_message': 'Impossible de récupérer l’horoscope pour le moment. Veuillez réessayer plus tard.' if not horoscope else None
    })
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Pacific/Auckland"
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_FORMAT = "j F Y"

DATE_INPUT_FORMATS = (
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d/%m/%y",  # '25-10-2006', '25/10/2006', '25/10/06'
    "%Y-%m-%d",  # '2006-10-21'
    "%b %d %Y",
    "%b %d, %Y",  # 'Oct 25 2006', 'Oct 25, 2006'
    "%d %b %Y",
    "%d %b, %Y",  # '25 Oct 2006', '25 Oct, 2006'
    "%B %d %Y",
    "%B %d, %Y",  # 'October 25 2006', 'October 25, 2006'
    "%d %B %Y",
    "%d %B, %Y",  # '25 October 2006', '25 October, 2006'
)

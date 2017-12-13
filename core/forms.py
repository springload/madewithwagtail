from wagtail.wagtailforms.forms import FormBuilder
from wagtailcaptcha.forms import WagtailCaptchaFormBuilder

from core.utilities import has_recaptcha


class SubmitFormBuilder(WagtailCaptchaFormBuilder if has_recaptcha() else FormBuilder):
    def get_form_class(self):
        form_class = super(SubmitFormBuilder, self).get_form_class()
        form_class.required_css_class = 'required'
        return form_class

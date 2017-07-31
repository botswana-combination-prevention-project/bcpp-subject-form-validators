from django.test import TestCase
from django.core.exceptions import ValidationError
from edc_registration.models import RegisteredSubject
from edc_constants.constants import MALE, YES

from .models import SubjectVisit

from ..form_validators import PimaVlFormValidator
from edc_base.utils import get_utcnow


class TestPimaCd4FormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    def test_location1(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES,
            location=None)
        form_validator = PimaVlFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)

    def test_location2(self):
        cleaned_data = dict(
            test_done=YES,
            location='Mmathethe',
            test_datetime=get_utcnow,
            easy_of_use=YES,
            stability=YES,
            subject_visit=self.subject_visit,)
        form_validator = PimaVlFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

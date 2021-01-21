from pigeon.module import Module
from faker import Faker
import random


class person(Module):
    options = {
    "locale": "en_GB"
    }
    strict_options = True

    def _init_(self):
        locale = self.options['locale']
        self.fake = Faker(locale)

    def create_age_and_birthdate(self, age=None, birth_date=None):
        pass

    def create_name_and_gender(self, gender=None, sex=None):
        gender = random.choice(
            [
                "male",
                "female",
                "non-binary"
            ]
        )
        sex = random.choice(  # hehe I wrote sex
            [
                "male",
                "female",
                "intersex"
            ]
        )
        # Faker has nonbinary methods, not non-binary methods, so we
        # Create a getattr friendly gender, replacing '-' with nothing.
        attr_friendly_gender = gender.replace('-', '')
        names = {}
        for name_type in ["first_name", "last_name", "suffix", "prefix"]:
            names['{}'.format(name_type)] = getattr(
                self.fake,
                "{}_{}".format(
                    name_type,
                    attr_friendly_gender
                    ))()
        # Create the identities
        # Create CIS people
        if gender == sex:
            identity = "cis-{}".format(gender)
        # Create Trans Men
        elif gender == "male" and sex == "female":
            identity = "trans-male"
        # Create Trans Women
        elif gender == "female" and sex == "male":
            identity = "trans-female"
        # Create intersex people
        # NOTE: Speak to intersex people about whether this is correct
        elif sex == "intersex":
            identity = "intersex-{}".format(gender)
        # Create non-binary people
        # NOTE: Speak to more non-binary people to confirm that this is correct.
        elif gender == "non-binary":
            identity = "non-binary"

        # Create the markers
        if gender == "non-binary":
            gender_marker = "NB"
        else:
            gender_marker = gender[0].capitalize()

        sex_marker = sex[0].capitalize()

        return {
         "gender": gender,
         "gender_marker": gender_marker,
         "sex": sex,
         "sex_marker": sex_marker,
         "identity": identity,
         **names
        }

    def execute(self, logger, row, variables, opt=None):
        name_and_gender =  self.create_name_and_gender()
        age_and_birthdate = self.create_age_and_birthdate()
        return {**name_and_gender}

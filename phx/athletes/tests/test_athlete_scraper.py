from itertools import groupby
from pathlib import Path

import responses
from athletes.athlete_scraper import AtheleteScraper
from athletes.models import Athlete
from django.test import TestCase
from faker import Faker

fake = Faker()


class TestAthleteScraper(TestCase):

    @responses.activate
    def test_handles_empty_results_page(self):
        self.setup_athletes([])
        scraper = AtheleteScraper()

        self.assertEqual([], scraper.find_by_surname('x'))

    @responses.activate
    def test_handles_non_empty_results_page(self):
        self.setup_athletes(["Jane Doe", "Steve Ovett"])

        scraper = AtheleteScraper()
        athletes = scraper.find_by_surname('o')

        self.assertEqual(len(athletes), 1)
        self.assertEqual(athletes[0].first_name, "Steve")
        self.assertEqual(athletes[0].last_name, "Ovett")

    @responses.activate
    def test_finds_all_athletes_by_first_letter_and_returns_count(self):
        self.setup_athletes(["Jane Doe", "John Smith", "Steve Ovett"])

        scraper = AtheleteScraper()

        self.assertEqual(scraper.find_athletes(), 3)

    @responses.activate
    def test_strips_whitespace_from_athlete_details(self):
        self.setup_athletes(["  Jane  Doe  "])

        scraper = AtheleteScraper()

        athletes = scraper.find_by_surname('d')
        self.assertEqual(athletes[0].first_name, "Jane")
        self.assertEqual(athletes[0].last_name, "Doe")

    @responses.activate
    def test_extracts_power_of_10_id_from_link(self):
        self.setup_athletes(["Jane Doe"])

        scraper = AtheleteScraper()

        athletes = scraper.find_by_surname('d')
        self.assertEqual(athletes[0].power_of_10_id, '8968')

    @responses.activate
    def test_stores_new_athletes_in_database(self):
        self.setup_athletes(["Jane Doe"])

        scraper = AtheleteScraper()

        scraper.find_athletes()
        scraper.save()

        results = Athlete.objects.all()
        self.assertEqual(1, results.count())
        self.assertEqual(["Jane"], list(map(lambda a: a.first_name, results)))

    @responses.activate
    def test_updates_existing_athletes_in_database(self):
        self.setup_athletes(["Jane Doe"])
        scraper = AtheleteScraper()

        scraper.find_athletes()
        scraper.save()

        self.setup_athletes(["Jane Doe", "John Smith"])
        scraper.find_athletes()
        # Updates two athletes
        self.assertEqual(2, scraper.save())

        results = Athlete.objects.all()

        # Does not create a second Jane Doe
        self.assertEqual(2, results.count())
        self.assertEqual(["Jane", "John"],
                         list(map(lambda a: a.first_name, results)))

    def setup_athletes(self, athletes, seed=1981):
        """
        Setup fake athletes for testing.

        Given a list of "First Last" athlete names, this method will setup
        fake responses for the Power of 10 athlete lookup page. The gender,
        age categories and power of 10 ids are randomly generated.
        """
        fake.seed_instance(seed)

        path = Path(__file__).with_name('test_body.html')
        template = path.read_text()

        # Group by first letter of surname
        for (letter, athletes) in groupby(athletes, lambda x: x.split()[1][0]):
            rows = ""
            for athlete in athletes:
                [first_name, last_name] = athlete.split()
                rows += """
                <tr>
                    <td>{first_name}</td>
                    <td>{last_name}</td>
                    <td>{age_category}</td>
                    <td>{age_category}</td>
                    <td>{age_category}</td>
                    <td>{gender}</td>
                    <td>Brighton Phoenix</td>
                    <td align="center">
                    <a href="profile.aspx?athleteid={power_of_10_id}">Show</a>
                    </td>
                    <td align="center">
                    <a href="https://www.runbritainrankings.com/""" \
                    """runners/profile.aspx?athleteid={power_of_10_id}">Show</a>
                    </td>
                </tr>
                """.format(first_name=first_name,
                           last_name=last_name,
                           age_category=fake.random_element(
                               ["U13", "SEN", "V35", "V50", "V60"]),
                           gender=fake.random_element(["M", "F"]),
                           power_of_10_id=fake.random_int())

            responses.get(
                "https://www.thepowerof10.info/athletes/athleteslookup.aspx?"
                "surname={letter}&firstname=&club=Brighton+Phoenix".format(
                    letter=letter.lower()),
                body=template.replace("{rows}", rows),
                content_type="text/plain",
                status=200,
            )

        # Default response for any other letter
        responses.get(
            "https://www.thepowerof10.info/athletes/athleteslookup.aspx",
            body=template.replace("{rows}", ""),
            content_type="text/plain",
            status=200,
        )

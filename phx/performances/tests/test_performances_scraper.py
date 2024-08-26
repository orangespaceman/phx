import datetime
from pathlib import Path

import responses
from athletes.models import Athlete
from django.test import TestCase
from faker import Faker
from performances.performances_scraper import PerformancesScraper

fake = Faker()


class TestPerformancesScraper(TestCase):

    @responses.activate
    def test_only_finds_performances_after_since_date(self):
        athlete = Athlete(power_of_10_id='1234',
                          created_date=datetime.datetime(2024, 1, 1))

        self.setup_profile_page([{
            "year":
            2024,
            "club":
            "Brighton Phoenix",
            "performances": [
                {
                    "date": "1 May 24",
                    "meeting_id": 1234
                },
                {
                    "date": "1 Apr 24",
                    "meeting_id": 5678
                },
            ]
        }])

        scraper = PerformancesScraper()

        count = scraper.find_performances(athlete, datetime.date(2024, 5, 1))

        self.assertEqual(1, count)
        self.assertEqual(1, len(scraper.events))
        self.assertEqual(1, len(scraper.performances))

    @responses.activate
    def test_only_finds_performances_after_athlete_created_date(self):
        athlete = Athlete(power_of_10_id='1234',
                          created_date=datetime.datetime(2024, 5, 1))

        self.setup_profile_page([{
            "year":
            2024,
            "club":
            "Brighton Phoenix",
            "performances": [
                {
                    "date": "1 May 24",
                    "meeting_id": 1234
                },
                {
                    "date": "1 Apr 24",
                    "meeting_id": 5678
                },
            ]
        }])

        scraper = PerformancesScraper()

        count = scraper.find_performances(athlete, datetime.date(2024, 1, 1))

        self.assertEqual(1, count)
        self.assertEqual(1, len(scraper.events))
        self.assertEqual(1, len(scraper.performances))

    @responses.activate
    def test_extracts_power_of_10_meeting_id_from_link(self):
        athlete = Athlete(power_of_10_id='1234',
                          created_date=datetime.datetime(2024, 5, 1))

        self.setup_profile_page([{
            "year":
            2024,
            "club":
            "Brighton Phoenix",
            "performances": [{
                "date": "1 May 24",
                "meeting_id": 5678
            }]
        }])

        scraper = PerformancesScraper()

        scraper.find_performances(athlete, datetime.date(2024, 1, 1))

        self.assertEqual('5678', scraper.events['5678'].power_of_10_meeting_id)

    @responses.activate
    def test_considers_athelete_with_no_recent_performances_inactive(self):
        athlete = Athlete(power_of_10_id='1234',
                          created_date=datetime.datetime(2024, 5, 1))

        self.setup_profile_page([{
            "year":
            2022,
            "club":
            "Brighton Phoenix",
            "performances": [{
                "date": "1 May 22",
                "meeting_id": 5678
            }]
        }])

        scraper = PerformancesScraper()

        count = scraper.find_performances(athlete, datetime.date(2024, 1, 1))

        self.assertEqual(0, count)
        self.assertListEqual(['1234'], list(scraper.inactive_athletes))

    @responses.activate
    def test_considers_athletes_that_now_compete_for_another_club_inactive(
            self):
        athlete = Athlete(power_of_10_id='1234',
                          created_date=datetime.datetime(2024, 5, 1))

        self.setup_profile_page([{
            "year":
            2024,
            "club":
            "Another Club AC",
            "performances": [{
                "date": "1 May 24",
                "meeting_id": 5678
            }]
        }])

        scraper = PerformancesScraper()

        count = scraper.find_performances(athlete, datetime.date(2024, 1, 1))

        self.assertEqual(0, count)
        self.assertListEqual(['1234'], list(scraper.inactive_athletes))

    @responses.activate
    def test_can_scrape_multiple_performances_at_same_event(self):
        scraper = PerformancesScraper()

        athlete_one = Athlete(power_of_10_id='1234',
                              created_date=datetime.datetime(2024, 5, 1))

        # First athlete competed in heat and final
        self.setup_profile_page([{
            "year":
            2024,
            "club":
            "Brighton Phoenix",
            "performances": [{
                "date": "1 May 24",
                "meeting_id": 9999,
                "round": "h1"
            }, {
                "date": "2 May 24",
                "meeting_id": 9999,
                "round": "f"
            }]
        }])

        count = scraper.find_performances(athlete_one,
                                          datetime.date(2024, 1, 1))

        self.assertEqual(2, count)
        self.assertEqual(1, len(scraper.events))
        self.assertEqual(2, len(scraper.performances))

        athlete_two = Athlete(power_of_10_id='5678',
                              created_date=datetime.datetime(2024, 5, 1))

        # Second athlete only competed in heat
        self.setup_profile_page([{
            "year":
            2024,
            "club":
            "Brighton Phoenix",
            "performances": [{
                "date": "1 May 24",
                "meeting_id": 9999,
                "round": "h1"
            }]
        }])

        count = scraper.find_performances(athlete_two,
                                          datetime.date(2024, 1, 1))

        self.assertEqual(1, count)
        self.assertEqual(1, len(scraper.events))
        self.assertEqual(3, len(scraper.performances))

    @responses.activate
    def test_ignores_parkruns(self):
        pass

    @responses.activate
    def test_save_stores_new_meetings_in_database(self):
        pass

    @responses.activate
    def test_save_stores_new_performances_in_database(self):
        pass

    @responses.activate
    def test_save_updates_existing_meetings_in_database(self):
        pass

    @responses.activate
    def test_save_updates_existing_performances_in_database(self):
        pass

    @responses.activate
    def test_save_updates_the_status_of_inactive_athletes(self):
        pass

    def setup_profile_page(self, performances):
        rows = []
        for group in performances:
            year = group['year']
            club = group['club']

            rows.append(f"""
                <tr style="background-color:DarkGray;">
                    <td colspan="12">
                        <a name="{year}"><b>{year} V35 {club}</b>
                    </td>
                </tr>
                """)

            rows.append("""
                <tr style="background-color:LightGrey;">
                    <td><b>Event</b></td>
                    <td><b>Perf</b></td>
                    <td></td><td></td>
                    <td></td>
                    <td><b>Pos</b></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td><b>Venue</b></td>
                    <td><b>Meeting</b></td>
                    <td align="right"><b>Date</b></td>
                </tr>
                """)

            for performance in group['performances']:
                meeting = performance.get("meeting", "Preston Park parkrun")
                meeting_date = performance.get("date", "1 Aug 24")
                meeting_id = performance.get("meeting_id", 1234)

                rows.append(f"""
                    <tr style="background-color:Gainsboro;">
                        <td>{performance.get("distance", "parkrun")}</td>
                        <td>{performance.get("time", "20:00")}</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>{performance.get("position", 1)}</td>
                        <td>{performance.get("round", "")}</td>
                        <td></td>
                        <td></td>
                        <td>
                            <a href="results.aspx?meetingid={meeting_id}">
                                {performance.get("location", "Preston Park")}
                            </a>
                        </td>
                        <td>{meeting}</td>
                        <td align="right">{meeting_date}</td>
                    </tr>
                    """)
        path = Path(__file__).with_name('test_body.html')

        responses.get("https://www.thepowerof10.info/athletes/profile.aspx",
                      body=path.read_text().replace("{rows}", ''.join(rows)),
                      content_type='text/plain',
                      status=200)

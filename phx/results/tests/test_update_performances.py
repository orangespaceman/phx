from datetime import datetime

import pytest
from results.jobs.hourly.update_performances import Job as UpdatePerformances


@pytest.mark.parametrize(
    "hour, fraction",
    [
        # between midnight and 6am no athletes should be checked
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 0),
        # between 6am and 10pm 1/16 of athletes should be checked each hour
        (6, 1 / 16),
        (7, 1 / 15),
        (8, 1 / 14),
        (9, 1 / 13),
        (10, 1 / 12),
        (11, 1 / 11),
        (12, 1 / 10),
        (13, 1 / 9),
        (14, 1 / 8),
        (15, 1 / 7),
        (16, 1 / 6),
        (17, 1 / 5),
        (18, 1 / 4),
        (19, 1 / 3),
        (20, 1 / 2),
        (21, 1 / 1),
        # after 10pm no athletes should be checked
        (22, 0),
        (23, 0)
    ])
def test_fraction_to_check(hour, fraction):

    time = datetime.now().replace(hour=hour)

    assert UpdatePerformances.fraction_to_check(time) == fraction

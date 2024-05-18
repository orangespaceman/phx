from django_extensions.management.jobs import WeeklyJob
from datetime import datetime

from results.results_processor import ResultsProcessor


class Job(WeeklyJob):
    help = "Prepare results spreadsheet for manual entry."

    def execute(self):
        [curr_file, prev_file] = ResultsProcessor.fetch_results(2)

        processor = ResultsProcessor()
        processor.process(curr_file, prev_file)

        filename = datetime.today().strftime("results/NewResults_%Y-%m-%d.xlsx")
        processor.save(filename)

        # TODO: email file to results crew

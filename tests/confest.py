def pytest_report_teststatus(report, config):
    if report.passed and report.when == 'call':
        return report.outcome, '', report.outcome.upper()

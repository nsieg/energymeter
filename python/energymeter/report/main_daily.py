import daily
from energymeter.util import main_helper

def main_report(props,tele):
    reporter = daily.Reporter(props,tele)
    reporter.report()

main_helper.main(main_report, "report")

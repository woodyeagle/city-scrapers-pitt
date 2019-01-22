# City Scrapers Template

Template repo for running a [City Scrapers](https://cityscrapers.org) project in your area.

## Setup

- Fork this repo to your GitHub account or organization account. Feel free to change the name to something specific to your area (i.e. `city-scrapers-il` for scrapers in Illinois).
- [Fill out this form](https://airtable.com/shrsdRcYVzp019U22) to join our [Slack channel](https://citybureau.slack.com/#labs_city_scrapers)
- Update `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `README.md` with your organization's information.
- Enable Travis CI at [travisci.org](https://travisci.org/)
- Setup deployment
  - Setup a daily cronjob on Travis CI to run the scrapers nightly [see instructions](https://docs.travis-ci.com/user/cron-jobs/)
  - Setup Azure or S3, on own or with us (give contact)
  - Enable settings, configure in Travis depending on provider used
- Setup Sentry
- Refer to our documentation on [getting started with development](https://cityscrapers.org/docs/development/)

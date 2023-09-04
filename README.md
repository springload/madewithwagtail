[Made with Wagtail](http://madewithwagtail.org) [![Codeship Status for springload/madewithwagtail](https://codeship.com/projects/26741250-da6d-0132-ea89-328081b30bed/status?branch=master)](https://codeship.com/projects/79308) [<img src="https://github.com/torchbox/wagtail/blob/82171f70faaf0c8b8da278261e6f45fed529c899/docs/logo.png" width="83" align="right" alt="Wagtail">](https://wagtail.io/)
=================

> A showcase of sites and apps made with [Wagtail](https://wagtail.io/): an easy to use, open source content management system from [Torchbox](https://github.com/torchbox/wagtail).

*Check out [Awesome Wagtail](https://github.com/springload/awesome-wagtail) for more awesome packages and resources from the Wagtail community.*

## Back End Setup

Development on this project can be done using docker. If you have not yet
installed docker, consult the instructions for your operating system.

[Docker](https://docs.docker.com/)

It's a good idea to set up the nginx proxy if you have not done so already,
instructions can be found on the github repo.

Vagrant is no longer in this project, and any material relating to vagrant
can be ignored.

## Clone the repo

```sh
cd [my-dev-environment]
git clone git@github.com:springload/madewithwagtail.git
cd madewithwagtail
```
### Setup your environment variables

```sh
cp dev.env.example dev.env
```

And then edit `dev.env` to suit your local setup. Any API keys etc should be in Bitwarden.

### Database setup

First, download the database dump you want from our [Google Cloud storage](<https://console.cloud.google.com/storage/browser/springload-backups/madewithwagtail?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&project=springload-backups&prefix=&forceOnObjectsSortingFiltering=false>).

Next decrypt the dump using gpg.

Finally, place the decrypted .sql file into [my-dev-environment]/madewithwagtail/docker/database - it will be automatically loaded when you build your database container in the next section.

### Build your containers

```sh
docker-compose up
# In another terminal tab run:
docker-compose exec application ./manage.py migrate
```

### Browsing locally

**https://madewithwagtail.dev.springload.nz/**

## Front End

This project uses [nvm](https://github.com/creationix/nvm) and [Yarn](https://yarnpkg.com/lang/en/)

```sh
# Make sure you use the right node version.
nvm use

# Setup
yarn install

# Start the server and the development tools.
yarn run start

# Builds frontend assets.
yarn run build

# Builds frontend production assets.
yarn run dist

# Runs linting.
yarn run lint

# Runs tests.
yarn run test

# View other available commands with:
yarn run
```

## Documentation

Check out the [`docs/`](docs/) in their own folder.

### Browser support

**Supported browser / device versions:**

| Browser | Device/OS | Version |
|---------|-----------|---------|
| Mobile Safari | iOS Phone | latest |
| Mobile Safari | iOS Tablet | latest |
| Chrome | Android | latest |
| Edge | Desktop | latest |
| Chrome | Desktop | latest |
| Firefox | Desktop | latest |
| Safari | OSX | latest |

### New site submissions workflow

Anyone can submit a site on the [submission form](http://madewithwagtail.org/submit/). When a new site is submitted, the details are saved and also sent to us via an email notification. We then need to manually validate the submission and add the new site via the CMS.

- Check that the submission is valid (see below)
- If the submission isn't valid, we won't add the site to our showcase. Remove it from the CMS.
- If the submission is valid,

1. Look for new submissions https://madewithwagtail.org/admin/forms/submissions/5/ (use the filters at the top to remove already processed dates)
2. Export to CSV
3. For each submission:
    1. Confirm whether it’s a Wagtail website, see [Validating submissions](#validating-submissions).
    2. Find the developer’s profile page or create it if that’s a first submission
    3. Create the website page:
        - Get a screenshot of the website with [headless Google Chrome](https://developers.google.com/web/updates/2017/04/headless-chrome), e.g. `google-chrome --headless --hide-scrollbars --disable-gpu --screenshot --window-size=1200,996 https://springload.co.nz/`
        - Fill out everything from the submission
        - Notify the developer

## Validating submissions

A site is accepted for inclusion on Made with Wagtail if it is made with Wagtail. It's that simple – there is no judgement of a site's quality. In the future, we may change how sites are displayed so some are more prominently visible than others.

To confirm that a site is made with Wagtail,

- Try to go to `<site URL>/admin/`. If the site uses the default admin URLs, it will redirect you to the Wagtail login page.
- Use the [Wappalyzer](https://wappalyzer.com/) browser extension. It won't flag Wagtail directly, but it can flag Django / Python, and could also uncover other technologies.
- Look at the homepage HTML to see if static assets are served from `/static/`, a common URL structure of Django sites.
- Can you find trace of images renditions (e.g. images’ src finish with -max-800 or fill-500x500 or -original or -width-800) in the source? :white_check_mark:
- Does the page has some meta name="generator" content="..." showing that it was made with Wordpress or Drupal? :x:
- Does the page has some /wp-upload path for the images? :x:
- Look at other ideas to figure it out here https://github.com/springload/madewithwagtail/issues/62  :white_check_mark: or :x:
- If all of those methods are inconclusive, assume that the site submission is faithful and that the site is indeed built with Wagtail.

## Publication hook

We send Slack notifications for every new site page published to Made with Wagtail. To try this locally, set up a `local.py` setting override with the right settings.
 


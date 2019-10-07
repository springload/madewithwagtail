[Made with Wagtail](http://madewithwagtail.org) [![Codeship Status for springload/madewithwagtail](https://codeship.com/projects/26741250-da6d-0132-ea89-328081b30bed/status?branch=master)](https://codeship.com/projects/79308) [<img src="https://github.com/torchbox/wagtail/blob/82171f70faaf0c8b8da278261e6f45fed529c899/docs/logo.png" width="83" align="right" alt="Wagtail">](https://wagtail.io/)
=================

> A showcase of sites and apps made with [Wagtail](https://wagtail.io/): an easy to use, open source content management system from [Torchbox](https://github.com/torchbox/wagtail).

*Check out [Awesome Wagtail](https://github.com/springload/awesome-wagtail) for more awesome packages and resources from the Wagtail community.*

## Installation

Install [Vagrant](http://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads), then from the command-line:

```sh
git clone git@github.com:springload/madewithwagtail.git
cd madewithwagtail
.githooks/deploy
vagrant up
# [.. wait until everything gets installed]
vagrant ssh
# [.. from your vagrant machine]
djrun
```

The demo site will now be accessible at [http://localhost:8111/](http://localhost:8111/) and the Wagtail admin interface at [http://localhost:8111/admin/](http://localhost:8111/admin/) . Log into the admin with the credentials ``admin / changeme``.

### Front-end installation

> Install [Node](https://nodejs.org). This project also uses [nvm](https://github.com/creationix/nvm).

To install our dependencies:

```sh
nvm install
# Then, install all project dependencies.
npm install
```

## Working on the project

> Everything mentioned in the installation process should already be done.

### Starting the server

```sh
vagrant up
vagrant ssh
djrun
```

### Front-end commands

```sh
# Make sure you use the right node version.
nvm use
# Start the server and the development tools.
npm run start
# Builds frontend assets.
npm run build
# Runs linting.
npm run lint:versions
# Runs tests.
npm run test
# View other available commands with:
npm run
```

## Deploying a new version

### To production

```sh
npm run deploy
```

From your local machine, it's a good idea to push to the master before
pushing to the deploy branch. That way you know that both are up to date.

## Documentation

### Browser support

**Supported browser / device versions:**

| Browser | Device/OS | Version |
|---------|-----------|---------|
| Mobile Safari | iOS Phone | latest |
| Mobile Safari | iOS Tablet | latest |
| Chrome | Android | latest |
| IE | Desktop | 11 |
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

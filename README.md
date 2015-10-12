[ ![Codeship Status for springload/madewithwagtail](https://codeship.com/projects/26741250-da6d-0132-ea89-328081b30bed/status?branch=master)](https://codeship.com/projects/79308)

Made with Wagtail (madewithwagtail)
================================

This is the source code of [Made with Wagtail](http://www.madewithwagtail.org).

# Installation

Install Vagrant and  VirtualBox:

* [Vagrant](http://www.vagrantup.com/downloads.html)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

# Setup

```
  $ git clone git@github.com:springload/madewithwagtail.git madewithwagtail
  $ cd madewithwagtail
  $ vagrant up
  [.. wait until everything gets installed]
  $ vagrant ssh
  [.. from your vagrant machine]
  $ djrun
```

The demo site will now be accessible at [http://localhost:8111/](http://localhost:8111/) and the Wagtail admin interface at [http://localhost:8111/admin/](http://localhost:8111/admin/) . Log into the admin with the credentials ``admin / changeme``.

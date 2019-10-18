# application

The container builds backend image from Python3.7.

It uses Docker staging and contains two stages:

1. Dev
2. Production

Dev stage installs additional Python dependencies and utilises daemon auto-reload on code change.

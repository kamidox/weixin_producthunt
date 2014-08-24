#!/bin/sh

curl http://localhost:6800/schedule.json -d project=producthunt -d spider=comments -d maxposts=7300


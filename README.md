pylint-server
====

A small Flask application to receive and store a badge for your pylint
reports.

## Requirements

The two main requirements are Flask and Travis.  No other build server are
supported at the moment.

## Deployment and Usage

This application configures a POST route on /reports.  This endpoint accepts
a pylint report generated from your travis build, and a travis job id.

In your install section, put something like the following:

<pre>
install:
  - "pip install pylint"
</pre>

In your after_success section, put something like this:

<pre>
after_success:
  - pylint YOUR_PACKAGE > /tmp/pylint-report.html
  - curl -v -m 120 -X POST -F travis-job-id=$TRAVIS_JOB_ID -F pylint-report=@/tmp/pylint-report.html https://pylint-server.herokuapp.com/travis
</pre>

You can find your badge under:

<pre>
/githubuser/repo?branch=branch
</pre>

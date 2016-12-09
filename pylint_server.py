from __future__ import absolute_import

from flask import Flask, request, Blueprint, current_app
import os
import re
from pymongo import MongoClient
from travispy import TravisPy
import logging


LOG_LEVEL = logging.INFO
BADGE_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="85" height="20">
  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <!-- whole rectangle -->
  <rect rx="3" width="85" height="20" fill="#555"/>

  <!-- rating part -->
  <rect rx="3" x="50" width="35" height="20" fill="#{1}"/>
  <path fill="#{1}" d="M50 0h4v20h-4z"/>

  <!-- whole rectangle -->
  <rect rx="3" width="85" height="20" fill="url(#a)"/>

  <g fill="#fff" text-anchor="middle"
                 font-family="DejaVu Sans,Verdana,Geneva,sans-serif"
                 font-size="11">
    <text x="25" y="15" fill="#010101" fill-opacity=".3">pylint</text>
    <text x="25" y="14">pylint</text>
    <text x="67" y="15" fill="#010101" fill-opacity=".3">{0:.2f}</text>
    <text x="67" y="14">{0:.2f}</text>
  </g>
</svg>
"""

blueprint = Blueprint('main', __name__)


@blueprint.route('/<user>/<repo>', methods=['GET'])
def handle_get(user, repo):
    slug_branch = user + '/' + repo + '/' + request.args.get('branch', 'master')
    db = MongoClient(os.environ['MONGODB_URI']).get_default_database()
    saved = db['badges'].find_one({"_id": slug_branch})
    return saved['svg'], 200


@blueprint.route('/reports', methods=['POST'])
def handle_report_post():
    current_app.logger.info('handling POST on /reports')
    travis_job_id = int(request.form['travis-job-id'])
    slug_branch = get_slug_branch(travis_job_id)
    report = request.files['pylint-report'].read()
    rating, colour = get_rating_and_colour(report)

    db = MongoClient(os.environ['MONGODB_URI']).get_default_database()
    db['badges'].update_one(
        {
            "_id": slug_branch
        },
        {"$set": {
            "_id": slug_branch,
            "svg": BADGE_TEMPLATE.format(rating, colour)
        }},
        upsert=True
    )
    return 'OK', 200


def get_rating_and_colour(report):
    colour = '9d9d9d'
    rating = 0
    match = re.search("Your code has been rated at (.+?)/10", report)
    if match:
        rating = float(match.group(1))
        if 9 <= rating <= 10:
            colour = '44cc11'
        elif 9 > rating >= 7:
            colour = 'f89406'
        elif 0 <= rating < 7:
            colour = 'b94947'
        else:
            colour = '9d9d9d'
    return rating, colour


def get_slug_branch(travis_job_id):
    travis = TravisPy.github_auth(os.environ["GITHUB_TOKEN"])
    log = travis.job(travis_job_id).log.body
    branch, slug = re.search("git clone .* --branch=(.*) https://github.com/(.*).git", log).groups()
    return slug + '/' + branch


def create_app():
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.logger.setLevel(LOG_LEVEL)
    app.config.from_object(__name__)
    app.register_blueprint(blueprint)
    return app


def main():
    app = create_app()
    app.run()

if __name__ == "__main__":
    main()

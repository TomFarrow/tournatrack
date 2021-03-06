# Copyright 2014 Roberto Brian Sarrionandia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import jinja2
import os

from google.appengine.ext import ndb
import tusers

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class JudgeHandler(webapp2.RequestHandler):
    def get(self):
        user = tusers.get_current_user()
        tid = self.request.get('t')

        if not user:
            self.redirect('/reg?t=' + tid)

        #Get the requested tournament
        key = ndb.Key('Tournament', int(tid))
        t = key.get()

        reg = t.preRegRecord().get()

        isi = reg.isInstitution(user)

        if isi:

            template_values = {
            'user' : user,
            't' : t,
            'logout' : tusers.create_logout_url('/'),
            'login' : tusers.create_login_url('/reg?t=' + tid),
            'r' : reg,
            'isi' : isi,
            'judges' : isi.judges(),
            'reg_key' : isi.key.urlsafe()
            }
            template = JINJA_ENVIRONMENT.get_template('view/update_inst_judges.html')
            self.response.write(template.render(template_values))

        else:
            self.redirect('/reg?t=' + tid)

    def post(self):
        user = tusers.get_current_user()
        tid = self.request.get('t')

        if not user:
            self.redirect('/reg?t=' + tid)

        #Get the requested tournament
        key = ndb.Key('Tournament', int(tid))
        t = key.get()

        reg = t.preRegRecord().get()

        isi = reg.isInstitution(user)

        if isi:
            if self.request.get('updating') == 'j':
                #Get all of the judge objects
                judges = isi.judges()

                for j in judges:
                    name = self.request.get(str(j.key.id()) + '_n')
                    j.name = name

                    cv = self.request.get(str(j.key.id()) + '_c')
                    j.cv = cv

                    j.put()

                self.redirect('/reg?t=' + tid)

        else:
            self.redirect('/reg?t=' + tid)

class TeamHandler(webapp2.RequestHandler):
    def get(self):
        user = tusers.get_current_user()
        tid = self.request.get('t')

        if not user:
            self.redirect('/reg?t=' + tid)

        #Get the requested tournament
        key = ndb.Key('Tournament', int(tid))
        t = key.get()

        reg = t.preRegRecord().get()

        isi = reg.isInstitution(user)

        if isi:

            template_values = {
            'user' : user,
            't' : t,
            'logout' : tusers.create_logout_url('/'),
            'login' : tusers.create_login_url('/reg?t=' + tid),
            'r' : reg,
            'isi' : isi,
            'teams' : isi.teams(),
            'reg_key' : isi.key.urlsafe()
            }
            template = JINJA_ENVIRONMENT.get_template('view/update_inst_teams.html')
            self.response.write(template.render(template_values))

        else:
            self.redirect('/reg?t=' + tid)

    def post(self):
        user = tusers.get_current_user()
        tid = self.request.get('t')
        if not user:
            self.redirect('/reg?t=' + tid)

        #Get the requested tournament
        key = ndb.Key('Tournament', int(tid))
        t = key.get()

        reg = t.preRegRecord().get()
        isi = reg.isInstitution(user)
        if isi:
            #Get all of the team objects
            teams = isi.teams()
            for t in teams:

                #Update each of the team attributes with the form data
                name = self.request.get(str(t.key.id()) + '_n')
                t.teamName = name

                sp1n = self.request.get(str(t.key.id()) + '_sp1n')
                t.sp1Name = sp1n

                sp2n = self.request.get(str(t.key.id()) + '_sp2n')
                t.sp2Name = sp2n

                if self.request.get(str(t.key.id()) + '_sp1ESL', default_value=False):
                    t.sp1ESL = True
                if self.request.get(str(t.key.id()) + '_sp1nov', default_value=False):
                    t.sp1Novice = True

                if self.request.get(str(t.key.id()) + '_sp2ESL', default_value=False):
                    t.sp2ESL = True
                if self.request.get(str(t.key.id()) + '_sp2nov', default_value=False):
                    t.sp2Novice = True

                t.put()
        self.redirect('/reg?t=' + tid)


app = webapp2.WSGIApplication([
                                  ('/updatejudges', JudgeHandler),
                                  ('/updateteams', TeamHandler)
                              ], debug=True)

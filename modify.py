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

from forms import JudgeForm, TeamForm

from models import RegisteredOpenTeam, InstitutionTeam

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class JudgeHandler(webapp2.RequestHandler):
	def get(self):
		user = tusers.get_current_user()
		form = JudgeForm()

		j = self.request.get('j')
		j_key = ndb.Key(urlsafe=j)
		judge = j_key.get()

		t = j_key.parent().parent().get()
		reg = t.preRegRecord().get()

		if user.key in t.owner or judge.user == user.key:
			form.name.data = judge.name
			form.phone.data = judge.phone
			form.email.data = judge.email
			form.cv.data = judge.cv

			template_values = {
				'user' : user,
				't' : t,
				'logout' : tusers.create_logout_url('/'),
				'login' : tusers.create_login_url('/mod/judge?j=' + j),
				'r' : reg,
				'form' : form,
				'j' : j_key.urlsafe()
			}
			template = JINJA_ENVIRONMENT.get_template('view/modjudge.html')
			self.response.write(template.render(template_values))
			return
		else:
			self.redirect(self.request.referer)


	def post(self):
		user = tusers.get_current_user()
		form = JudgeForm(self.request.POST)

		j = self.request.get('j')
		j_key = ndb.Key(urlsafe=j)
		judge = j_key.get()

		t = j_key.parent().parent().get()
		reg = t.preRegRecord().get()

		if user.key in t.owner or user.key == judge.user:

			#If valid, create the new judge object
			if (form.validate()):

				judge.name = form.name.data
				judge.phone = form.phone.data
				judge.email = form.email.data
				judge.cv = form.cv.data

				judge.put()

				self.redirect('/reg_control?t=' + str(t.key.id()))
			else:
				template_values = {
					'user' : user,
					't' : t,
					'logout' : tusers.create_logout_url('/'),
					'login' : tusers.create_login_url('/mod/judge?j=' + j),
					'r' : reg,
					'form' : form,
				}
				template = JINJA_ENVIRONMENT.get_template('view/modjudge.html')
				self.response.write(template.render(template_values))
		else:
			self.redirect(self.request.referer)

#Handles the modification of teams
class TeamHandler(webapp2.RequestHandler):
	def get(self):
		user = tusers.get_current_user()
		form = TeamForm()

		t_string = self.request.get('t')
		t_key = ndb.Key(urlsafe=t_string)
		team = t_key.get()

		t = None
		reg = None

		if team.authorised(user):
			form.teamName.data = team.teamName
			form.sp1Name.data = team.sp1Name
			form.sp2Name.data = team.sp2Name
			form.sp1ESL.data = team.sp1ESL
			form.sp1Novice.data = team.sp1Novice
			form.sp2ESL.data = team.sp2ESL
			form.sp2Novice.data = team.sp2ESL

			institution = None

			if isinstance(team, RegisteredOpenTeam ):
				form.leadName.data = team.leadName
				form.email.data = team.email
				form.phone.data = team.phone
				reg = t_key.parent().get()
			elif isinstance(team, InstitutionTeam):
				institution = team.key.parent().get()
				form.leadName.data = institution.leadName
				form.phone.data = institution.phone
				form.email.data = institution.email
				reg = t_key.parent().parent().get()

			t = reg.key.parent().get()

			template_values = {
				'user' : user,
				'logout' : tusers.create_logout_url('/'),
				'login' : tusers.create_login_url('/mod/team?t=' + t_string),
				'r' : reg,
				't' : t,
				'form' : form,
				'institution' : institution,
				'team' : t_key.urlsafe()
			}
			template = JINJA_ENVIRONMENT.get_template('view/modteam.html')
			self.response.write(template.render(template_values))
			return
		else:
			self.redirect(self.request.referer)


	def post(self):
		user = tusers.get_current_user()
		form = TeamForm(self.request.POST)

		t_string = self.request.get('t')
		t_key = ndb.Key(urlsafe=t_string)
		team = t_key.get()

		institution = None
		t = None

		# If it is an institutional team, don't let them update the contact info
		# with this method, as that data belongs to the Institution
		if (isinstance(team, InstitutionTeam)):
			institution = team.key.parent().get()
			form.leadName.data = institution.leadName
			form.email.data = institution.email
			form.phone.data = institution.phone

			reg = institution.key.parent().get()

		elif (isinstance(team, RegisteredOpenTeam)):
			reg = t_key.parent().get()

		t = reg.key.parent().get()

		#Check if they are allowed to edit
		if team.authorised(user):

			#If valid, update the team object
			if (form.validate()):

				team.leadName = form.leadName.data
				team.email = form.email.data
				team.phone = form.phone.data
				team.teamName = form.teamName.data
				team.sp1Name = form.sp1Name.data
				team.sp2Name = form.sp2Name.data
				team.sp1ESL = form.sp1ESL.data
				team.sp2ESL = form.sp2ESL.data
				team.sp1Novice = form.sp1Novice.data
				team.sp2Novice = form.sp2Novice.data

				team.put()

				self.redirect('/reg_control?t=' + str(t.key.id()))
			else:
				template_values = {
					'user' : user,
					't' : t,
					'logout' : tusers.create_logout_url('/'),
					'login' : tusers.create_login_url('/mod/team?j=' + t_key.urlsafe()),
					'r' : reg,
					'form' : form,
					'team' : t_key.urlsafe(),
					'institution' : institution
				}
				template = JINJA_ENVIRONMENT.get_template('view/modteam.html')
				self.response.write(template.render(template_values))
		else:
			self.redirect(self.request.referer)

app = webapp2.WSGIApplication([
	('/mod/judge', JudgeHandler),
	('/mod/team', TeamHandler)
], debug=True)

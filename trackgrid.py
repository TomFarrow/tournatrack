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
import datetime

import tusers
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class GridHandler(webapp2.RequestHandler):
	def get(self):
		user = tusers.get_current_user()
		#Get the requested tournament
		tid = self.request.get('t')
		t_key = ndb.Key('Tournament', int(tid))
		t = t_key.get()
				
		if (user and user.key in t.owner):
			#Get all of the rooms whose parent is the current tournament
			q = t.rooms()
			
			template_values = {
				'user' : user,
				't' : t,
				'rooms' : q,
				'logout' : tusers.create_logout_url('/'),
			}
			#Check if this is an AJAX request for the raw table
			if (self.request.get('raw') == '1'):
				template = JINJA_ENVIRONMENT.get_template('view/rawgrid.html')
			else:
				template = JINJA_ENVIRONMENT.get_template('view/trackgrid.html')
			self.response.write(template.render(template_values))
						
		else:
			self.redirect(tusers.create_login_url(self.request.uri))
			
	def post(self):
		user = tusers.get_current_user()
		#Get the requested tournament
		tid = self.request.get('t')
		t_key = ndb.Key('Tournament', int(tid))
		t = t_key.get()
				
		if (user and user.key in t.owner):
			rid = self.request.get('r')
			r_key = ndb.Key('Tournament', int(tid), 'Room', int(rid))
			room = r_key.get()
		
			room.status = self.request.get('status')
			room.comment = self.request.get('comment')
			room.changed = datetime.datetime.now().time()
		
			room.put()
			self.redirect('/trackgrid?t=' + str(t_key.id()))
		else:
			self.redirect(tusers.create_login_url(self.request.uri))
	

app = webapp2.WSGIApplication([
	('/trackgrid', GridHandler)
], debug=True)

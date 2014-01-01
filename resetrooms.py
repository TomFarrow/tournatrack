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
import os
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

from models import Tournament
from models import Room

class ResetRoomsHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		#Get the requested tournament
		tid = self.request.get('t')
		t_key = ndb.Key('Tournament', int(tid))
		t = t_key.get()
				
		if (user and user in t.owner):
			#Get all of the rooms whose parent is the current tournament
			q = t.rooms()
			
			#Change the status of each of the rooms to nothing
			for r in q:
				r.comment = None
				r.status = None
				r.changed = None
				r.put()
			self.redirect('/trackgrid?t=' + str(t_key.id()))
			
		else:
			self.redirect(users.create_login_url(self.request.uri))
	

app = webapp2.WSGIApplication([
	('/reset_rooms', ResetRoomsHandler)
], debug=True)
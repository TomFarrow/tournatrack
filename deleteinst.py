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

import tusers
from google.appengine.ext import ndb

class InstitutionHandler(webapp2.RequestHandler):
	def get(self):
		user = tusers.get_current_user()
		#Get the requested tournament
		tid = self.request.get('t')
		t_key = ndb.Key('Tournament', int(tid))
		t = t_key.get()
				
		if (user and user.key in t.owner):
			#Get the institution in question
			iid = self.request.get('i')
			i_key = ndb.Key('Tournament', int(tid), 'Institution', int(iid))
			#Unceremoniously delete it
			i_key.delete()
			
			#Send the user back to the institution list
			self.redirect('/institution?t=' + str(t_key.id()))
						
		else:
			self.redirect(tusers.create_login_url(self.request.uri))
	

app = webapp2.WSGIApplication([
	('/del_i', InstitutionHandler)
], debug=True)

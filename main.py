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

import tusers

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		user = tusers.get_current_user()
		if user:
			template_values = {
				'user' : user,
				'logout' : tusers.create_logout_url('/')
			}
			template = JINJA_ENVIRONMENT.get_template('view/index.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(tusers.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)

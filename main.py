import os
import json
import urllib
import webapp2
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        name = self.request.get('zipCode')
        url = "https://api.nationalize.io/?name="+ name
        data = urllib.urlopen(url).read()
        
        data = json.loads(data)

        if(data['country'] != ''):
            country_id = data['country'][0]['country_id']
            probability = data['country'][0]['probability']
            template_values = {
                "country_id": country_id,
                "probability":probability,
            }
            path = os.path.join(os.path.dirname(__file__), 'results.html')
            self.response.out.write(template.render(path, template_values))
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'error.html')
            self.response.out.write(template.render(path, template_values))
        
        
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
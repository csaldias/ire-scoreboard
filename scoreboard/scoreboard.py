import cgi
import datetime
import wsgiref.handlers
import os
import urllib

from google.appengine.ext import db
from google.appengine.api import users
#from google.appengine.ext import webapp

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Team(db.Model):
	name = db.StringProperty(multiline=False)			#Nombre equipo
	team_id = db.StringProperty(multiline=False)		#ID Equipo
	category = db.StringProperty(multiline=False)		#Categoria: Avanzado, Basico
	score_total = db.StringProperty(multiline=False)	#Puntaje total
	score_round1 = db.StringProperty(multiline=False)	#Puntaje ronda 1
	score_round2 = db.StringProperty(multiline=False)	#Puntaje ronda 2
	score_code = db.StringProperty(multiline=False)		#Puntaje codigo
	score_teamwork = db.StringProperty(multiline=False)	#Puntaje trabajo equipo

class AddTeam(webapp2.RequestHandler):
	def get(self):
		#List all teams
		query = Team.all()
		query.order('name')
		#first, lets see if there's any team in the system
		results = query.get()
		teams = []
		if results: #If there is...
			for team in query.run(): #We show them
				teams.append(team)

		template_values = {
            'teams': teams,
        }

		template = JINJA_ENVIRONMENT.get_template('create_team.html')
		self.response.write(template.render(template_values))

#TODO: Proteger pagina para modificar puntajes
#Google login?
class CreateTeam(webapp2.RequestHandler):
	def post(self):
		team = Team()
		team.team_id = self.request.get('team_id')
		team.name = self.request.get('name')
		team.category = self.request.get('category')
		team.score_total = self.request.get('score_total')
		team.score_round1 = self.request.get('score_round1')
		team.score_round2 = self.request.get('score_round2')
		team.score_teamwork = self.request.get('score_teamwork')
		team.score_code = self.request.get('score_code')
		team.put()
		self.redirect('/')

class UpdateTeam(webapp2.RequestHandler):
	def post(self):
		query = Team.all()
		query.filter('team_id =', self.request.get('team_id'))
		team = query.get()
		if self.request.get('score_total'): team.score_total = self.request.get('score_total')
		if self.request.get('score_round1'): team.score_round1 = self.request.get('score_round1')
		if self.request.get('score_round2'): team.score_round2 = self.request.get('score_round2')
		if self.request.get('score_teamwork'): team.score_teamwork = self.request.get('score_teamwork')
		if self.request.get('score_code'): team.score_code = self.request.get('score_code')
		team.put()
		self.redirect('/')

class ScorePage(webapp2.RequestHandler):
	def get(self):

		scores = db.GqlQuery("SELECT * "
			"FROM Team "
			"ORDER BY score_total DESC")

		template_values = {
            'scores': scores,
        }

		template = JINJA_ENVIRONMENT.get_template('scores.html')
		self.response.write(template.render(template_values))

class ScoreBasico(webapp2.RequestHandler):
	def get(self):

		scores = db.GqlQuery("SELECT * "
			"FROM Team "
			"WHERE category = 'Basico'"
			"ORDER BY score_total DESC")

		template_values = {
            'scores': scores,
        }

		template = JINJA_ENVIRONMENT.get_template('scores_basico.html')
		self.response.write(template.render(template_values))

class ScoreAvanzado(webapp2.RequestHandler):
	def get(self):

		scores = db.GqlQuery("SELECT * "
			"FROM Team "
			"WHERE category = 'Avanzado'"
			"ORDER BY score_total DESC")

		template_values = {
            'scores': scores,
        }

		template = JINJA_ENVIRONMENT.get_template('scores_avanzado.html')
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
	('/', ScorePage),
	('/score-basico', ScoreBasico),
	('/score-avanzado', ScoreAvanzado),
	('/create', CreateTeam),
	('/update', UpdateTeam),
	('/add', AddTeam)
	], debug=True)


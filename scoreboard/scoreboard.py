import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Team(db.Model):
	name = db.StringProperty(multiline=False)			#Nombre equipo
	score_total = db.StringProperty(multiline=False)	#Puntaje total
	score_round1 = db.StringProperty(multiline=False)	#Puntaje ronda 1
	score_round2 = db.StringProperty(multiline=False)	#Puntaje ronda 2
	score_code = db.StringProperty(multiline=False)		#Puntaje codigo
	score_teamwork = db.StringProperty(multiline=False)	#Puntaje trabajo equipo

class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')
		self.response.out.write("""
			<p>Create team</p>
			<form action="/create" method="post">
			<div>Team name: <textarea name="name" rows="1" cols="30"></textarea></div>
			<div>Total score: <textarea name="score_total" rows="1" cols="10"></textarea></div>
			<div>First round score: <textarea name="score_round1" rows="1" cols="10"></textarea></div>
			<div>Second round score: <textarea name="score_round2" rows="1" cols="10"></textarea></div>
			<div>Code score: <textarea name="score_code" rows="1" cols="10"></textarea></div>
			<div>Teamwork score: <textarea name="score_teamwork" rows="1" cols="10"></textarea></div>
			<div><input type="submit" value="Create team"></div>
			</form>
			<p>Update</p>
			<select>
			""")

		#List all teams
		query = Team.all()
		query.order('name')
		#first, lets see if there's any team in the system
		results = query.get()
		if results: #If there is...
			for team in query.run(): #We show them
				self.response.out.write("""<option value="">"""+team.name+"""</option>""")
		self.response.out.write("""<body><html>""")

#TODO: Proteger pagina para modificar puntajes
#Google login?
class CreateTeam(webapp.RequestHandler):
	def post(self):
		team = Team()
		team.name = self.request.get('name')
		team.score_total = self.request.get('score_total')
		team.score_round1 = self.request.get('score_round1')
		team.score_round2 = self.request.get('score_round2')
		team.score_teamwork = self.request.get('score_teamwork')
		team.score_code = self.request.get('score_code')
		team.put()
		self.redirect('/scores')

class ScorePage(webapp.RequestHandler):
	def get(self):

		highscores = db.GqlQuery("SELECT * "
			"FROM Team "
			"ORDER BY score_total DESC")

		self.response.out.write("""
			<html>
			<body>
			<p>Scoreboard</p>
			<table>
			<tr>
				<td>Nombre</td>
				<td>Puntaje Programacion</td>
				<td>Puntaje Trabajo Equipo</td>
				<td>Puntaje Ronda 1</td>
				<td>Puntaje Ronda 2</td>
				<td>Puntaje Total</td>
			</tr>
			""")
		for sc in highscores:
			self.response.out.write("""
				<tr>
					<td>"""+sc.name+"""</td>
					<td>"""+sc.score_code+"""</td>
					<td>"""+sc.score_teamwork+"""</td>
					<td>"""+sc.score_round1+"""</td>
					<td>"""+sc.score_round2+"""</td>
					<td>"""+sc.score_total+"""</td>
				</tr>""")
		self.response.out.write("""<body><html>""")

application = webapp.WSGIApplication([
	('/', MainPage),
	('/create', CreateTeam),
	('/scores', ScorePage)
	], debug=True)


def main():
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()

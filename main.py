import cherrypy
import os
import pymysql.cursors
from jinja2 import Environment, FileSystemLoader

# Connexion à la base de données
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database= 'ski_alpin',
    cursorclass=pymysql.cursors.DictCursor
)

# Classe pour le serveur web CherryPy
class MyWebService(object):

    # Méthode pour la page d'index
    @cherrypy.expose
    def index(self, tri=None):

        # Récupération des informations des stations et des pistes depuis la base de données
        with connection.cursor() as cursor:
            sql = "SELECT * FROM stations"
            if tri is not None:
                if tri == "nom_asc":
                    sql += " ORDER BY nom ASC"
                elif tri == "nom_desc":
                    sql += " ORDER BY nom DESC"
                elif tri == "cout_jour_asc":
                    sql += " ORDER BY cout_jour ASC"
                elif tri == "cout_jour_desc":
                    sql += " ORDER BY cout_jour DESC"
                elif tri == "cout_semaine_asc":
                    sql += " ORDER BY cout_semaine ASC"
                elif tri == "cout_semaine_desc":
                    sql += " ORDER BY cout_semaine DESC"
            cursor.execute(sql)
            stations = cursor.fetchall()
            for station in stations:
                sql = "SELECT * FROM pistes WHERE station_id = %s ORDER BY couleur"
                cursor.execute(sql, station['id'])
                station['pistes'] = cursor.fetchall()

        # Récupération des notes depuis la base de données
        with connection.cursor() as cursor:
            sql = "SELECT * FROM notes"
            cursor.execute(sql)
            notes = cursor.fetchall()
            for note in notes:
                sql = "SELECT * FROM pistes WHERE id = %s"
                cursor.execute(sql, note['piste_id'])
                note['piste'] = cursor.fetchone()

        # Chargement du template
        env = Environment(loader=FileSystemLoader('templates'))
        tmpl = env.get_template('index.html')

        # Affichage de la page
        return tmpl.render(stations=stations, tri=tri, notes=notes)

    # Méthode pour ajouter une note
    @cherrypy.expose
    def ajouter_note(self, date=None, qualite_neige=None, frequentation=None, commentaire=None, piste_id=None):
        if date and qualite_neige and frequentation and commentaire and piste_id:
            with connection.cursor() as cursor:
                sql = "INSERT INTO notes (date, qualite_neige, frequentation, commentaire, piste_id) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (date, qualite_neige, frequentation, commentaire, piste_id))
                connection.commit()
        raise cherrypy.HTTPRedirect("/notes")
    
    @cherrypy.expose
    def notes(self):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM notes"
            cursor.execute(sql)
            notes = cursor.fetchall()
            for note in notes:
                sql = "SELECT * FROM pistes WHERE id = %s"
                cursor.execute(sql, note['piste_id'])
                note['piste'] = cursor.fetchone()
            sql = "SELECT * FROM stations"
            cursor.execute(sql)
            stations = cursor.fetchall()
            for station in stations:
                sql = "SELECT * FROM pistes WHERE station_id = %s"
                cursor.execute(sql, station['id'])
                station['pistes'] = cursor.fetchall()
            for pistes in station['pistes']:
                sql = "SELECT * FROM notes WHERE piste_id = %s"
                cursor.execute(sql, pistes['id'])
                pistes['notes'] = cursor.fetchall()
        env = Environment(loader=FileSystemLoader('templates'))
        tmpl = env.get_template('notes.html')
        return tmpl.render(notes=notes,stations=stations)
    
    @cherrypy.expose
    def admin(self):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM stations"
            cursor.execute(sql)
            stations = cursor.fetchall()
            for station in stations:
                sql = "SELECT * FROM pistes WHERE station_id = %s"
                cursor.execute(sql, station['id'])
                station['pistes'] = cursor.fetchall()
            for pistes in station['pistes']:
                sql = "SELECT * FROM notes WHERE piste_id = %s"
                cursor.execute(sql, pistes['id'])
                pistes['notes'] = cursor.fetchall()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM notes"
            cursor.execute(sql)
            notes = cursor.fetchall()
            for piste in notes:
                sql = "SELECT * FROM pistes WHERE id = %s"
                cursor.execute(sql, piste['piste_id'])
                piste['piste'] = cursor.fetchone()
        env = Environment(loader=FileSystemLoader('templates'))
        tmpl = env.get_template('admin.html')
        return tmpl.render(stations=stations,notes=notes)

    @cherrypy.expose
    def ajouter_station(self, nom=None,localisation=None, cout_jour=None, cout_semaine=None, commentaire=None):
        if nom and localisation and cout_jour and cout_semaine and commentaire:
            with connection.cursor() as cursor:
                sql = "INSERT INTO stations (nom, localisation, cout_jour, cout_semaine, commentaire) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (nom, localisation, cout_jour, cout_semaine, commentaire))
                connection.commit()
        raise cherrypy.HTTPRedirect("/admin")
    
    @cherrypy.expose
    def supprimer_station(self, id_station=None):
        if id:
            with connection.cursor() as cursor:
                sql = "DELETE FROM pistes WHERE station_id = %s"
                cursor.execute(sql, id_station)
                connection.commit()
                sql = "DELETE FROM stations WHERE id = %s"
                cursor.execute(sql, id_station)
                connection.commit()
        raise cherrypy.HTTPRedirect("/admin")
    
    @cherrypy.expose
    def ajouter_piste(self, nom_piste=None, couleur=None, station_id=None):
        if nom_piste and couleur and station_id:
            with connection.cursor() as cursor:
                sql = "INSERT INTO pistes (nom_piste, couleur, station_id) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nom_piste, couleur, station_id))
                connection.commit()
        raise cherrypy.HTTPRedirect("/admin")
    
    @cherrypy.expose
    def supprimer_piste(self, piste_id=None):
        if id:
            with connection.cursor() as cursor:
                sql = "DELETE FROM pistes WHERE id = %s"
                cursor.execute(sql, piste_id)
                connection.commit()
        raise cherrypy.HTTPRedirect("/admin")
    
    @cherrypy.expose
    def modifier_station(self, id_station=None, nom=None,localisation=None, cout_jour=None, cout_semaine=None, commentaire=None, message=None):
        if nom and localisation and cout_jour and cout_semaine and commentaire:
            with connection.cursor() as cursor:
                sql = "UPDATE stations SET nom = %s, localisation = %s, cout_jour = %s, cout_semaine = %s, commentaire = %s WHERE id = %s"
                cursor.execute(sql, (nom, localisation, cout_jour, cout_semaine, commentaire, id_station))
                connection.commit()
        raise cherrypy.HTTPRedirect("/admin")
    
    @cherrypy.expose
    def modifier_piste(self, id_piste=None, nom_piste=None, couleur=None, station_id=None):
        if nom_piste and couleur and station_id:
            with connection.cursor() as cursor:
                sql = "UPDATE pistes SET nom_piste = %s, couleur = %s, station_id = %s WHERE id = %s"
                cursor.execute(sql, (nom_piste, couleur, station_id, id_piste))
                connection.commit()
        raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose
    def supprimer_note(self, id_note=None):
        if id_note:
            with connection.cursor() as cursor:
                sql = "DELETE FROM notes WHERE id = %s"
                cursor.execute(sql, id_note)
                connection.commit()
        raise cherrypy.HTTPRedirect("/admin")
    
    @cherrypy.expose
    def modifier_note(self, id_note=None, date=None, qualite_neige=None, frequentation=None, commentaire=None, piste_id=None):
        if date and qualite_neige and frequentation and commentaire and piste_id and id_note:
            with connection.cursor() as cursor:
                sql = "UPDATE notes SET date = %s, qualite_neige = %s, frequentation = %s, commentaire = %s, piste_id = %s WHERE id = %s"
                cursor.execute(sql, (date, qualite_neige, frequentation, commentaire, piste_id, id_note))
                connection.commit()
        raise cherrypy.HTTPRedirect("/admin")
    
    @cherrypy.expose
    def login(self):
        env = Environment(loader=FileSystemLoader('templates'))
        tmpl = env.get_template('login.html')
        return tmpl.render()
    
    @cherrypy.expose
    def auth(self, username=None, password=None):
        if username == "admin" and password == "admin":
            cherrypy.session['username'] = username
            raise cherrypy.HTTPRedirect("/admin")
        else:
            raise cherrypy.HTTPRedirect("/login")

        
    @cherrypy.expose
    def logout(self):
        raise cherrypy.HTTPRedirect("/")
    
# Configuration de CherryPy
conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './static'
    },
    'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080
    }
}

# Démarrage du serveur CherryPy
if __name__ == '__main__':
    cherrypy.quickstart(MyWebService(), '/', conf)

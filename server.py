#!/usr/bin/env python3
# server.py
# author: Diego van Outryve d'Ydewalle, 16092
# author: Alexandre Seyaeneve, 16169
# version:  20 décembre, 2017

import json
import os.path

import cherrypy
from cherrypy.lib.static import serve_file
import jinja2

import jinja2plugin
import jinja2tool

class BeerCalc():
    """Web application of the BeerCalc application."""
    def __init__(self):
        self.beers = self.loadbeers()


    @cherrypy.expose
    def index(self,):
        """Main page of the BeerCalc application."""
        beersindex = " "
        for i in range(len(self.beers)):
            beer = self.beers[i]
            beersindex += '<option value={} {} </option>'.format(id, beer["nom"])
        return {'beersindex': beersindex}

    @cherrypy.expose
    def calc(self, selectedBeer=""):
        "Take the all info of the beer selected"
        beers = ''
        cdt =''
        alcool = ''
        Pl= ''
        for id in range(len(self.beers)):
            beer = self.beers[id]
            if selectedBeer !='' and id == int(selectedBeer):

                beers += '<option value="{}"selected>{}</option>'.format(id, beer['nom'])
            else:
                beers += '<option value="{}">{}</option>'.format(id, beer['nom'])

        if selectedBeer != "":
            alcool = self.beers[int(selectedBeer)]["alcool"]
            Pl = self.beers[int(selectedBeer)]["Pl"]
            for c in self.beers[int(selectedBeer)]["conditionnement"]:
                cdt += '<option value="{0}">{0}</option>'.format(c)
        return {"beers": beers, "cdt": cdt, "alcool": alcool, "Pl" : Pl}

    @cherrypy.expose
    def new(self):
       return serve_file(os.path.join(CURDIR, 'templates/new.html'))\

    @cherrypy.expose
    def rslt(self, id, nM, soifg, nF, soiff,cdt,alcool,Pl):
        "All the math behind the page rslt"
        alcool = float(self.beers[int(id)]["alcool"])
        Pl = float(self.beers[int(id)]["Pl"])
        namebeer =str(self.beers[int(id)]["nom"]) #Comentaire#
        Bpg = int
        Bpf = int
        nM=int(nM)
        nF = int(nF)
        soifg=int(soifg)
        soiff = int(soiff)
        cdtc = self.converter(cdt)

        if soifg == 1 or soifg == 2:
            k = 2
            Bpg = soifg * k
        if soiff == 1 or soiff == 2:
            k = 1.5
            Bpf = soiff * k
        if soifg == 3 :
            k = 2.5
            Bpg = soifg * k
        if soiff == 3 :
            k = 2
            Bpf = soiff * k

        if soifg == 4:
            k = 3
            Bpg = soifg * k

        if soiff == 4:
            k = 2.5
            Bpf = soiff * k
        if soifg == 5:
            k = 3.5
            Bpg = soifg * k
        if soiff == 3:
            k = 2
            Bpf = soiff * k

        if alcool < 10.0 and alcool > 8:
            ka = 2.0
            Bpf = Bpf // ka
            Bpg = Bpg // ka
        if alcool < 8 and alcool > 5:
            ka = 1.5
            Bpf = Bpf // ka
            Bpg = Bpg // ka
        if alcool < 5.0:
            ka = 1
            Bpf = Bpf // ka
            Bpg = Bpg // ka

        quantité= ((nM*Bpg)+(nF*Bpf))*0.25
        Prix = quantité*Pl
        Unité = quantité//cdtc

        Pp = Prix/(nM+nF)
        Pp = int(Pp * 100)
        Pp = (float(Pp)) / 100


        return {"namebeer": namebeer, "nM": nM, "soifg": soifg, "nF": nF, "soiff": soiff, "cdt": cdt, "alcool": alcool,
                "Pl": Pl,"quantité":quantité, "Prix":Prix,"Unité":Unité,"Bpf":Bpf,"Bpg":Bpg,"Pp":Pp}

    def converter(self,cdt):
        '''Convertisseur de mes Conditionnements'''
        if cdt == "Cannette 25cl":
            cdt = 0.25
            return (cdt)
        if cdt == "Cannette 33cl":
            cdt = 0.33
            return (cdt)
        if cdt == "Cannette 50cl":
            cdt = 0.5
            return (cdt)
        if cdt == "Bouteille 25cl":
            cdt = 0.25
            return (cdt)
        if cdt == "Bouteille 50cl":
            cdt = 0.5
            return (cdt)
        if cdt == "Bouteille 33cl":
            cdt = 0.33
            return (cdt)
        if cdt == "Bouteille 75cl":
            cdt = 0.75
            return (cdt)
        if cdt == "Fût 30l":
            cdt = 30
            return (cdt)
        if cdt == "Fût 50l":
            cdt = 50
            return (cdt)
        print("error cdt")
        print(cdt)
        return (cdt)

    @cherrypy.expose
    def addbeer(self, nom, alcool, Pl, conditionnement):
        """POST route to add a new beer to the database."""
        if nom != '' and alcool != '' and conditionnement != []:
            self.beers.append({
                    'nom': nom,
                    'alcool': alcool,
                    'Pl': Pl,
                    'conditionnement': conditionnement
            })
            self.savebeers()


        raise cherrypy.HTTPRedirect('/')

    def loadbeers(self):
        """Load links' database from the 'db.json' file."""
        try:
            with open('db.json', 'r', encoding='utf-8') as file:
                content = json.loads(file.read())
                return content ['beers']
        except Exception as e:
            print(e)
            cherrypy.log('Loading database failed.')
            return []

    def savebeers(self):
        """Save links' database to the 'db.json' file."""
        try:
            with open('db.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps({
                    'beers': self.beers
                }, ensure_ascii=False,indent=4))
        except:
            cherrypy.log('Saving database failed.')


if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=ENV).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()
    # Launch web server
    CURDIR = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(BeerCalc(), '', 'server.conf')

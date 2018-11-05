import mysql.connector

class Mapping():
    
    def __init__(self,hash,url):
        self.hash = hash
        self.url = url

    def __str__(self):
        return self.hash+" "+self.url

class MappingDao():

    def __init__(self):
        self.db = mysql.connector.connect(host="localhost",user="root",password="sarvesh",database="urlshortener")
        self.cursor = self.db.cursor()


    def add(self,mapping):
        self.cursor.execute("insert into mapping values(%s,%s)",(mapping.hash,mapping.url))
        self.db.commit()
        

    def getbyhash(self,hash):
        self.cursor.execute("select url from mapping where hash='%s'" %(hash))
        result = self.cursor.fetchone()[0]
        return result

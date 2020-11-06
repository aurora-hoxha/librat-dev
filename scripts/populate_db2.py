"""
+---------+      www.google.com       +---------------+
|    U    | ------------------------> |       B       |
+---------+                           +---------------+
                                             ||

                                      +---------------+      kerkon IP         +---------+
                                      |       B       | ---------------------> |   DNS   |
                                      +---------------+                        +---------+
                                                                                    || gjen IP

                                      +---------------+      kthen IP          +---------+
                                      |       B       | <--------------------- |   DNS   |
                                      +---------------+                        +---------+
                                             ||
                                             ||
                                      +---------------+      kerkon faqen      +---------+
                                      |       B       | ---------------------> |    S    |
                                      +---------------+                        +---------+

                                                                                    ||   proceson kerkesen
                                                                                    ||   ...
                                                                                    ||   nderton pergjigjen

                                      +---------------+     kthen pergjigje    +---------+
                                      |       B       | <--------------------- |    S    |
                                      +---------------+                        +---------+
                                             || interpreton
                                             || pergjigjen
+---------+     paraqet rezultatin    +---------------+
|    U    | <-----------------------  |       B       |
+---------+                           +---------------+


------
Protokolli HTTP
Koncepti i Resource / URI

Request (Client-Server):
	GET / HTTP/1.1
	Host: www.example.com

	<verb> <relative-path (URI)> <specification>
	Host: <plaintext>

	Verbs: GET POST PUT DELETE OPTIONS HEAD ...

Response (Server - Client):
	HTTP/1.1 200 OK
	<specification> <status-code> <status message>

	<response-headers>
	Date: Mon, 23 May 2005 22:38:34 GMT
	Content-Type: text/html; charset=UTF-8
	Content-Length: 155
	Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT
	Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)
	ETag: "3f80f-1b6-3e1cb03b"
	Accept-Ranges: bytes
	Connection: close

	<response body>
	<html>
	  <head>
	    <title>An Example Page</title>
	  </head>
	  <body>
	    <p>Hello World, this is a very simple HTML document.</p>
	  </body>
	</html>


"""
import csv
from app.models import Liber, Autor



def krijo_liber(autori, titulli, img_src, _id):
    cmimi = "15.00 EUR"
    liber = Liber(
        titulli=titulli,
        autori=autori,
        cmimi=cmimi,
        img_src=img_src,
        iid=_id
    )
    liber.save()


def krijo_autor(emer, _id):
    autor = Autor(
        emri=emer.title(),
        iid=_id
    )
    autor.save()

def krijo_lidhje(id_liber, emer_autori):
    libri = Liber.objects.get(iid=id_liber)
    autori = Autor.objects.get(emri=emer_autori.lower().title())

    # <fusha>.add(<objekti>)
    autori.librat.add(libri)
    # <objekti>.save() -> ben qe ndryshimet te jene ne databaze
    autori.save()

def krijo_librat():
    with open('books.csv', 'r', encoding='utf8') as data:
        reader = csv.reader(data)
        for rrjesht in reader:
            autori = rrjesht[7]
            titulli = rrjesht[9]
            img_src = rrjesht[-2]
            _id = rrjesht[0]

            krijo_liber(
                autori,
                titulli,
                img_src, _id
            )


def krijo_autoret():
    autore = set()

    with open('books.csv', 'r', encoding='utf8') as data:
        reader = csv.reader(data)
        for rrjesht in reader:
            autori = rrjesht[7]
            autore.add(autori.lower())

    autoret = list(autore)
    autoret.sort()
    for _id, emer in enumerate(list(autoret)):
        krijo_autor(emer, _id)


def krijo_lidhjet():
    with open('books.csv', 'r', encoding='utf8') as data:
        reader = csv.reader(data)
        for rrjesht in reader:
            autori = rrjesht[7]
            id_liber = rrjesht[0]
            krijo_lidhje(id_liber, autori)

def zbraz():
    Liber.objects.all().delete()
    Autor.objects.all().delete()


def numri_i_librave():
    return Liber.objects.all().count()


def numri_i_autoreve():
    return Autor.objects.all().count()


def run():
    print("Pastrim i DB ...")
    zbraz()
    print('Krijo librat ...')
    print('(Libra) Numri para:', numri_i_librave())
    krijo_librat()
    print('(Libra) Numri pas:', numri_i_librave())
    print('Krijo autoret ...')
    print('(Autore) Numri para:', numri_i_autoreve())
    krijo_autoret()
    print('(Autore) Numri pas:', numri_i_autoreve())
    print('Krijo lidhjet ...')
    krijo_lidhjet()



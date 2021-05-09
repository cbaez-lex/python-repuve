import tornado.ioloop
import tornado.web
import cv2 as cv
from bs4 import BeautifulSoup
from urllib import request
import urllib
import io
from io import StringIO
import numpy
from PIL import Image
import pytesseract


class MainHandler(tornado.web.RequestHandler):
    def get(self):

        fp = urllib.request.urlopen("http://www2.repuve.gob.mx:8080/ciudadania/jcaptcha")
        mybytes = fp.read()

        file = mybytes
        pil = Image.open(io.BytesIO(file))
        img = numpy.array(pil)
        im = Image.fromarray(img)
        im.save("captcha.jpeg")
        gray = cv.imread("captcha.jpeg", cv.IMREAD_GRAYSCALE)
        masked = cv.inRange(gray, 231, 255)

        text_found = pytesseract.image_to_string(gray)
        print(text_found)
        # text = '22'

        # print(text)

        # response = urllib2.urlopen('http://www2.repuve.gob.mx:8080/ciudadania/servletconsulta')
        # print response.read()
        # html = response.read()
        # do something
        # response.close()  # best practice to close the file

        url = 'http://www2.repuve.gob.mx:8080/ciudadania/servletconsulta'
        values = {'placa': 'PHB6260',
                  'captcha': text_found,
                  'pageSource': 'index.jsp'}

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        response = urllib.request.urlopen(url, data)
        the_page = response.read()

        classname = 'style21'

        soup = BeautifulSoup(the_page)
        soup2 = BeautifulSoup(the_page)
        try:
            tr = soup.findAll('table')[0].findAll(
                'tr')[2].findAll("table")[1].findAll("tr")

            # print(tr)

            brand = tr[0].find("span", {"class": classname}).text
            model = tr[1].find("td", {"class": classname}).text
            yearModel = tr[2].find("span", {"class": classname}).text
            class_ = tr[3].find("span", {"class": classname}).text
            type_ = tr[4].find("span", {"class": classname}).text
            niv = tr[5].find("span", {"class": classname}).text
            nci = tr[6].find("span", {"class": classname}).text
            plate = tr[7].find("span", {"class": classname}).text
            doors = tr[8].find("td", {"class": classname}).text
            originCity = tr[9].find("td", {"class": classname}).text
            version = tr[10].find("td", {"class": classname}).text
            ccl = tr[11].find("td", {"class": classname}).text
            cylinders = tr[12].find("td", {"class": classname}).text
            axles = tr[13].find("td", {"class": classname}).text
            assemblyPlant = tr[14].find("td", {"class": classname}).text
            extra = tr[15].find("span", {"class": classname}).text
            enrolledInstitution = tr[16].find("span", {"class": classname}).text
            enrolledDate = tr[17].find("span", {"class": classname}).text
            enrolledHour = tr[18].find("span", {"class": classname}).text
            registrationEntity = tr[19].find("span", {"class": classname}).text
            registrationDate = tr[20].find("span", {"class": classname}).text
            lastUpdate = tr[21].find("span", {"class": classname}).text

            stolenString = soup2.findAll('table')[4].findAll('tr')[0].findAll('td')[
                1].find('b').text.strip(' \t\n\r')

            stolen = False

            if (stolenString != 'SIN REPORTE DE ROBO'):
                stolen = True

            self.write(stolenString)
        except Exception as e:
            print("Exception in scrapping portion: ", e)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

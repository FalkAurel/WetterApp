from sys import exit
import pygame
import requests

class API:
    def __init__(self, stadt, apikey = "Gebe deinen eigenen ein"):
        self.stadt = stadt
        self.apikey = apikey
    def kontrolle(self):
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(self.stadt, self.apikey))
        r = r.ok
        return r
    
    def get(self):
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(self.stadt, self.apikey))
        r = r.json()
        return r
    
    @staticmethod
    def inf_sorting(r):
        display_data = [r["wind"]["speed"], r["main"]["pressure"], r["main"]["humidity"], r["wind"]["deg"], r["main"]["temp"], r["main"]["feels_like"]]
        return display_data
    
    def inf_ausgabe(self, data):
        windrichtung = data[3]
        windspeed = str(data[0]) + " " + "m/s"
        druck = str(data[1]) + "hPa"
        temp = str(int(data[4] - 273.15)) + "°C"
        feels_like = str(round(data[5] - 273.15)) + "°C"
        luftfeucht = str(data[2]) + "%"
        if windrichtung >= 0 and windrichtung <= 90:
            windrichtung = "NO"
        elif windrichtung == 0:
            windrichtung = "N"
        elif windrichtung == 90:
            windrichtung = "O"
        elif windrichtung >= 90 and windrichtung <= 180:
            windrichtung = "SO"
        elif windrichtung == 180:
            windrichtung = "S"
        elif windrichtung >= 180 and windrichtung <= 270:
            windrichtung ="SW"
        elif windrichtung == 270:
            windrichtung = "W"
        else:
            windrichtung = "NW"
        ausgabe = [self.stadt, temp, feels_like, windrichtung, windspeed, druck, luftfeucht]
        return ausgabe
    
pygame.init()

class stuff:
    def __init__(self, wo, was, scale):
        self.x = wo[0]
        self.y = wo[1]
        self.object = pygame.image.load(was)
        self.trans_obejct = pygame.transform.scale_by(self.object, (scale[0], scale[1]))
        self.rect = self.object.get_rect(center = (self.x, self.y))
    def draw(self):
        win.blit(self.trans_obejct, self.rect)

class Text(object):
    def __init__(self, wo, inhalt, art, größe, farbe):
        self.text = pygame.font.Font(art, größe)
        self.text_ren = self.text.render(inhalt, True, farbe)
        self.text_rect = self.text_ren.get_rect(center = (wo[0], wo[1]))
    
    def draw(self):
        win.blit(self.text_ren, self.text_rect)

searchbar = stuff((260, 40), ".\Assets\search.png.png", (0.7, 0.8))
bar = stuff((450, 450), ".\Assets\Copy of box.png", (1,1))
scope = stuff((315, 35), ".\Assets\Copy of search_icon.png", (1,1))
#framerate
win = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Wetterapp")
fps = pygame.time.Clock()
#bg
bg = pygame.image.load(".\Assets\Copy of logo.png").convert_alpha()
bg_trans = pygame.transform.scale_by(bg, (1.1, 1.1))
bg_rect = bg_trans.get_rect(center = (450, 200))
back = pygame.Surface((900, 500))
back.fill("White")


def sbarinput(text):
    searchbar_content = Text((175, 33), text, None, 38, "#FFFFFF")
    searchbar_content.draw()

def wetterausgabe(eingabe):
    ausgabe1 = Text((170, 455), eingabe[1], None, 38, "Black")
    ausgabe1.draw()
    ausgabe2 = Text((270, 455), eingabe[3], None, 38, "Black")
    ausgabe2.draw()
    ausgabe3 = Text((400, 455), eingabe[4], None, 38, "Black")
    ausgabe3.draw()
    ausgabe4 = Text((550, 455), eingabe[5], None, 38, "Black")
    ausgabe4.draw()
    ausgabe5 = Text((700, 455), eingabe[6], None, 38, "Black")
    ausgabe5.draw()

def keyboardInput(event,text, UIFeed):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            s = API(text)
            UIFeed = s.inf_ausgabe(s.inf_sorting(s.get()))
            print(UIFeed)
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += event.unicode
    if event.type == pygame.MOUSEBUTTONDOWN:
        if scope.rect.collidepoint(pygame.mouse.get_pos()):
            s = API(text)
            UIFeed = s.inf_ausgabe(s.inf_sorting(s.get()))
    return text, UIFeed

text = ""
UIFeed = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        text, UIFeed = keyboardInput(event, text, UIFeed)
    
    win.blit(back, (0, 0))
    searchbar.draw()
    sbarinput(text)
    scope.draw()
    bar.draw()
    if UIFeed != None:
        wetterausgabe(UIFeed)
    win.blit(bg_trans, bg_rect)
    pygame.display.update()
    fps.tick(60)











# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:07:30 2021

@author: Ayoub LABIB
"""

import pygame
import math
import time

pygame.init()

# definir une clock
clock = pygame.time.Clock()
fps = 60

COLOR_INACTIVE = pygame.Color(10, 10, 150)
COLOR_ACTIVE = pygame.Color(150, 150, 255)
FONT = pygame.font.Font(None, 32)

FONT.render("bonjour", 1, (255, 255, 255))


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global d_date
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    d_date = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Planète:
    def __init__(self, r, r_x, r_y, angle, tmps_rev, foyer, date_réf="12/2/1992", distance=0,
                 exentricité=0):  # date_réf : début de la vie intelligente sur Terre
        # la vitesse est relative au temps de révolution de la planète, pas de sa réelle vitesse
        self.r = r
        self.r_x = r_x
        self.r_y = r_y
        self.distance_focale = round(math.sqrt(self.r_x ** 2 - self.r_y ** 2) / 2,
                                     3)  # selon les formules des ellipses.
        self.angle = angle
        self.tmps_rev = tmps_rev  # entre 0.1 et 10 je dirai; eh bah non, cheh
        self.distance = distance
        self.foyer = foyer
        self.x = int(math.cos(self.angle * math.pi / 180) * self.r_x) + (self.foyer[0] - self.distance_focale)
        self.y = int(math.sin(self.angle * math.pi / 180) * self.r_y) + (self.foyer[1] - self.distance_focale)
        self.points = []
        self.compte = 0
        self.date_réf = date_réf


    def speed(self):

        acceleration = FONT.render("acceleration", 1, (255, 255, 255))
        fenetre.blit(acceleration, (5, 5))
        ralentir = FONT.render("ralentir", 1, (255, 255, 255))
        fenetre.blit(ralentir, (5, 40))

        # attention à la distance focale ! (distance entre le milieu de l'ellipse et un foyer aka le Soleil)

    def affich_orbite(self):
        # pygame.draw.ellipse(fenetre,(0,255,255),[self.foyer[0]-(self.r_x), self.foyer[1]-(self.r_y), self.r_x*2 , self.r_y*2],2)
        if self.compte <= 1:
            self.compte += 1
        elif not pause:
            self.compte += 1
            self.points.append([self.x + self.r / 2, self.y + self.r / 2])
            if len(self.points) >= 100:
                del self.points[0]
                self.compte = len(self.points)
        if d_date != "":
            self.points = []
        for i in range(len(self.points)):
            pygame.draw.circle(fenetre, (255, 255, 255), self.points[i], 2)
        pass

    def reinit_coord(self, planete):
        self.foyer = (planete.x, planete.y)

    def avancer_date(self):
        self.date = self.date  # complète Complette

    def calcul_angle(self):
        self.angle += 360 / self.tmps_rev
        self.angle %= 360

    def affiche_planet(self, image):
        self.x = int(math.cos(self.angle * math.pi / 180) * self.r_x) + self.foyer[0]
        self.y = int(math.sin(self.angle * math.pi / 180) * self.r_y) + self.foyer[1]
        fenetre.blit(image, (self.x, self.y))


def jour_suivant():  # date sous format "j m a"
    global date_
    global année_bissextile
    if not pause:
        data = [int(i) for i in date_.split(" ")]
        jours_mois = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # if data[0] > jours_mois[data[1]-1]:
        #     print("Erreur ! Jour invalide")
        # elif data[1] > 12:
        #     print("Erreur ! Mois invalide")
        # elif data[1] == 2 and data[0] == 29 and abs(data[2]) + abs(année_bissextile) % 4 != 0: # si jour bissextile mais que l'année ne l'est pas
        #     print("Erreur ! Année non bissextile")

        if data[0] == 31 and data[1] == 12:  # si c'est la fin de l'année
            date_ = "1 1 " + str(data[2] + 1)
            print("fin d'année")
        elif data[0] == jours_mois[data[1] - 1]:  # si c'est la fin du mois
            date_ = "1 " + str(data[1] + 1) + " " + str(data[2])
            print("fin du mois")
        # if data[1] == 2 and data[0] == 28 and abs(data[2]) + abs(année_bissextile) % 4 == 0: # si l'année est bissextile
        #     date_ = "29 2 " + str(data[2])
        #     pass
        # je garde au cas où, mais je ne pense pas que l'on ait besoin de ce cas (inclus dans le cas général)
        elif data[1] == 2 and data[0] == 28 and abs(data[2]) + abs(
                année_bissextile) % 4 != 0:  # si l'année n'est PAS bissextile
            date_ = "1 3 " + str(data[2])
        else:
            date_ = str(data[0] + 1) + " " + str(data[1]) + " " + str(data[2])
        for pl in planètes:
            pl.calcul_angle()


def date_en_deg(date, date_réf,
                temps_année):  # les dates doivent être en format "0/0/0", type "12/2/236" ou "1/10/1234242313" soit jour/mois/année
    # plutôt année_bis en global, et pourquoi pas faire des listes pour temps_année et date_réf (pour les planètes, plus simple)
    date_s = [int(i) for i in date.split(" ")]  # s pour split, donc des listes
    date_réf_s = [int(i) for i in date_réf.split(
        " ")]  # on définit la position de "date" en fonction de cette date réf. Si à date_réf la planète P est à un emplacement X, alors on veut savoir où se situe P par raport à X (distance en s)
    jours_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    date_m = sum(jours_mois[:date_s[1] - 1])  # mois into jours
    date_réf_m = sum(jours_mois[:date_réf_s[1] - 1])
    date_actuelle = date_s[0] + date_m + date_s[2] * 365.26  # .26, très important ^^
    date_référence = date_réf_s[0] + date_réf_m + date_réf_s[2] * 365.26

    temps = abs(date_actuelle - date_référence) % temps_année
    return round(temps / temps_année * 360,
                 3)  # en gros, où se situe la planète par rapport à un emplacement donné en degré


def date_demande(date_entree):
    global date_
    for pl in planètes:
        pl.angle = date_en_deg(date_entree, pl.date_réf, pl.tmps_rev)
    date_ = date_entree


pygame.display.set_caption("El systemo")

clock = pygame.time.Clock()

# Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((1500, 750))

# Chargement et collage du fond
fond = pygame.image.load("fond.jpg").convert()

# Chargement et collage du soleilnnage
taille_soleil = 70

# soleil=pygame.transform.scale(soleil,[taille_soleil,taille_soleil])

pret = True
coord_soleil = (440, 320)
année_bissextile = 2020

# Mercure = Planète(30, 116*0.65, 114*0.65, 0, 4.09091/10, coord_soleil)
# Vénus = Planète(30, 216*0.65, 216*0.65, 0, 1.6/10, coord_soleil)
# Terre = Planète(30, 299*0.65, 299*0.65, 0, 0.9843/10, coord_soleil)
# Lune = Planète(20, 30, 30, 0, 13.09091/10,(Terre.x, Terre.y))
# Mars = Planète(30, 456*0.65, 454*0.65, 0, 0.52402/10, coord_soleil)

Mercure = Planète(30, 116 * 0.65, 116 * 0.65, 0, 88, coord_soleil, "14 12 2021")
Vénus = Planète(30, 216 * 0.65, 216 * 0.65, 0, 225, coord_soleil, "2 11 2020")
Terre = Planète(30, 299 * 0.65, 299 * 0.65, 0, 365.25, coord_soleil, "2 11 2020")
Lune = Planète(20, 30, 30, 0, 27.5, (Terre.x, Terre.y), "2 11 2020")
Mars = Planète(30, 456 * 0.65, 456 * 0.65, 0, 687, coord_soleil, "24 9 2022")
Jupiter = Planète(80, 580 * 0.65, 580 * 0.65, 0, 4335, coord_soleil, "10 12 2022")  # pour cette planète et celles d'après, je n'ai pas pris les vraies valeurs
Saturne = Planète(55, 665 * 0.65, 665 * 0.65, 0, 10758, coord_soleil, "4 5 2022")
Uranus = Planète(30, 780 * 0.65, 780 * 0.65, 0, 30708, coord_soleil, "30 10 2022")
Neptune = Planète(30, 880 * 0.65, 880 * 0.65, 0, 60224, coord_soleil, "1 7 2023")

planètes = [Mercure, Vénus, Terre, Lune, Mars, Jupiter, Saturne, Uranus, Neptune]



images = ["Mercure.png", "Venus.png", "Terre.png", "Lune.png", "Mars.png", "Jupiter.png", "Saturne.png", "Uranus.png",
          "Neptune.png"]
for i in range(len(planètes)):
    img = pygame.image.load(images[i]).convert_alpha()
    img = pygame.transform.scale(img, [planètes[i].r, planètes[i].r])
    images[i] = img

forma = "%d %m %Y"


def calc_phase(date):
    ref = "13 03 2021"  # %d %m %Y

    refA = time.strptime(ref, forma)
    dateA = time.strptime(date, forma)

    ref_s = time.mktime(refA)
    date_s = time.mktime(dateA)

    diff_s = round(date_s - ref_s)
    diff_j = round(diff_s / (3600 * 24), 3)

    phase = round((diff_j % 29.5) * 29 / 29.5)
    # print(phase)
    if phase == 0:
        phase = 29
    elif phase < 0:
        phase = 29 - phase
    return phase

#def fonction_rotation():




def aff_lune():
    global date_

    phases = [str(i) + ".png" for i in range(1, 30)]  # liste avec noms des fichiers des phases

    img_l = pygame.image.load(phases[calc_phase(date_) - 1]).convert_alpha()
    img_l = pygame.transform.scale(img_l, [100, 100])
    fenetre.blit(img_l, (1045, 130))


d_date = "6 6 1992"
date_ = "12 2 1992"
date_demande(date_)
pause = False
pausebutton = button((10, 10, 150), 990, 500, 200, 50, "Pause")
playbutton = button((150, 150, 255), 990, 500, 200, 50, "Play")
date_button = button((10, 10, 150), 980, 50, 225, 50, date_)
input_box = InputBox(990, 400, 200, 32)

img_soleil = [
    pygame.transform.scale(pygame.image.load("1-" + str(i) + ".png").convert_alpha(), [taille_soleil, taille_soleil])
    for i in range(0, 60)]
c_s = 0
while pret:
    # Rafraîchissement de l'écran
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        input_box.handle_event(event)
    if event.type == pygame.QUIT:
        pygame.quit()
        pret = False
    if pausebutton.isOver(pos):
        print("pos is over")
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("ui")
            if pause:
                pause = False
            else:
                pause = True
            time.sleep(0.2)

    fenetre.blit(fond, (0, 0))
    acceleration_rect = pygame.draw.rect(fenetre, (0, 0, 0), (5, 5, 50, 30))
    ralentir_rect = pygame.draw.rect(fenetre, (0, 0, 0), (5, 30, 50, 30))
    pygame.draw.rect(fenetre, (0, 0, 30), (900, 0, 800, 800), 0)
    fenetre.blit(img_soleil[c_s], (coord_soleil[0] - taille_soleil / 2, coord_soleil[1] - taille_soleil / 2))

    c_s = (c_s + 1) % 59
    # fenetre.blit(soleil, (coord_soleil[0]-taille_soleil/2, coord_soleil[1]-taille_soleil/2)) # on peut le mettre en dehors de la boucle while ?
    date_button.draw(fenetre, (150, 150, 255))
    Lune.reinit_coord(Terre)
    date_button = button((10, 10, 150), 980, 50, 225, 50, date_)
    input_box.draw(fenetre)
    Planète.speed()
    # quand on fera un gif du  : une liste d'images, et k (emplacement de l'image) +=1 à chaque tour % len

    if not pause:
        pausebutton.draw(fenetre, (150, 150, 255))
        pausebutton.color = (10, 10, 150)

        if d_date == "":
            jour_suivant()
    else:
        playbutton.draw(fenetre, (150, 150, 255))

    if d_date != "":
        date_demande(d_date)

    aff_lune()
    for pl in range(len(planètes)):
        planètes[pl].affich_orbite()
        planètes[pl].affiche_planet(images[pl])

    if event.type == pygame.MOUSEMOTION:
        if pausebutton.isOver(pos):
            pausebutton.color = (150, 150, 255)

        else:
            pausebutton.color = (10, 10, 150)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if acceleration_rect.collidepoint(event.pos):
            fps += 10
            print(fps)
        if ralentir_rect.collidepoint(event.pos):
            fps -= 10
            print(fps)

    d_date = ""
    clock.tick(fps)
    pygame.display.update()

pygame.time.clock().tick(self.nbr_fps)

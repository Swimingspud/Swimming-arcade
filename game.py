#basic structure

#imports
import pygame, random, sqlite3, os
from pygame.sprite import *

#define classes


class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([46,62])
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,670)

    def setImage(self,graphicSelected):
        fallingObjectsImage = pygame.image.load(graphicSelected)
        self.image.blit(fallingObjectsImage,(0,0))
       
    def moveFallingObjects(self,distance):
        if self.rect.y <= 470:
            self.rect.y = self.rect.y + distance
    
    def deleteFallingObjects(self, oldscore):
        if self.rect.y > 470: 
            self.kill()
            newscore = oldscore +1
            return  newscore
        else:
            return oldscore

#Character class
class Character(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100,130])
        self.images = [pygame.image.load("Swimmer.png"), pygame.image.load("swimmer2.png")] #loading two images for animation
        self.image = self.images[0]
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = 310
        self.rect.y = 300
        self.animation_counter = 0 
        self.animation_speed = 15

    def moveCharacter(self,movement):

        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            # Change swimmer image every animation_speed frames
            self.animation_counter = 0
            if self.image == self.images[0]:
                self.image = self.images[1]
                self.image.set_colorkey(white)
            else:
                self.image = self.images[0]

        #movement for character    
        if self.rect.y >= 2 and self.rect.x + movement < 630:
            self.rect.x = self.rect.x + movement
        if self.rect.x < 2:
            self.rect.x = 2
        if self.rect.x > 639:
            self.rect.x = 630

#Button class
class Button:
    def __init__(self, screen, text, position, size, color, hover_color, text_color,type):
        self.screen = screen
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.type = type

    def draw(self, mouse_pos, page):
        rect = pygame.Rect(self.position, self.size)
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.hover_color, rect)
        else:
            pygame.draw.rect(self.screen, self.color, rect)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

        # Check for mouse click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if rect.collidepoint(event.pos):
                    if self.type == True:
                        page = "startscreen"
                    else:
                        page = "game"
        return page
    
#database
class database():

    #reading data from database
    def read():

        data = []
        sql_read_name = ''' SELECT Name FROM scores; '''
        sql_read_score = ''' SELECT userscore FROM scores;'''


        path = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(path, "scores.db")
        db = sqlite3.connect(file)
        cursor = db.cursor()
        #getting names
        cursor.execute(sql_read_name)
        data = cursor.fetchall()
        namearray = [list(row) for row in data]
        #getting scores
        cursor.execute(sql_read_score)
        data = cursor.fetchall()
        scorearray = [list(row) for row in data]
        db.close()

        return namearray, scorearray

    #adding username and score to the database
    def add(username, score):
        datatoadd = (username, score)
         
        sql_adddata = ''' INSERT INTO scores(Name,userscore)
                  VALUES(?,?) '''

        path = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(path, "scores.db")
        db = sqlite3.connect(file)
        cursor = db.cursor()
        cursor.execute(sql_adddata, datatoadd)
        db.commit()
        db.close()

    #sorting queried data with a bubble sort
    def sort(namearray, scorearray):
        ntemp = ""
        stemp = 0

        #Bubble sort
        for index in range(len(scorearray) - 1):
            for index in range(len(scorearray) - 1):
                if scorearray[index] < scorearray[index + 1]:
                    stemp = scorearray[index]
                    ntemp = namearray[index]
                    scorearray[index] = scorearray[index + 1]
                    namearray[index] = namearray[index + 1]
                    scorearray[index + 1 ] = stemp
                    namearray[index + 1] = ntemp
        return namearray, scorearray
    



pygame.init() #start pygame

screen = pygame.display.set_mode([700,500]) #set screen size
pygame.display.set_caption("swim arcade") #name of window
background_image = pygame.image.load("Pool.png").convert()
done = False 
clock = pygame.time.Clock() #ammage speed of screen updates
black = (0,0,0)
white = (255,255,255)
font = pygame.font.Font(None,36)

#Dglobal variables
allFallingObjects = pygame.sprite.Group()
nextfloat = pygame.time.get_ticks() + random.randint(2500,5000)

charatersGroup = pygame.sprite.Group()
character = Character()
charatersGroup.add(character)

buttons = [] #buttons array for button objects

movement = 0
score = 0
speed = 10
animate = 0
page = False

page = "startscreen" #sets the game screen to startscreen. Can be changed for testing.

#Creating and adding buttons to an array.
button = Button(screen, "start again", (490, 10), (200, 80), (100, 100, 100), (150, 150, 150), (255, 255, 255), True)
buttons.append(button)
button = Button(screen, "restart game", (10,10), (200, 80), (100, 100, 100), (150, 150, 150), (255, 255, 255), False)
buttons.append(button)
# Get mouse position
mouse_pos = pygame.mouse.get_pos()

#-------------main program-------------#

while not done:

#start screen of game
    if page == "startscreen":
    
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(250, 300, 140, 32)
        color = pygame.Color("white")
        active = False
        text = ''
        game = False

        while not game:
            for event in pygame.event.get():
    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #check if mouse clicks on the box
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                #Getting what the user enters in the text box        
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if len(text) > 0:
                                game = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

                        
            screen.fill((0,51,102))
            width = 200
            pygame.draw.rect(screen, color, input_box, 2)
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            start_message = font.render("Click on the box and enter name and press enter to begin.", 1, white)
            screen.blit(start_message, (10,100))
            username = text
            page = "game"
            pygame.display.flip()

    elif page == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movement =- speed
                if event.key == pygame.K_RIGHT:
                    movement = speed
            if event.type == pygame.KEYUP:
                movement = 0

        #Update sprites
        if pygame.time.get_ticks() > nextfloat:
            nextObject = FallingObject()
            nextObject.setImage("float.png")
            allFallingObjects.add(nextObject)
            nextfloat = pygame.time.get_ticks() + random.randint(750, 3000)

        for eachObject in (allFallingObjects.sprites()):
            eachObject.moveFallingObjects(10)

            score = eachObject.deleteFallingObjects(score)

        character.moveCharacter(movement)

        collisions = pygame.sprite.groupcollide(allFallingObjects,charatersGroup,False,False)
        if len(collisions) > 0:
            database.add(username,score)
            page = "endscreen"

        screen.blit(background_image, [0,0])

        allFallingObjects.draw(screen)
        charatersGroup.draw(screen)
        textImg = font.render(str(score),1,white)
        screen.blit(textImg,(10,10))
        pygame.display.flip() #update screen with what was drawn
        clock.tick(40)


    elif page == "endscreen":
        
        # Reset character position
        character.rect.x = 310
        character.rect.y = 300
        # Clear falling objects
        allFallingObjects.empty()
        # Reset score
        score = 0
        #reset collisions
        collisions = 0
        #reset movement to 0 so charater doesnt move 
        movement = 0 
 
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        # Fill the screen with background color
        screen.fill((0,51,102))
    
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
    
        # Draw buttons

        for button in buttons:
            page = button.draw(mouse_pos, page)

    
        #getting score and name arrays
        namearray, scorearray = database.read()
        namearray, scorearray = database.sort(namearray, scorearray)
    
        font = pygame.font.Font(None, 36)
        y = 120 #starting y axsis for displaying names
    
        #cheching to see if the length of the name array is greater than 5
        if len(namearray) < 5:
            lengthofloop = len(namearray)
        else:
            lengthofloop = 5
    
        #display scores to screen
        for index in range(lengthofloop):
            iteamtodisplay = str(namearray[index]) + "  " + str(scorearray[index])
            display = str(iteamtodisplay).replace('[','').replace(']','').replace('\'','').replace('\"','') #remove undwanted character
            text = font.render(str(display), 1 , white)
            screen.blit(text, (300,y))
            y += 50
        pygame.display.flip()
        clock.tick(40)
pygame.quit()



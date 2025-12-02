#relative pack packer
import sys
import os
import random
import pygame

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#difficulty reps the percenage of bombs from 0 to 1
def minefieldGen(length, difficulty):
 
    #size of square based on length of sides where length * length is size of field
    minefield = []
    # define a list that stores the information for 
    for i in range(length ** 2):
 
        if (random.random()<difficulty):
            minefield.append("x")
        # approx add 15.6 % of mines for medium difficulty
        else:
            minefield.append(0)
        
    for i in range(length**2):
        #creating numbers
        if minefield[i]!= "x":
            # Overall just checking surroundings of a square to check the # of bombs
            if (minefield[i-1] == "x" and i - 1 >= 0 and i % length != 0):
            #check to avoid undefined list values
                minefield[i] = minefield[i] + 1
            if((i+1)<length**2):
                if (minefield [i+1] == "x" and (i+1) % length != 0):
                    minefield[i] = minefield[i] + 1
            if(minefield [i-length] =="x" and i-length >=0 ):
                minefield[i] = minefield[i] + 1
            if(minefield [i-length-1] =="x" and i-length >=0 and i % length != 0):
                minefield[i] = minefield[i] + 1
            if(minefield [i-length+1] =="x" and i-length >=0 and (i+1) % length != 0):
                minefield[i] = minefield[i] + 1
        
            if(i+length < (length**2)):
            
                if(minefield [i+length] =="x"):
                    minefield[i] = minefield[i] + 1
            if(i+length < (length**2)-1):
                if(minefield [i+length+1] =="x" and (i + 1) % length != 0):
                    minefield[i] = minefield[i] + 1
            if i+length < (length**2):
                if(minefield [i+length-1] =="x" and i % length != 0 ):
                    minefield[i] = minefield[i] + 1
    return([str(field) for field in minefield])


# Setup for eight way fill to clear empty spaces
def dfs(field, entry, length, last):
    chunks = [field[x:x+length] for x in range(0, len(field), length)] #Field list of numbers and x's data type string
    x = entry % length
    y = entry // length
    #checking if the entry breaks bounds or is a protected type or if last wasnt a 0
    if (x < 0 or x >= length or y < 0 or y >= length) or chunks[y][x] == "x" or chunks[y][x][-1] == "f" or chunks[y][x][-1] == "c" or last != "0":
        return field
    
    last = chunks[y][x]
    # marking all cleared tiles for later clearance
    chunks[y][x] = chunks[y][x] + "c"

    field = sum(chunks, []) #
    

   
    # protecting the right checking dfs from reccursison
    if (entry + 1) % length != 0:
        field = dfs(field, entry + 1, length, last)
        field = dfs(field, entry + length + 1, length, last)
        field = dfs(field, entry - length + 1, length,last)
    #protecting the left seeking dfs from infinite reccursion
    if entry % length != 0:
        field = dfs(field, entry - 1, length,last)
        field = dfs(field, entry + length - 1, length,last)
        field = dfs(field, entry - length - 1, length,last)
    field = dfs(field, entry + length, length,last)
    field = dfs(field, entry - length, length,last)
    
    
    return field

    


# pygame setup
pygame.init()
#font intialization

pygame.font.init()
asset_url = resource_path('Assets/Robotfont.ttf')
Robo = pygame.font.Font(asset_url,28)
title = pygame.font.Font(asset_url,50)
# creating screen dimensions
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()

#importing purple colours 
asset_url = resource_path('Assets/PurpCover.PNG')
Purpcover = pygame.image.load(asset_url)
#importing numbers
asset_url = resource_path('Assets/1_pixel.GIF')
one = pygame.image.load(asset_url)
asset_url = resource_path('Assets/2_pixel.GIF')
two = pygame.image.load(asset_url)
asset_url = resource_path('Assets/3_pixel.GIF')
three = pygame.image.load(asset_url)
asset_url = resource_path('Assets/4_pixel.GIF')
four = pygame.image.load(asset_url)
asset_url = resource_path('Assets/5_pixel.GIF')
five = pygame.image.load(asset_url)
asset_url = resource_path('Assets/6_pixel.GIF')
six = pygame.image.load(asset_url)
asset_url = resource_path('Assets/7_pixel.GIF')
seven = pygame.image.load(asset_url)
asset_url = resource_path('Assets/8_pixel.GIF')
eight = pygame.image.load(asset_url)
asset_url = resource_path('Assets/Bomb.GIF')
bomb = pygame.image.load(asset_url)
asset_url = resource_path('Assets/Flag.GIF')
flag = pygame.image.load(asset_url)

asset_url = resource_path('Assets/Button_v1.GIF')
button = pygame.image.load(asset_url)



#Creating the rect elements that represent the position and hitbox of the sprites
def gridmaker(length):
    x = int((1280 - length*26)/2)
    y = int((720 - length * 26)/2)
    grid = []
    # finding where the top left of the first sprite is by going from center 
    # and then moving left and up based on amount of squares
   
    for i in range (length ** 2):
        grid.append(pygame.Rect(x,y,26,26))
        if (i+1) % length != 0:
            x += 26
        else:
            x = x - ((length - 1) * 26)
            y = y + 26
            
    return grid

# creates a square grid the size of the input

# background color
back = (181,199,235)

def easy():
    length = 10
    x = int((1280 - length*26)/2)
    y = int((720 - length * 26)/2)
    grid = gridmaker(length)
    minefield = minefieldGen(length,0.123)
    FieldBack = pygame.Rect(x,y,26 * length,26 * length)
    running = True
    Cleared = []
    Flag = []
    FirstClick = 0
    end = 0
    startTime = pygame.time.get_ticks()
    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                end = 2
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = event.pos
                
                

                GridCounter = 0 
                for sprite in grid:
                    
                # Right-click
                    if event.button == 3:
                        # checking if square is already flagged
                        if sprite.collidepoint(mouse_pos):
                            if sprite in Flag:
                            #   removing the flagged square from the list
                                Flag.remove(sprite)
                                minefield[GridCounter] = (minefield[GridCounter])[0]
                            elif sprite not in Cleared:
                                # flagging by adding flagged to the list
                                Flag.append(sprite)
                                minefield[GridCounter] = minefield[GridCounter] + "f"
                            break  # stop after handling the first clicked square
                    # left click
                    if event.button == 1:
                        # if it clicks a sprite from the grid
                        if sprite.collidepoint(mouse_pos):
                            if FirstClick == 0 and minefield[GridCounter] != '0':
                                while minefield[GridCounter] != '0':  
                                    minefield = minefieldGen(length,0.123)
                            FirstClick +=1

                            #checking if the sprite is in flag
                            if sprite not in Flag:
                                if minefield[GridCounter] == "x":
                                    Cleared.append(sprite)
                                minefield = dfs(minefield, GridCounter, length,"0")
                                
                
                    GridCounter += 1
                
                counter = 0
                flaggedcorrect = 0
                cleared = 0
                bombNum = 0
                #rechecking the grid for any that end with c and clearing it
                for sprite in grid:
                    if minefield[counter][-1] == "c":
                        Cleared.append(sprite)
                        cleared+=1
                    if minefield[counter][0] == "x":
                        bombNum +=1

                    if minefield[counter] == "xf":
                        flaggedcorrect += 1
                    if flaggedcorrect == bombNum and counter == length ** 2 -1:
                        end = 3
                    
                    counter+=1
            

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(back)
        pygame.draw.rect(screen,(255,255,197), (x , y ,26 * length,26 * length))
    
        for item in range(len(grid)):
            # checking if the bomb was clicked and ENDING NEEDS TO BE MADE
            if minefield[item] == "x" and grid[item] in Cleared:
                
                end = 1
            # generating numbers and bombs first to be under tiles

            if minefield[item][0] == "x":
                screen.blit(bomb,grid[item])

            if minefield[item][0] == '1':
                screen.blit(one,grid[item])
            if minefield[item][0] == '2':
                screen.blit(two,grid[item])
            if minefield[item][0] == '3':
                screen.blit(three,grid[item])
            if minefield[item][0] == '4':
                screen.blit(four,grid[item])    
            if minefield[item][0] == '5':
                screen.blit(five,grid[item])
            if minefield[item][0] == '6':
                screen.blit(six,grid[item])
            if minefield[item][0] == '7':
                screen.blit(seven,grid[item])
            if minefield[item][0] == '8':
                screen.blit(eight,grid[item])
            #printing only non cleared and not covering when game is ove on x
            if grid[item] not in Cleared and end != 3:
                screen.blit(Purpcover,grid[item])
            # printing flags
            if grid[item] in Flag and end == 0:
                screen.blit(flag,grid[item])
        if end == 1:
            for item in range(len(grid)):
                if minefield[item][0] == "x":
                    screen.blit(bomb,grid[item])
        
        if end == 1:
            screen.blit((title.render('YOU LOST',True, (0,0,0))), (50,360))
            
        
        if end == 3:
            screen.blit((title.render('YOU WON',True, (0,0,0))), (50,360))
        
        screen.blit(title.render(str((pygame.time.get_ticks()- startTime)/1000), True,(0,0,0)), (50,480))

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()
        if end == 1:
            pygame.time.delay(3000)
            running = False
            return "main"
        if end == 2:
            running = False
            return "end"
        if end == 3:
            pygame.time.delay(3000)
            running = False
            return "main"
    clock.tick(60)  # limits FPS to 60

    pygame.quit()
    

def medium():
    length = 20
    x = int((1280 - length*26)/2)
    y = int((720 - length * 26)/2)
    grid = gridmaker(length)
    minefield = minefieldGen(length,0.156)
    FieldBack = pygame.Rect(x,y,26 * length,26 * length)
    running = True
    Cleared = []
    Flag = []
    FirstClick = 0
    end = 0
    startTime = pygame.time.get_ticks()
    while running:
    
         
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
              
            if event.type == pygame.QUIT:
                end = 2
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = event.pos
                
                

                GridCounter = 0 
        
                for sprite in grid:
                    
                # Right-click
                    if event.button == 3:
                        # checking if square is already flagged
                        if sprite.collidepoint(mouse_pos):
                            if sprite in Flag:
                            #   removing the flagged square from the list
                                Flag.remove(sprite)
                                minefield[GridCounter] = (minefield[GridCounter])[0]
                            elif sprite not in Cleared:
                                # flagging by adding flagged to the list
                                Flag.append(sprite)
                                minefield[GridCounter] = minefield[GridCounter] + "f"
                            break  # stop after handling the first clicked square
                    # left click
                    if event.button == 1:
                        # if it clicks a sprite from the grid
                        if sprite.collidepoint(mouse_pos):
                            if FirstClick == 0 and minefield[GridCounter] != '0':
                                while minefield[GridCounter] != '0':  
                                    minefield = minefieldGen(length,0.156)
                            FirstClick +=1

                            #checking if the sprite is in flag
                            if sprite not in Flag:
                                if minefield[GridCounter] == "x":
                                    Cleared.append(sprite)
                                minefield = dfs(minefield, GridCounter, length,"0")
                                
                
                    GridCounter += 1
                
                counter = 0
                flaggedcorrect = 0
                cleared = 0
                bombNum = 0
                #rechecking the grid for any that end with c and clearing it
                for sprite in grid:
                    if minefield[counter][-1] == "c":
                        Cleared.append(sprite)
                        cleared+=1
                    if minefield[counter][0] == "x":
                        bombNum +=1

                    if minefield[counter] == "xf":
                        flaggedcorrect += 1
                    if flaggedcorrect == bombNum and counter == length ** 2 -1:
                        end = 3
                    
                    counter+=1
            

        # fill the screen with a color to wipe away anything from last frame
            pygame.draw.rect(screen,(255,255,197), (x , y ,26 * length,26 * length))       
            
            for item in range(len(grid)):
                
                # checking if the bomb was clicked and ENDING NEEDS TO BE MADE
                if minefield[item] == "x" and grid[item] in Cleared:
                    
                    end = 1
                # generating numbers and bombs first to be under tiles

                if minefield[item][0] == "x":
                    screen.blit(bomb,grid[item])

                if minefield[item][0] == '1':
                    screen.blit(one,grid[item])
                if minefield[item][0] == '2':
                    screen.blit(two,grid[item])
                if minefield[item][0] == '3':
                    screen.blit(three,grid[item])
                if minefield[item][0] == '4':
                    screen.blit(four,grid[item])    
                if minefield[item][0] == '5':
                    screen.blit(five,grid[item])
                if minefield[item][0] == '6':
                    screen.blit(six,grid[item])
                if minefield[item][0] == '7':
                    screen.blit(seven,grid[item])
                if minefield[item][0] == '8':
                    screen.blit(eight,grid[item])
                #printing only non cleared and not covering when game is ove on x
                if grid[item] not in Cleared and end != 3:
                    screen.blit(Purpcover,grid[item])
                # printing flags
                if grid[item] in Flag and end == 0:
                    screen.blit(flag,grid[item])

            if end == 1:
                for item in range(len(grid)):
                    if minefield[item][0] == "x":
                        screen.blit(bomb,grid[item])

                

            

            

        
       
        
        pygame.draw.rect(screen, back, (50,480,200,100))
        screen.blit(title.render(str((pygame.time.get_ticks()- startTime)/1000), True,(0,0,0)), (50,480))
            # flip() the display to put your work on screen
        pygame.display.flip()
        if end == 1:
                screen.blit((title.render('YOU LOST',True, (0,0,0))), (50,360))
                
            
        if end == 3:
                screen.blit((title.render('YOU WON',True, (0,0,0))), (50,360))
        if end == 1:
            pygame.time.delay(3000)
            running = False

            return "main"
        if end == 2:
            running = False
            return "end"
        if end == 3:
            pygame.time.delay(3000)
            running = False
            return "main"
    clock.tick(60)  # limits FPS to 60
    pygame.quit()
    '''for i in range(length**2):
        if (i + 1)%length == 0:
            print(minefield[i], end = "\n")
        else:
            print(minefield[i], end=" ")'''

def hard():
    length = 25
    x = int((1280 - length*26)/2)
    y = int((720 - length * 26)/2)
    grid = gridmaker(length)
    minefield = minefieldGen(length,0.20)
    FieldBack = pygame.Rect(x,y,26 * length,26 * length)
    running = True
    Cleared = []
    Flag = []
    FirstClick = 0
    end = 0
    startTime = pygame.time.get_ticks()
    screen.fill(back)
    while running:
    
         
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
              
            if event.type == pygame.QUIT:
                end = 2
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = event.pos
                
                

                GridCounter = 0 
        
                for sprite in grid:
                    
                # Right-click
                    if event.button == 3:
                        # checking if square is already flagged
                        if sprite.collidepoint(mouse_pos):
                            if sprite in Flag:
                            #   removing the flagged square from the list
                                Flag.remove(sprite)
                                minefield[GridCounter] = (minefield[GridCounter])[0]
                            elif sprite not in Cleared:
                                # flagging by adding flagged to the list
                                Flag.append(sprite)
                                minefield[GridCounter] = minefield[GridCounter] + "f"
                            break  # stop after handling the first clicked square
                    # left click
                    if event.button == 1:
                        # if it clicks a sprite from the grid
                        if sprite.collidepoint(mouse_pos):
                            if FirstClick == 0 and minefield[GridCounter] != '0':
                                while minefield[GridCounter] != '0':  
                                    minefield = minefieldGen(length,0.20)
                            FirstClick +=1

                            #checking if the sprite is in flag
                            if sprite not in Flag:
                                if minefield[GridCounter] == "x":
                                    Cleared.append(sprite)
                                minefield = dfs(minefield, GridCounter, length,"0")
                                
                
                    GridCounter += 1
                
                counter = 0
                flaggedcorrect = 0
                cleared = 0
                bombNum = 0
                #rechecking the grid for any that end with c and clearing it
                for sprite in grid:
                    if minefield[counter][-1] == "c":
                        Cleared.append(sprite)
                        cleared+=1
                    if minefield[counter][0] == "x":
                        bombNum +=1

                    if minefield[counter] == "xf":
                        flaggedcorrect += 1
                    if flaggedcorrect == bombNum and counter == length ** 2 -1:
                        end = 3
                    
                    counter+=1
            

        # fill the screen with a color to wipe away anything from last frame
            pygame.draw.rect(screen,(255,255,197), (x , y ,26 * length,26 * length))       
            
            for item in range(len(grid)):
                
                # checking if the bomb was clicked and ENDING NEEDS TO BE MADE
                if minefield[item] == "x" and grid[item] in Cleared:
                    
                    end = 1
                # generating numbers and bombs first to be under tiles

                if minefield[item][0] == "x":
                    screen.blit(bomb,grid[item])

                if minefield[item][0] == '1':
                    screen.blit(one,grid[item])
                if minefield[item][0] == '2':
                    screen.blit(two,grid[item])
                if minefield[item][0] == '3':
                    screen.blit(three,grid[item])
                if minefield[item][0] == '4':
                    screen.blit(four,grid[item])    
                if minefield[item][0] == '5':
                    screen.blit(five,grid[item])
                if minefield[item][0] == '6':
                    screen.blit(six,grid[item])
                if minefield[item][0] == '7':
                    screen.blit(seven,grid[item])
                if minefield[item][0] == '8':
                    screen.blit(eight,grid[item])
                #printing only non cleared and not covering when game is ove on x
                if grid[item] not in Cleared and end != 3:
                    screen.blit(Purpcover,grid[item])
                # printing flags
                if grid[item] in Flag and end == 0:
                    screen.blit(flag,grid[item])

            if end == 1:
                for item in range(len(grid)):
                    if minefield[item][0] == "x":
                        screen.blit(bomb,grid[item])

                

            

            

        
       
        
        pygame.draw.rect(screen, back, (50,480,200,100))
        screen.blit(title.render(str((pygame.time.get_ticks()- startTime)/1000), True,(0,0,0)), (50,480))
            # flip() the display to put your work on screen
        pygame.display.flip()
        if end == 1:
                screen.blit((title.render('YOU LOST',True, (0,0,0))), (50,360))
                
            
        if end == 3:
                screen.blit((title.render('YOU WON',True, (0,0,0))), (50,360))
        if end == 1:
            pygame.time.delay(3000)
            running = False

            return "main"
        if end == 2:
            running = False
            return "end"
        if end == 3:
            pygame.time.delay(3000)
            running = False
            return "main"
    clock.tick(60)  # limits FPS to 60
    pygame.quit()
#main menu pygame
def main_menu():
    Running = True
    #easy text
    easy = Robo.render(' EASY',True, (255,255,255))
    easy_button = pygame.Rect(640-152/2 ,200,125,52)
    #medium text

    med = Robo.render(' MEDIUM',True, (255,255,255))
    med_button = pygame.Rect(640-152/2 ,300,125,52)

    hard = Robo.render(' HARD',True, (255,255,255))
    hard_button = pygame.Rect(640-152/2 ,400,125,52)

    Title = title.render('MINESWEEPAH',True, (0,0,0))
    
    while Running:
        # Process player inputs.
        for event in pygame.event.get():
            #quit
            if event.type == pygame.QUIT:
                Running=False
                return "end"
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = event.pos
                if med_button.collidepoint(mouse_pos):
                    Running = False
                    return "med"
                if easy_button.collidepoint(mouse_pos):
                    Running = False
                    return "easy"
                if hard_button.collidepoint(mouse_pos):
                    Running = False
                    return "hard"
                 

        

        screen.fill(back)  # Fill the display with a solid color
        screen.blit(button,med_button)
        screen.blit(med, (640-152/2+3,300+8,125,52))
        screen.blit(button,easy_button)
        screen.blit(easy, (640-152/2+3 + 20,200+8,125,52))
        screen.blit(button,hard_button)
        screen.blit(hard, (640-152/2+3,400+8,125,52))
        screen.blit(Title, (640-183,100))
        screen.blit(button,hard_button)
        screen.blit(hard, (640-152/2+3 +20,400+8,125,52))


        # Render the graphics here.
        # ...

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # wait until next frame (at 60 FPS)
    pygame.quit()
gamestate = "main"

while gamestate != "end":
    if gamestate == "main":
        gamestate = (main_menu())
    
    if gamestate == "med":
        gamestate = (medium())
    if gamestate == "easy":
        gamestate = (easy())
    if gamestate == "hard":
        gamestate = (hard())


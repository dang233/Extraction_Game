import pygame, math, random
pygame.init()
class Background(pygame.sprite.Sprite):
    """A general background for the game, used with defeat and win screens"""
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class world_location():
    """Allows the world location to be used with other assets"""
    def __init__(self):
        self.posX = 0
        self.posY = 0

class ship(pygame.sprite.Sprite):
    """the ship is considered the player. This class houses all the players movement functions"""
    def __init__(self, screen):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.screenPosX, self.screenPosY = screen.get_size()
        self.last_keys = ""
        self.hitbox = (self.screenPosX/2, self.screenPosY/2, 0, 0) # sets the hitbox to zero along with it's size
        
        self.health_max = 100
        self.health = self.health_max

        self.energy_max = 200
        self.energy = self.energy_max

        self.vel = 5

    def ship_direction(self):
        """switches the image of the player depending on what key is pressed"""
        if self.keys[pygame.K_w] or self.last_keys == "w":
            self.image = pygame.image.load(r"test_ship_up.png")
        elif self.keys[pygame.K_s] or self.last_keys == "s":
            self.image = pygame.image.load(r"test_ship_down.png")
        elif self.keys[pygame.K_a] or self.last_keys == "a":
            self.image = pygame.image.load(r"test_ship_left.png")
        elif self.keys[pygame.K_d] or self.last_keys == "d":
            self.image = pygame.image.load(r"test_ship_right.png")
        else:
            self.image = pygame.image.load(r"test_ship_up.png")
    
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_width()/2
        self.rect.centery = self.screen.get_height()/2

        self.hitbox = (self.screenPosX/2 - 25, self.screenPosY/2 - 25, 50, 50) #Hitbox is now 50 by 50 pixels

    def render(self):
        pygame.draw.aaline(self.screen, (255, 0, 0), (self.screenPosX/2, self.screenPosY/2), (self.mousePos[0], self.mousePos[1]), 1)
        #pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox, 1) #Basically draws the hitbox
        self.screen.blit(self.image, (self.rect.centerx - 50, self.rect.centery - 50)) #Makes it so the image is drawn on the screen from the middle

    def run(self, keys, mousePos, last_keys):
        """ Purpose of this function is to obtain user input and process them. Ontains the key pressed and mouse position. Returns nothing. """
        #Allows the ship to stay in the same position after key press
        self.keys = keys
        if self.keys[pygame.K_w]:
            self.last_keys = "w"
        if self.keys[pygame.K_s]:
            self.last_keys = "s"
        if self.keys[pygame.K_a]:
            self.last_keys = "a"
        if self.keys[pygame.K_d]:
            self.last_keys = "d"
        self.mousePos = mousePos

        ship.ship_direction(self)
        ship.render(self)

class projectile():
    """A sprite that is used to calculate the trijectory of bullets and draw them on screen"""
    def __init__(self, screen, x, y, radius, colour, mouse, damage, speed, btype = "player"):
        self.screen = screen
        self.posX = x
        self.posY = y
        
        self.radius = radius
        self.colour = colour
        self.vel = speed
        self.damage = damage
        self.type = btype

        self.mouse = mouse


    def update_pos(self, up, down, left, right):
        """Updates the bullets to correlate with the screen"""

        self.posY += up
        self.posY -= down
        self.posX += left
        self.posX -= right

        self.currentx = self.mouse[0]
        self.currenty = self.mouse[1]

    def render(self, screen, x = None, y = None):
        self.update_pos(0, 0, 0, 0)
        if x or y != None:
            self.currentx = x
            self.currenty = y
        self.x_diff = self.currentx - self.screen.get_width()/2
        self.y_diff = self.currenty - self.screen.get_height()/2

        self.angle = math.atan2(self.y_diff, self.x_diff) # Calculates the angle to shoot from
        self.posX += int(math.cos(self.angle) * self.vel)
        self.posY += int(math.sin(self.angle) * self.vel)
        pygame.draw.circle(screen, self.colour, (self.posX, self.posY), self.radius)

### RANDOMIZERS FOR THE PLANET CLASS
def name_random():
    """Generates a random name that the planet will be mentioned by. Takes nothing and returns a generated name."""
    random_pick1 = random.randint(0, 4)
    random_pick2 = random.randint(0, 4)
    random_pick3 = random.randint(0, 4)
    name_list1 = ["MESO", "AXI", "LITH", "LF", "NEO"]
    random_number = random.randint(0, 99)
    name_list2 = ["A", "B", "C", "D", "Z"]
    name_list3 = ["15", "023", "E", "8", "2"]
    return name_list1[random_pick1] + "-" + str(random_number) + name_list2[random_pick2] + name_list3[random_pick3] # Creates a custom and unique name

def temperature_random():
    random_pick = random.randint(-99, 300)
    return random_pick

def advancement_random():
    random_pick = random.randint(1, 3)
    return random_pick

def surface_random():
    random_pick = random.randint(0, 5)
    surface_list = ["Rocky", "Oceans", "Land", "Lava", "Deserts", "Gas"]
    return surface_list[random_pick]

def random_planet(surface):
    if surface == "Oceans" or surface == "Gas":
        return pygame.image.load(r"pixelized_moon_blue.png")
    elif surface == "Rocky":
        return pygame.image.load(r"pixelized_moon.png")
    elif surface == "Oceans" or surface == "Gas":
        return pygame.image.load(r"pixelized_moon_blue2.png")
    elif surface == "Land":
        return pygame.image.load(r"pixelized_moon_green.png")
    elif surface == "Gas":
        return pygame.image.load(r"planet_rings_purple.png")
    elif surface == "Deserts" or surface == "Lava":
        return pygame.image.load(r"pixelized_moon_brown.png")

class planet(pygame.sprite.Sprite):
    """The planet includes all of its uses. Quest, shop, recharge, repair. Planet stats are randomized"""
    def __init__(self, screen, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        self.screenx, self.screeny = screen.get_size()
        self.posX = posX # Sets the original planet point
        self.posY = posY
        self.render_menu = False
        self.render_shop = False
        self.timer = 0

        # Listing information for the user to see
        self.name = name_random()
        self.temperature = temperature_random()
        self.advancement = advancement_random()
        self.surface = surface_random()
        self.image = random_planet(self.surface)
        self.rect = self.image.get_rect()
        self.visited = False
        self.repair_cost = 500
        self.charge_cost = 500

        self.random_weapon = random.randint(0, 3) #item is randomized only once
        self.random_upgrade = random.randint(0, 2)

    def check_hover(self, x, y, keys):
        """ """
        if self.posX + x - 50 < 400 < self.posX + x + 50 and self.posY + y - 50 < 300 < self.posY + y + 50:
            pygame.draw.circle(self.screen, (0, 250, 0), (self.posX + x, self.posY + y), 10)
            if keys[pygame.K_e]:
                return True
        else:
            pygame.draw.circle(self.screen, (0, 150, 0), (self.posX + x, self.posY + y), 10)

    def discovered(self):
        title_font = pygame.font.SysFont("Tahoma", 45, bold=True)
        discover_title = title_font.render("DISCOVERED " + self.name, 1, (150, 150, 150))

        if self.timer < 400:
            self.screen.blit(discover_title, (-300 + 4 * self.timer, 30))
            self.timer += 1.4
        if self.timer > 400: # prompt of discovering the planet is shown for 5 seconds
            planet.visited = True

    def render(self, x, y): ### CHANGE THIS NAME TO RUN
        self.new_posX = x + self.posX # moves the planet's x coordinate to a new position
        self.new_posY = y + self.posY # moves the planet's y coordinate to a new position
        self.screen.blit(self.image, (self.new_posX, self.new_posY))
        #pygame.draw.circle(self.screen, (0, 0, 255), (self.new_posX, self.new_posY), 20)

    def shop(self, mouse, buttondown):
        myfont = pygame.font.SysFont("Tahoma", 20, bold=True)
        shop_font = pygame.font.SysFont("Tahoma", 30, bold=True)
        shop_text = shop_font.render("SHOP", 1, (17, 17, 17))
        weapons = ["Blaster", "Laser", "Flamer", "Energy Ball", "Nothing in Stock"]
        upgrades = ["Energy (+50)", "Health (+75)", "Damage (x0.2)"]


        self.item1 = weapons[self.random_weapon] # Make sure that the planet randomizes items in the shop
        #Setting the item prices for each weapon
        if self.item1 == "Laser":
            self.item1_price = 7000
        elif self.item1 == "Blaster":
            self.item1_price = 3000
        elif self.item1 == "Flamer":
            self.item1_price = 3000
        elif self.item1 == "Energy Ball":
            self.item1_price = 5000
        item1_text = myfont.render(self.item1, 1, (17, 17, 17))
        item1_price_text =  myfont.render("Cost:" + str(self.item1_price), 1, (17, 17, 17))

        self.item2 = upgrades[self.random_upgrade]
        #Setting the item prices for each upgrade
        if self.item2 == "Health (+75)":
            self.item2_price = 1600
        elif self.item2 == "Energy (+50)":
            self.item2_price = 1600
        elif self.item2 == "Damage (x0.2)":
            self.item2_price = 1600
        item2_text = myfont.render(self.item2, 1, (17, 17, 17))
        item2_price_text =  myfont.render("Cost:" + str(self.item2_price), 1, (17, 17, 17))

        #item2_text = myfont.render("Flamer", 1, (17, 17, 17))
        #item3_text = myfont.render("Shield Abil", 1, (17, 17, 17))
        #item4_text = myfont.render("Dmg Upgrade", 1, (17, 17, 17))

        pygame.draw.rect(self.screen, (86, 86, 86), (self.screenx/4, self.screeny/4, self.screenx/2, self.screeny/2))

        # WEAPONS BUTTON
        if self.screenx/2 - 90 < mouse[0] < self.screenx/2 + 80 and self.screeny/2 - 10 < mouse[1] < self.screeny/2 + 40:
            pygame.draw.rect(self.screen, (199, 199, 199), (self.screenx/2 - 100, self.screeny/2 - 10, 180, 50))
            if buttondown:
                return self.item1
        else:
            pygame.draw.rect(self.screen, (130, 130, 130), (self.screenx/2 - 100, self.screeny/2 - 10, 180, 50))

        #UPGRADES BUTTON
        if self.screenx/2 - 90 < mouse[0] < self.screenx/2 + 80 and self.screeny/2 - 70 < mouse[1] < self.screeny/2 - 20:
            pygame.draw.rect(self.screen, (199, 199, 199), (self.screenx/2 - 100, self.screeny/2 - 70, 180, 50))
            if buttondown:
                return self.item2
        else:
            pygame.draw.rect(self.screen, (130, 130, 130), (self.screenx/2 - 100, self.screeny/2 - 70, 180, 50))

        #Labels for the buttons
        self.screen.blit(item1_text, (self.screenx/2 - 100 + 10, self.screeny/2 - 10))
        self.screen.blit(item1_price_text, (self.screenx/2 - 100 + 10, self.screeny/2 + 15))
        self.screen.blit(item2_text, (self.screenx/2 - 100 + 10, self.screeny/2 - 70))
        self.screen.blit(item2_price_text, (self.screenx/2 - 100 + 10, self.screeny/2 - 45))

        self.screen.blit(shop_text, (self.screenx/2 - 45, 150))

    def menu(self, mouse, buttondown):
        """ Creates the UI of the menu. Takes and returns nothing"""
        myfont = pygame.font.SysFont("Tahoma", 20, bold=True)
        name = myfont.render("Planet: " + self.name, 1, (17, 17, 17))
        temp = myfont.render("Temperature: " + str(self.temperature) + "°C", 1, (17, 17, 17))
        surface = myfont.render("Surface: " + self.surface, 1, (17, 17, 17))
        advancement = myfont.render("Advancement: " + str(self.advancement), 1, (17, 17, 17))

        pygame.draw.rect(self.screen, (86, 86, 86), (self.screenx/4, self.screeny/4, self.screenx/2, self.screeny/2))
        
        pygame.draw.rect(self.screen, (45, 45, 45), (self.screenx/4 + 10, self.screeny/4 + 10, 120, 120 + 160))
        self.screen.blit(self.image, (self.screenx/4 + 20, self.screeny/4 + 20 + 60))

        self.screen.blit(name, (self.screenx/4 + 20 + 120, self.screeny/4 + 20))
        self.screen.blit(temp, (self.screenx/4 + 20 + 120, self.screeny/4 + 45))
        self.screen.blit(surface, (self.screenx/4 + 20 + 120, self.screeny/4 + 70))
        self.screen.blit(advancement, (self.screenx/4 + 20 + 120, self.screeny/4 + 95))
        self.cooldown = 0 # limits amount of presses
        

        ### Checks what button the mouse is hovering over
        # Font Icons
        icon_font = pygame.font.SysFont("Tahoma", 20, bold=True)
        quest = icon_font.render("QUEST", 1, (17, 17, 17))
        shop = icon_font.render("SHOP", 1, (17, 17, 17))
        recharge = icon_font.render("CHARGE", 1, (17, 17, 17))
        repair = icon_font.render("REPAIR", 1, (17, 17, 17))
        
        # top left button
        if self.screenx/2 - 50 < mouse[0] < self.screenx/2 + 50 and self.screeny/2 - 10 < mouse[1] < self.screeny/2 + 40:
            pygame.draw.rect(self.screen, (199, 199, 199), (self.screenx/2 - 50, self.screeny/2 - 10, 100, 50))
            if buttondown and self.render_menu:
                return "quest"
        else:
            pygame.draw.rect(self.screen, (130, 130, 130), (self.screenx/2 - 50, self.screeny/2 - 10, 100, 50))

        # top right button
        if self.screenx/2 + 80 < mouse[0] < self.screenx/2 + 180 and self.screeny/2 - 10 < mouse[1] < self.screeny/2 + 40:
            pygame.draw.rect(self.screen, (199, 199, 199), (self.screenx/2 + 80, self.screeny/2 - 10, 100, 50))
            if buttondown and self.render_menu:
                return "shop"
        else:
            pygame.draw.rect(self.screen, (130, 130, 130), (self.screenx/2 + 80, self.screeny/2 - 10, 100, 50))

        # bottom left button
        if self.screenx/2 - 50 < mouse[0] < self.screenx/2 + 50 and self.screeny/2 + 60 < mouse[1] < self.screeny/2 + 110:
            pygame.draw.rect(self.screen, (199, 199, 199), (self.screenx/2 - 50, self.screeny/2  + 60, 100, 50))
            if buttondown and self.render_menu:
                return "recharge"
        else:
            pygame.draw.rect(self.screen, (130, 130, 130), (self.screenx/2 - 50, self.screeny/2 + 60, 100, 50))

        # bottom right button
        if self.screenx/2 + 80 < mouse[0] < self.screenx/2 + 180 and self.screeny/2 + 60 < mouse[1] < self.screeny/2 + 110:
            pygame.draw.rect(self.screen, (199, 199, 199), (self.screenx/2 + 80, self.screeny/2  + 60, 100, 50))
            if buttondown and self.render_menu:
                return "repair"
        else:
            pygame.draw.rect(self.screen, (130, 130, 130), (self.screenx/2 + 80, self.screeny/2  + 60, 100, 50))
            
        self.screen.blit(quest, (self.screenx/2 - 50 + 10, self.screeny/2 - 10))
        self.screen.blit(shop, (self.screenx/2 + 80 + 10, self.screeny/2 - 10))
        self.screen.blit(recharge, (self.screenx/2 - 50 + 10, self.screeny/2 + 60))
        self.screen.blit(repair, (self.screenx/2 + 80 + 10, self.screeny/2 + 60))
        
        

class health_bar():
    """keeps track of, and allows the render of your health bar"""
    def __init__(self, screen):
        self.screen = screen
        self.screenPosX, self.screenPosY = screen.get_size()

        #####REPLACE THIS IN A SEPARATE FUNCTION THAT TAKES IN HEALTH CURRENT AND MAX FROM THE SHIP
        self.health_current = 200
        self.health_max = 200

    def change(self, amount):
        """Adjusts your current health by adding or subtracting more."""
        self.health_current += amount
        if self.health_current > self.health_max: #When the total health is more than the max, health is turned into the max
            self.health_current = self.health_max 
        if self.health_current < 0: #When the total health is less than 0, health stays at 0
            self.health_current = 0

    def render(self):
        health_bar.change(self, 0)
        self.barback = pygame.draw.rect(self.screen, (170, 0, 0), (10, 500, self.health_max, 15))
        self.barfront = pygame.draw.rect(self.screen, (0, 150, 0), (10, 500, self.health_current, 15))


class mods():
    """keeps track of all the owned items you have"""
    def __init__(self, screen):
        self.screen = screen
        self.screenPosX, self.screenPosY = screen.get_size()
        self.myfont = pygame.font.SysFont("Tahoma", 20, bold=True)

        self.own_blaster = True
        self.own_laser = False
        self.own_thrower = False
        self.own_energy_ball = False

        self.equip_blaster = True
        self.equip_laser = False
        self.equip_thrower = False
        self.equip_energy_ball = False

        self.current_damage_increase = 0 # only this value changes
        self.damage_increase = 1 + self.current_damage_increase # This value can only be modified by upgrading
        self.upgraded_damage_increase = 0 #upgraded value of the multiplier
        self.health_increase = 1
        self.energy_increase = 1

        self.own_shield = False
        self.own_repair = False
        self.own_minion = False

    def render_equipped(self):
        self.damage_increase = 1 + self.upgraded_damage_increase + self.current_damage_increase # Updates the damage increase

        if self.equip_blaster == True:
            current_weapon = self.myfont.render("BLASTER", 1, (255, 255, 0))
            if self.own_blaster == False:
                current_weapon = self.myfont.render("BLASTER", 1, (127, 127, 127))
        elif self.equip_thrower == True:
            current_weapon = self.myfont.render("FLAMER", 1, (109, 252, 255))
            if self.own_thrower == False:
                current_weapon = self.myfont.render("FLAMER", 1, (127, 127, 127))
        elif self.equip_energy_ball == True:
            current_weapon = self.myfont.render("E-BALL", 1, (86, 210, 255))
            if self.own_energy_ball == False:
                current_weapon = self.myfont.render("E-BALL", 1, (127, 127, 127))
        elif self.equip_laser == True:
            current_weapon = self.myfont.render("LASER", 1, (198, 102, 255))
            if self.own_laser == False:
                current_weapon = self.myfont.render("LASER", 1, (127, 127, 127))
        
        multiplier = self.myfont.render(str(round(self.damage_increase, 1)) + "x", 1, (255, 187, 0))
        pygame.draw.rect(self.screen, (90, 90, 90), (10, 425, 115, 30))
        self.screen.blit(current_weapon, (20, 425))
        self.screen.blit(multiplier, (135, 425))


class system_stats():
    """keeps track of all user system stats"""
    def __init__(self, screen):
        self.screenPosX, self.screenPosY = screen.get_size()

        self.time_played = 0
        self.planets_max = 0
        self.planets_discovered = 0

        self.enemies_killed = 0
        self.quest_eliminated = 0

        self.menu_mode = False
        self.interact = True ### IF YOU'RE IN BATTLE, DO NOT INTERACT WITH PLANETS TO REDUCE CPU USAGE


class quest_kills():
    """This class is part of the elimination quest type"""
    ##### Current quest is declared in the beginning and put active when pressing a key. Make so that quest can be renewed!!"""
    def __init__(self, screen):
        random_counter = random.randint(3, 5)
        random_reward = random.randint(0, 99)
        self.screen = screen
        self.complete = False
        self.active = False
        self.screenPosX, self.screenPosY = screen.get_size()
        self.myfont = pygame.font.SysFont("Tahoma", 20, bold=True)

        self.enemies_killed = 0
        self.enemies_requirement = random_counter
        self.reward = random_reward + random_counter * 100

    def update(self):
        if self.enemies_killed >= self.enemies_requirement:
            self.complete = True
            self.active = False
            return True
        
        self.enemies_counter = self.myfont.render("Defeat " + str(self.enemies_killed) + "/" + str(self.enemies_requirement) + " Enemies, Reward:" + str(self.reward), 1, (255, 0, 0))

    def render(self):
        quest_kills.update(self)

        self.screen.blit(self.enemies_counter, (30, self.screenPosY/10))

class quest_capture():
    """In this quest, the player has to defeat an enemy before the time runs out"""
    # THIS CODE IS SCRAPPED
    def __init__(self, screen):
        random_reward = random.randint(299, 399)
        self.screen = screen
        self.screenPosX, self.screenPosY = screen.get_size()
        self.complete = False
        self.active = False
        self.myfont = pygame.font.SysFont("Tahoma", 20, bold=True)

        self.reward = random_reward
    
    def update(self):
        if self.complete == True:
            self.active == False
            return True
        self.counter = self.myfont.render("Capture the Target! Reward:" + str(self.reward), 1, (0, 255, 0))

    def render(self):
        quest_capture.update(self)
        self.screen.blit(self.counter, (30, self.screenPosY/10 ))

class energy_bar():
    """keeps track of, and allows the render of your energy bar"""
    def __init__(self, screen):
        self.screen = screen
        self.screenPosX, self.screenPosY = screen.get_size()

        self.energy_current = 200 ### This piece of code is ignored because they already take in values from the ship
        self.energy_max = 200

    def change(self, amount):
        """Adjusts your current energy by adding or subtracting more"""
        self.energy_current += amount
        if self.energy_current > self.energy_max: #When the total energy is more than the max, health is turned into the max
            self.energy_current = self.energy_max 
        if self.energy_current < 0: #When the total energy is less than 0, energy stays at 0
            self.energy_current = 0

    def render(self):
        energy_bar.change(self, 0)
        self.barback = pygame.draw.rect(self.screen, (170, 0, 0), (10, 520, self.energy_max, 15))
        self.barfront = pygame.draw.rect(self.screen, (0, 0, 150), (10, 520, self.energy_current, 15))

class exp_bar():
    """keeps track of, and allows the render of your exp bar"""
    def __init__(self, screen):
        self.screen = screen
        self.screenPosX, self.screenPosY = screen.get_size()

        self.level = 1
        self.timer = 0

        #####REPLACE THIS IN A SEPARATE FUNCTION THAT TAKES IN HEALTH CURRENT AND MAX FROM THE SHIP
        self.exp_current = 10 ### This piece of code is ignored because they already take in values from the ship
        self.exp_max = 100

    def change(self, amount):
        """Adjusts your current exp by adding or subtracting more"""
        self.exp_current += amount
        if self.exp_current > self.exp_max: #When the total exp is more than the max, you level up
            self.exp_current = 0
            exp_bar.level_up(self) #place this inside extraction

    def level_up(self):
        title_font = pygame.font.SysFont("Tahoma", 45, bold=True)
        level_up_text = title_font.render("LEVEL UP" + str(self.level), 1, (150, 150, 150))
        self.level += 1

        if self.timer < 400:
            self.screen.blit(level_up_text, (-300 + 4 * self.timer, 30))
            self.timer += 1.4
        if self.timer > 400:
            self.timer = 0

    def render(self):
        myfont = pygame.font.SysFont("Tahoma", 15, bold=True)
        level_text = myfont.render("lvl: " + str(self.level), 1, (255, 255, 0))
        exp_bar.change(self, 0)
        self.barback = pygame.draw.rect(self.screen, (170, 0, 0), (10, 480, self.exp_max, 15))
        self.barfront = pygame.draw.rect(self.screen, (255, 244, 96), (10, 480, self.exp_current, 15))
        self.screen.blit(level_text, (120, 480))


class navigation(pygame.sprite.Sprite):
    """renders all the lines of the planets"""
    def __init__(self, screen):
        self.screen = screen
        self.screenx, self.screeny = screen.get_size()

    def render(self, x, y, planet_posX, planet_posY):#, planet_2_posX, planet_2_posY, planet_3_posX, planet_3_posY, planet_4_posX, planet_4_posY):
        pygame.draw.aaline(self.screen, (0, 255, 0), (self.screenx/2, self.screeny/2), (planet_posX + x, planet_posY + y), 3) #adds the new coordinates with the original coordinates


class money():
    """Stores and displays your current money"""
    def __init__(self,screen):
        self.screen = screen
        self.screenx, self.screeny = screen.get_size()
        self.myfont = pygame.font.SysFont("Tahoma", 20, bold=True)

        self.money_current = 1000

    def change(self, amount):
        self.money_counter = self.myfont.render("MONEY: " + str(self.money_current), 1, (255, 255, 0))
        self.money_current += amount
    
    def render(self):
        money.change(self, 0)
        self.screen.blit(self.money_counter, (20, self.screeny - self.screeny/10))


class Enemy(object):
    """Defines an enemie's attributes"""
    def __init__(self, screen, speed, posX, posY, colour, loot, level, damage, bulletvel, firerate, enemy_type):
        self.screen = screen
        self.posX = posX 
        self.posY = posY
        self.colour = colour
        self.timer = 0
        self.firerate = firerate
        self.bulletvel = bulletvel
        self.enemy_type = enemy_type

        self.level = level
        self.damage = damage # damage is only for bullet damage. damage caused by your ship hitting the enemy is a fraction of this

        self.myfont = pygame.font.SysFont("Tahoma", 10, bold=True)
        self.level_show = self.myfont.render("lvl " + str(self.level), 1, (255, 255, 255))

        self.speed = speed
        self.health_max = 25 * level
        self.health = self.health_max
        self.size = 30
        self.money_drop = random.randint(loot, loot + 50)

    def health_change(self, amount):
        self.health += amount

    def render(self, x, y):
        self.posX = int(x)
        self.posY = int(y)

        if self.enemy_type == "boss1":
            self.screen.blit(self.image, (self.posX - 800, self.posY - 600))
            pygame.draw.circle(self.screen, (85, 168, 232), (self.posX, self.posY), self.size)
        elif self.enemy_type == "boss2":
            self.screen.blit(self.image, (self.posX - 400, self.posY - 300))
            pygame.draw.circle(self.screen, (85, 168, 232), (self.posX, self.posY), self.size)
        elif self.enemy_type == "boss3":
            self.screen.blit(self.image, (self.posX - 400, self.posY - 300))
            pygame.draw.circle(self.screen, (85, 168, 232), (self.posX, self.posY), self.size)
        elif self.enemy_type == "enemy":
            self.screen.blit(self.image, (self.posX - 80, self.posY - 80))
        else:
            pygame.draw.circle(self.screen, self.colour, (self.posX, self.posY), self.size)

        if self.health < self.health_max:
            self.firerate = 1
        #pygame.draw.aaline(self.screen, self.colour, (self.posX, self.posY), (400, 300), 2) # Shows enemy path to shoot for debugging
        self.barback = pygame.draw.rect(self.screen, (170, 0, 0), (self.posX, self.posY, 50, 10))
        self.barfront = pygame.draw.rect(self.screen, (0, 90, 0), (self.posX, self.posY, self.health * 50/self.health_max, 10)) # Allows enemy health to be show in the same look
        self.screen.blit(self.level_show, (self.posX, self.posY + 10))


class explode():
    """creates an explosion sprite"""
    def __init__(self, screen):
        self.screen = screen
        self.timer = 0
        self.frame = pygame.image.load(r"explosion3.png")
        self.frame = pygame.transform.scale(self.frame, (500, 500))
    
    def render(self, screen, x, y, size = 0):#Creates an explosion when something dies
        screen.blit(self.frame, (x - 250, y - 250)) #centers image


class timer():
    def __init__(self, cooldown):
        self.max_time = cooldown
        self.current = 0

    def update(self):
        if self.current > self.max_time:
            self.current = self.max_time

def died(screen, surface):
    screen.blit(surface, (0, 0))

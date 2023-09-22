import pygame, Extraction_Classes
import math
import random
pygame.init()

screen_width = 800
screen_height = 600 #allows the referencing of display values(you can change these values later)

black = (0, 0, 0)
world_location = Extraction_Classes.world_location() #world location indications which coordinate of the world you are on

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Extraction Game")
clock = pygame.time.Clock()

system_states = Extraction_Classes.system_stats(screen)

ship = Extraction_Classes.ship(screen)
navigation = Extraction_Classes.navigation(screen)
money = Extraction_Classes.money(screen)

health = Extraction_Classes.health_bar(screen)
energy = Extraction_Classes.energy_bar(screen)
exp = Extraction_Classes.exp_bar(screen)

MODS = Extraction_Classes.mods(screen)

#TIMERS
bps_timer = Extraction_Classes.timer(200) # Cooldown clock for bullets
your_hit_time = Extraction_Classes.timer(200) # Cooldown clock for when you are getting hit (dont want to die instantly)
quest_timer = Extraction_Classes.timer(200)
combo_timer = 300

planet_1 = Extraction_Classes.planet(screen, world_location.posX + 50, world_location.posY + 50)
planet_2 = Extraction_Classes.planet(screen, world_location.posX + 700, world_location.posY + 800)
planet_3 = Extraction_Classes.planet(screen, world_location.posX + 2000, world_location.posY + 2000)


#ENABLE/DISABLE ENTITIES
planets = [planet_1, planet_2, planet_3]
for i in range(150):
    planets.append(Extraction_Classes.planet(screen, random.randint(-5000, 15000), random.randint(-15000, 15000)))

bullets = []
enemy_bullets = []

exploding = Extraction_Classes.explode(screen)

### MODIFY QUESTS HERE
quest = Extraction_Classes.quest_kills(screen)
quest_capture = Extraction_Classes.quest_capture(screen)
quest_slot = []

### Different enemy speed values make fighting enemies more believable
enemies = []
waves = 0

### Makes the bosses (improves performance)
boss1 = Extraction_Classes.Enemy(screen, 3, 1000, 1000, (255, 0, 0), 500, 25, 20, 10, 0.8, "boss1") # Testing out a possible boss
boss1.image = pygame.image.load(r"Boss1.png")
boss1.image = pygame.transform.scale(boss1.image, (1600, 1200))

boss2 = Extraction_Classes.Enemy(screen, 3, 1000, 1000, (255, 0, 0), 500, 25, 20, 10, 0.8, "boss2") # Testing out a possible boss
boss2.image = pygame.image.load(r"Boss2.png")
boss2.image = pygame.transform.scale(boss2.image, (800, 600))

boss3 = Extraction_Classes.Enemy(screen, 3, 1000, 1000, (255, 0, 0), 500, 25, 20, 10, 0.8, "boss3") # Testing out a possible boss
boss3.image = pygame.image.load(r"Boss3.png")
boss3.image = pygame.transform.scale(boss3.image, (800, 600))

boss1_defeat = False
boss2_defeat = False
boss3_defeat = False

danger2_font = pygame.font.SysFont("Tahoma", 15, bold=True)
boss1_text = danger2_font.render("Press h to spawn boss", 1, (255, 0, 0))
boss2_text = danger2_font.render("Press g to spawn boss", 1, (255, 0, 0))
boss3_text = danger2_font.render("Press f to spawn boss", 1, (255, 0, 0))

winner_font = pygame.font.SysFont("Tahoma", 40, bold=True)
winner_text1 = winner_font.render("YOU WIN THE GAME", 1, (170, 170, 0))
winner_text2 = winner_font.render("CONGRATULATIONS", 1, (170, 170, 0))

Background = Extraction_Classes.Background(r"pixelated_space.png", [0, 0])
background = pygame.Surface(screen.get_size())


#---------------------------------------------------sounds------------------------------------------------------------------------
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

laser_sound = pygame.mixer.Sound(r"sound_laser.wav")
laser2_sound = pygame.mixer.Sound(r"sound_laser2.wav")
explosion_sound = pygame.mixer.Sound(r"sound_explosion.wav")
ship_sound = pygame.mixer.Sound(r"sound_ship.wav")
hit_sound = pygame.mixer.Sound(r"sound_hit.wav")
ching_sound = pygame.mixer.Sound(r"sound_ching.wav")
electric_sound = pygame.mixer.Sound(r"sound_electric.wav")
glitch_sound = pygame.mixer.Sound(r"sound_glitch.wav")
repair_sound = pygame.mixer.Sound(r"sound_repair.wav")

pygame.mixer.music.load(r"music_ambient.wav")
pygame.mixer.music.play(-1)


def draw_world():
    global buttondown, bullets, enemy_bullets, enemies, planets
    screen.fill((black)) #erases everything before anything is updated
    screen.blit(Background.image, Background.rect)
    ### DRAW AND ACTION ENEMENTS ARE VERY RELATED TO EACH OTHER!!!

    # Obtains the keys and mouse input used for when interacting with the world
    keys = pygame.key.get_pressed()
    last_keys = keys
    mouse = pygame.mouse.get_pos()

    # Simulates the world and background moving
    if keys[pygame.K_a]:
        world_location.posX += ship.vel
        screen.blit(Background.image, (1, 0))
    if keys[pygame.K_d]:
        world_location.posX -= ship.vel
        screen.blit(Background.image, (-1, 0))
    if keys[pygame.K_w]:
        world_location.posY += ship.vel
        screen.blit(Background.image, (0, 1))
    if keys[pygame.K_s]:
        world_location.posY -= ship.vel
        screen.blit(Background.image, (0, -1))

    # Updates all player bullets
    
    for bullet in bullets:
        if keys[pygame.K_w]:
            bullet.update_pos(ship.vel, 0, 0, 0)
        elif keys[pygame.K_s]:
            bullet.update_pos(0, ship.vel, 0, 0)
        elif keys[pygame.K_a]:
            bullet.update_pos(0, 0, ship.vel, 0)
        elif keys[pygame.K_d]:
            bullet.update_pos(0, 0, 0, ship.vel)

    # Updates all enemy bullets



    ### ENEMY AI REQUIRES OUTSIDE INTERACTION SO IT IS NOT IN A CLASS
    global combo_timer
    combo_timer += 1.4

    global mytimer2
    mytimer2 += 1.4
    for enemy in enemies:
        enemy.timer += 1.4
    
        for enemy_bullet in enemy_bullets:
            
            if keys[pygame.K_w]:
                enemy_bullet.update_pos(ship.vel, 0, 0, 0)
            elif keys[pygame.K_s]:
                enemy_bullet.update_pos(0, ship.vel, 0, 0)
            elif keys[pygame.K_a]:
                enemy_bullet.update_pos(0, 0, ship.vel, 0)
            elif keys[pygame.K_d]:
                enemy_bullet.update_pos(0, 0, 0, ship.vel)
        
        if enemy.timer > 60/enemy.firerate: #divides clock speed by enemy firerate, shots per second
            enemy_bullets.append(Extraction_Classes.projectile(screen, enemy.posX, enemy.posY\
                , 5, (255, 30, 138), (400, 300), enemy.damage, -(enemy.bulletvel), "enemy"))
            enemy.timer = 0
        
        if enemy.posX > screen_width/2: # Allows enemy to travel to middle of player
            enemy.posX -= enemy.speed
        elif enemy.posX < screen_width/2:
            enemy.posX += enemy.speed
        # Movement along y direction
        if enemy.posY < screen_height/2:
            enemy.posY += enemy.speed
        elif enemy.posY > screen_height/2:
            enemy.posY -= enemy.speed

        # Updates the position of the enemy to correlate with the player
        if keys[pygame.K_a]:
            enemy.posX += ship.vel
        if keys[pygame.K_d]:
            enemy.posX -= ship.vel
        if keys[pygame.K_w]:
            enemy.posY += ship.vel
        if keys[pygame.K_s]:
            enemy.posY -= ship.vel

        # AREAS WHERE ENEMY CAN CHANGE STUFF
        global exploding

        for bullet in bullets:
            if len(bullets) > 200:
                bullets.remove(bullet) # Removes the bullet from the player if it reaches a max of 200 sprites

            if bullet.type == "player": # Checks if the bullet being hit is by the player
                if enemy.posX - enemy.size - 15 < bullet.posX < enemy.posX + enemy.size and enemy.posY - 15 < bullet.posY < enemy.posY + 30: # This is the enemy hitbox # enemy position is subtracted by enemy health/2 because circle is drawn on the corner
                    enemy.health_change(-1 * bullet.damage) # When the enemy is hit, it loses health # Bullet damage is a positive, make it negative to make the enemy lose health
                    bullets.remove(bullet) # removes the bullet that hit the enemy so it doesn't go through
                    pygame.mixer.Sound.play(hit_sound)
                    exploding.render(screen, bullet.posX, bullet.posY)

                
        for enemy_bullet in enemy_bullets:
            if enemy_bullet.type == "enemy": # Checks if the bullet being hit is by the player
                if ship.hitbox[0] < enemy_bullet.posX < ship.hitbox[0] + 50 and ship.hitbox[1] < enemy_bullet.posY < ship.hitbox[1] + 50: # This is the enemy hitbox # enemy position is subtracted by enemy health/2 because circle is drawn on the corner
                    health.change(-1 * enemy_bullet.damage) # When the enemy is hit, it loses health # Bullet damage is a positive, make it negative to make the enemy lose health
                    #print("You're hit by bullet")
                    enemy_bullets.remove(enemy_bullet) # removes the bullet so it doesn't go through
                    exploding.render(screen, enemy_bullet.posX, enemy_bullet.posY)

        

        if ship.hitbox[0] < enemy.posX < ship.hitbox[0] + 50 and ship.hitbox[1] < enemy.posY < ship.hitbox[1] + 50:### HIT BOX OF THE SHIP IS 100 BY 100 ATM!!! ### SHIP IMAGE IS ADJUSTED BY 50 TO THE LEFT AND TOP!!!
            #print("You're hit")
            health.health_current -= enemy.damage/100

        #enemy dies
        global boss1_defeat, boss2_defeat, boss3_defeat
        if enemy.health < 0:
            global boss1, boss2, boss3 #gets the boss images (increases performance)
            if enemy == boss1:
                boss1_defeat = True
                pygame.mixer.music.load(r"music_ambient.wav") #replays the ambient music
                print(boss1_defeat)
            if enemy == boss2:
                boss2_defeat = True
                pygame.mixer.music.load(r"music_ambient.wav")
                print(boss2_defeat)
            if enemy == boss3:
                boss3_defeat = True
                pygame.mixer.music.load(r"music_ambient.wav")
                print(boss3_defeat)
            enemies.remove(enemy)
            pygame.mixer.Sound.play(explosion_sound)
            system_states.enemies_killed += 1
            money.money_current += enemy.money_drop
            exp.exp_current += enemy.level * 10 # Levels up your exp
            MODS.current_damage_increase += 0.1 #increases damage multiplier for a brief moment
            combo_timer = 0

            # checks with a quest
            if quest.active:
                quest.enemies_killed += 1

    if combo_timer >= 300:
        MODS.current_damage_increase = 0 #resets the combo if no enemies are killed within 5 seconds

            
        
    ### SPRITE HIEARCHY: BACKGROUND, LARGE SPRITES, SMALL SPRITES, ENEMY/YOUR SHIP, UI

    for planet in planets:
        if planet.visited == False and planet.posX + world_location.posX - 250 < 400 < planet.posX + world_location.posX + 250 \
            and planet.posY + world_location.posY - 250 < 300 < planet.posY + world_location.posY + 250:
            planet.discovered()
        planet.render(world_location.posX, world_location.posY)

    for enemy in enemies:
        enemy.render(enemy.posX, enemy.posY)

    for bullet in bullets:
        bullet.render(screen)
        if bullet.posX > screen_width or bullet.posX < 0 or bullet.posY > screen_height or bullet.posY < 0:
            bullets.remove(bullet)
    

    ship.run(keys, mouse, last_keys)
    health.render()
    energy.render()
    exp.render()
    money.render()

    for enemy in enemies:
        for enemy_bullet in enemy_bullets:
            if enemy_bullet.posX > screen_width or enemy_bullet.posX < 0 or enemy_bullet.posY > screen_height or enemy_bullet.posY < 0:
                enemy_bullets.remove(enemy_bullet)
            enemy_bullet.render(screen, enemy.posX, enemy.posY) #updates where the enemy is so they know which angle to shoot at
    
    # Checks for when a ship is hovering over a station
    for planet in planets:
        if planet.check_hover(world_location.posX, world_location.posY, keys):
            planet.render_menu = True
            system_states.menu_mode = True #Disallows your ship to shoot bullets

        #All options nyou can interact the planet with
        global toggle_enemies
        if planet.render_menu == True:
            if planet.menu(mouse, buttondown) == "quest" and (quest.active == False or quest_capture == False):
                toggle_enemies = True #spawns enemies
                quest.active = True
                quest.enemies_requirement = quest.enemies_requirement * planet.advancement
                quest.reward = quest.reward * planet.advancement
        
            if planet.menu(mouse, buttondown) == "shop":
                planet.render_shop = True
                planet.render_menu = False
            
            if planet.menu(mouse, buttondown) == "repair":
                if money.money_current >= health.health_max and health.health_current < health.health_max:
                    health.health_current = health.health_max
                    money.money_current -= health.health_max #THE COST TO REPAIR IS THE AMOUNT OF MAX HEALTH YOU HAVE!
                    pygame.mixer.Sound.play(repair_sound)

            if planet.menu(mouse, buttondown) == "recharge":
                if money.money_current >= 250 and energy.energy_current < energy.energy_max:
                    energy.energy_current = energy.energy_max
                    money.money_current -= 250 
                    pygame.mixer.Sound.play(electric_sound)

        #opens up shop menu
        if planet.render_shop == True:
            #SHOP WEAPONS
            if planet.shop(mouse, buttondown) == "Laser" and MODS.own_laser == False:         
                if money.money_current >= planet.item1_price:
                    MODS.own_laser = True
                    money.money_current -= planet.item1_price
                    pygame.mixer.Sound.play(ching_sound)

            if planet.shop(mouse, buttondown) == "Blaster" and MODS.own_blaster == False:         
                if money.money_current >= planet.item1_price:
                    MODS.own_blaster = True
                    money.money_current -= planet.item1_awprice
                    pygame.mixer.Sound.play(ching_sound)

            if planet.shop(mouse, buttondown) == "Energy Ball" and MODS.own_energy_ball == False:         
                if money.money_current >= planet.item1_price:
                    MODS.own_energy_ball = True
                    money.money_current -= planet.item1_price
                    pygame.mixer.Sound.play(ching_sound)

            if planet.shop(mouse, buttondown) == "Flamer" and MODS.own_thrower == False:         
                if money.money_current >= planet.item1_price:
                    MODS.own_thrower = True
                    money.money_current -= planet.item1_price
                    pygame.mixer.Sound.play(ching_sound)

            #UPGRADES
            if planet.shop(mouse, buttondown) == "Health (+75)" and health.health_max < 750:
                if money.money_current >= planet.item2_price:
                    health.health_max += 75
                    money.money_current -= planet.item2_price
                    pygame.mixer.Sound.play(ching_sound)

            if planet.shop(mouse, buttondown) == "Energy (+50)":
                if money.money_current >= planet.item2_price and energy.energy_max < 400:
                    energy.energy_max += 50
                    money.money_current -= planet.item2_price
                    pygame.mixer.Sound.play(ching_sound)

            if planet.shop(mouse, buttondown) == "Damage (x0.2)" and MODS.upgraded_damage_increase < 4:
                if money.money_current >= planet.item2_price:
                    MODS.upgraded_damage_increase += 0.2
                    money.money_current -= planet.item2_price
                    print(MODS.upgraded_damage_increase)
                    pygame.mixer.Sound.play(ching_sound)

        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            planet.render_menu = False
            planet.render_shop = False
            system_states.menu_mode = False #now allows your ship to shoot
            # Place code to know what the player wants to buy

    #----------------ACTIONS----------------
    ##### MAKE SURE TO PUT TIME FACTOR INTO EQUATION (regeneration, recharges)
    ### for every frame, an action is done
    ### this includes adding ex. time, energy

    bps_timer.current += 1.4 # 100/60 = 1.4
    bps_timer.update()

    #----------------------------------WEAPONS----------------------------------
    #checks if the user wants a new weapon to use
    if keys[pygame.K_1]:
        MODS.equip_blaster = True
        MODS.equip_laser = False
        MODS.equip_thrower = False
        MODS.equip_energy_ball = False
    elif keys[pygame.K_2]:
        MODS.equip_thrower = True
        MODS.equip_blaster = False
        MODS.equip_laser = False
        MODS.equip_energy_ball = False
    elif keys[pygame.K_3]:
        MODS.equip_energy_ball = True
        MODS.equip_blaster = False
        MODS.equip_laser = False
        MODS.equip_thrower = False
    elif keys[pygame.K_4]:
        MODS.equip_laser = True
        MODS.equip_thrower = False
        MODS.equip_energy_ball = False
        MODS.equip_blaster = False

    MODS.render_equipped()

    # All weapons
    if buttondown and system_states.menu_mode == False:
        if MODS.own_blaster == True and MODS.equip_blaster == True: ### make sure to check which weapon is equipped!
            if energy.energy_current > 5 and bps_timer.current > 20: #1/3 seconds have passed
                bullets.append(Extraction_Classes.projectile(screen, 400, 300, 3, (255, 255, 0), mouse, 5 * MODS.damage_increase, 20)) # Makes bullets shoot from the middle
                pygame.mixer.Sound.play(laser2_sound)
                bps_timer.current = 0 # subtracting 100, 50, 25, shoots 1, 2, 4 a second
                energy.energy_current -= 5
    
        # FLAME THROWER
        if MODS.own_thrower == True and MODS.equip_thrower == True:
            if energy.energy_current > 0.5 and bps_timer.current > 1.4:
                bullets.append(Extraction_Classes.projectile(screen, 400, 300, 5, (109, 252, 255), mouse, 2 * MODS.damage_increase, 10))
                pygame.mixer.Sound.play(laser_sound)
                bps_timer.current = 0
                energy.energy_current -= 1
    
        # LASER BEAM
        if MODS.own_laser == True and MODS.equip_laser == True:
            if energy.energy_current > 0:
                bullets.append(Extraction_Classes.projectile(screen, 400, 300, 15, (198, 102, 255), mouse, 5 * MODS.damage_increase, 25))
                energy.energy_current -= 4

        # ENERGY BALL
        if MODS.own_energy_ball == True and MODS.equip_energy_ball == True:
            if energy.energy_current > 50 and bps_timer.current > 80:
                pygame.mixer.Sound.play(electric_sound)
                bullets.append(Extraction_Classes.projectile(screen, 400, 300, 30, (86, 210, 255), mouse, 50 * MODS.damage_increase, 6)) # Makes bullets shoot from the middle
                bps_timer.current = 0 # subtracting 100, 50, 25, shoots 1, 2, 4 a second
                energy.energy_current -= 50

                               
    #-----------------------------------------------------------------------------------

    # Displays navigation
    if keys[pygame.K_LALT] and energy.energy_current > 0:
        for planet in planets:
            if planet.posX + world_location.posX - 3500 < 400 < planet.posX + world_location.posX + 3500 \
            and planet.posY + world_location.posY - 3500 < 300 < planet.posY + world_location.posY + 3500:
                navigation.render(world_location.posX, world_location.posY, planet.posX, planet.posY)
        for enemy in enemies:
            pygame.draw.line(enemy.screen, (165, 0, 0), (enemy.posX, enemy.posY), (400, 300), 3) # Shows All the enemies
        energy.energy_current -= 0.3
    
    if keys[pygame.K_c] and health.health_current < health.health_max and energy.energy_current > 0:
        health.health_current += 10
        energy.energy_current -= 10

        # ----------------ALL ABOUT SPAWNING ENEMY TYPES--------------------
    danger_font = pygame.font.SysFont("Tahoma", 20, bold=True)
    global waves
    if toggle_enemies and waves < 4: # Replace this with an event that spawns enemies
        danger_text = danger_font.render("ENEMY REINFORCEMENTS ACTIVE", 1, (255, 0, 0))
        screen.blit(danger_text, (screen_width/4 + 50, 10))
        if enemies == []:
            for i in range(5):
                # Creates random spawn locations and speed values
                randomX = random.randint(-screen_width, screen_width * 2)
                randomY = random.randint(-screen_height, screen_height * 2)
                randomspeed = random.randint(1, 3)
                if 100 < randomX < screen_width - 100 and 100 < randomY < screen_height - 100:
                    continue

                testenemy = Extraction_Classes.Enemy(screen, randomspeed, randomX, randomY, (255, 0, 0), 50 * int(1 + exp.level/5), 1 * int(1 + exp.level/5), 5 * int(1 + exp.level/5), 6, 0.03, "enemy")
                testenemy.image = pygame.image.load(r"enemy_small.png")
                testenemy.image = pygame.transform.scale(testenemy.image, (160, 160))
                enemies.append(testenemy)
            waves += 1

    if waves == 4:
        toggle_enemies = False
        waves = 0 #resets the numer of waves


    #ALL THE BOSSES
    
    #-------Boss 1----------
    if exp.level >= 6: #prompts the user that they can spawn a boss
        screen.blit(boss1_text, (screen_width/2 + 50, 30))
    if keys[pygame.K_h] and exp.level >= 6 and boss1 not in enemies and boss2 not in enemies and boss3 not in enemies:
        boss1.__init__(screen, 2, screen_width/2, -500, (255, 0, 0), 1500, 50, 20, 10, 0.8, "boss1")
        enemies = [boss1]
        pygame.mixer.music.load(r"music_boss1.wav")
        pygame.mixer.music.play(-1)
    #------Boss 1------------
    if boss1 in enemies:
        if len(enemies) < 3:
            for i in range(3):
                randomX = random.randint(-screen_width, screen_width)
                randomY = random.randint(-screen_height, screen_height)
                randomspeed = random.randint(1, 2)
                if 100 < randomX < screen_width - 100 and 100 < randomY < screen_height - 100:
                    continue
                minion = Extraction_Classes.Enemy(screen, randomspeed, randomX, randomY, (255, 0, 0), 50 , 2 , 9 , 10, 0.03, "enemy")
                minion.image = pygame.image.load(r"enemy_small.png")
                minion.image = pygame.transform.scale(minion.image, (160, 160))
                enemies.append(minion)
    #--------Boss 2----------
    if exp.level >= 12:
        screen.blit(boss2_text, (screen_width/2 + 50, 50))
    if keys[pygame.K_g] and exp.level >= 12 and boss1 not in enemies and boss2 not in enemies and boss3 not in enemies:
        boss2.__init__(screen, 3, screen_width/2, -1500, (255, 0, 0), 2500, 80, 40, 10, 0.8, "boss2")
        enemies = [boss2]
        pygame.mixer.music.load(r"music_boss2.wav")
        pygame.mixer.music.play(-1)

    if boss2 in enemies:
        if len(enemies) < 5:
            for i in range(5):
                randomX = random.randint(-screen_width, screen_width * 2)
                randomY = random.randint(-screen_height, screen_height * 2)
                randomspeed = random.randint(1, 3)
                if 100 < randomX < screen_width - 100 and 100 < randomY < screen_height - 100:
                    continue
                minion = Extraction_Classes.Enemy(screen, randomspeed, randomX, randomY, (255, 0, 0), 50 , 5 , 9 , 10, 0.03, "enemy")
                minion.image = pygame.image.load(r"enemy_small.png")
                minion.image = pygame.transform.scale(minion.image, (160, 160))
                enemies.append(minion)
    #------Boss 3-------------
    if exp.level >= 18:
        screen.blit(boss3_text, (screen_width/2 + 50, 70))
    if keys[pygame.K_f] and exp.level >= 18 and boss1 not in enemies and boss2 not in enemies and boss3 not in enemies:
        boss3.__init__(screen, 3, screen_width/2, -1500, (255, 0, 0), 3500, 120, 50, 11, 2, "boss3")
        enemies = [boss3]
        pygame.mixer.music.load(r"music_boss3.wav")
        pygame.mixer.music.play(-1)

    if boss3 in enemies:
        if len(enemies) < 3:
            for i in range(5):
                randomX = random.randint(-screen_width, screen_width * 2)
                randomY = random.randint(-screen_height, screen_height * 2)
                randomspeed = random.randint(4, 5)
                if 100 < randomX < screen_width - 100 and 100 < randomY < screen_height - 100:
                    continue
                minion = Extraction_Classes.Enemy(screen, randomspeed, randomX, randomY, (255, 0, 0), 50 , 2 , 9 , 3, 0.03, "enemy")
                minion.image = pygame.image.load(r"enemy_small.png")
                minion.image = pygame.transform.scale(minion.image, (160, 160))
                enemies.append(minion)
    
    # separate from activator
    if quest.active:
        quest.render()
        if quest.complete == True: # Checks to see if the quest is complete after rendering only
            money.money_current += quest.reward
            quest.__init__(screen) # Resets the values of the quest so a new one can be made

    global mytimer, mytimer3 ### CHANGE MY TIMER LATER

    if keys[pygame.K_v] and mytimer < 10:
        mytimer = 0
        energy.energy_max += 1
    else:
        mytimer += 1

    # Recharges the energy
    if energy.energy_current == 0 and mytimer < 60:
        mytimer += 1.4
    else:
        energy.energy_current += 0.3 # Energy only increases once all actions are done 
        mytimer = 0
    # Only does this code once the cool down initiates

    #----------------------------GAME DEATH SCREEN------------------------
    global lives, death_screen_timer
    death_font = pygame.font.SysFont("Tahoma", 30, bold=True)
    death_text = death_font.render("You're Dead", 1, (170, 0, 0))
    lives_text = death_font.render("Reincarnations Left: " + str(lives), 1, (170, 0, 0))

    if health.health_current == 0: # Checks if your character is dead or not before running everything else
        #Extraction_Classes.died(screen, background)
        screen.blit(background, (0, 0))
        death_screen_timer += 1.4
        print("TIME:", death_screen_timer)
        pygame.mixer.music.pause() #mutes all music

        if death_screen_timer > 100:
            pygame.mixer.pause()
        else:
            pygame.mixer.Sound.play(explosion_sound)
            pygame.mixer.Sound.play(glitch_sound)

        if lives == 0:
            lives_text = death_font.render("     GAME     OVER", 1, (170, 0, 0))

        if death_screen_timer > 120:
            screen.blit(death_text, (screen_width/2 - 85, screen_height/2 - 200))
        if death_screen_timer > 220:
            screen.blit(lives_text, (screen_width/4 + 40, screen_height/2 + 50))

        
        #RESPAWNING
        if death_screen_timer > 350:
            pygame.mixer.music.unpause() #unmutes all music
            pygame.mixer.unpause()
            lives -= 1
            death_screen_timer = 0

            # Resets the whole entire screen
            health.health_current = health.health_max
            enemies = []
    
    global end_counter
    if boss1_defeat and boss2_defeat and boss3_defeat:
        screen.blit(background, (0, 0))
        screen.blit(winner_text1, (screen_width/4, screen_height/2 - 200))
        screen.blit(winner_text2, (screen_width/4, screen_height/2 - 250))

##### USED FOR TESTING ENEMIES
toggle_enemies = False

mytimer = 0
mytimer2 = 0
mytimer3 = 0
lives = 5

death_screen_timer = 0

crashed = False
buttondown = False
while not crashed:
    clock.tick(60) #sets frames per second
    if lives < 0:
        crashed = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttondown = True
        if event.type == pygame.MOUSEBUTTONUP:
            buttondown = False
        
    draw_world()
    
    #----------------------REFRESH-------------------------
    pygame.display.update() #refreshes display and updates the display
    pygame.display.flip()


pygame.quit()
quit() #quits program and python

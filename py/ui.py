from settings import *
from stats import Gold, Upgrades

class UI():
    def __init__(self):
        self.window = pygame.display.get_surface()

        self.state = 'start_menu'

        self.start_menu_options = ['Start', 'Save', 'Load', 'Quit', 'Upgrades']
        self.character_list = ['Archer', 'Knight', 'Mage']
        self.btns = []

        self.gold = Gold()
        self.upgrades = Upgrades()

        ## Labels ig ## TODO try find way to improve :)
        self.labels = {}

        self.scroll_offset = 0
        self.scroll_distance = 15
        
    ## Helpers ##
    def input(self):
        self.mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_just_pressed()

        for button in self.btns:
            if button.collidepoint(self.mouse_pos):
                    index = self.btns.index(button)

                    if mouse[0]:
                        self.click(index)

    def click(self, index):
        ## Checks if return button is clicked ##
        if self.state != 'start_menu' and self.btns[index] == self.btns[-1]:
            self.state = 'start_menu'
            self.scroll_offset = 0
            self.btns.clear()
            return

        if self.state == 'start_menu':
            match index:
                case 0: self.state = 'start'
                case 1: self.state = 'save'
                case 2: self.state = 'load'
                case 3: self.state = 'quit'
                case 4: self.state = 'upgrades'
            self.btns.clear()

        elif self.state == 'start':
            match index:
                case 0:
                    self.state = 'start_game'
                    self.selected_character = 'archer'
                case 1:
                    self.state = 'start_game'
                    self.selected_character = 'knight'
                case 2:
                    self.state = 'start_game'
                    self.selected_character = 'mage'
            self.btns.clear()

        elif self.state == 'upgrades':
            if index < len(self.upgrade_keys):  # Ensure the index is valid
                self.upgrades.buyUpgrade(self.upgrade_keys[index])  # Pass the key to buyUpgrade
                print(f"Upgrade Purchased: {self.upgrade_keys[index]}")
                
        elif self.state == 'save':
            pass

    def hover(self, index, options, font):
        if self.btns[index].collidepoint(self.mouse_pos):
            hover_surf = font.render(options[index], True, COLOURS['hoverred'])
            self.window.blit(hover_surf, self.btns[index])

    def get_font(self, size):
        return pygame.font.Font(join('data', 'Fonts', 'Cormorant', 'Cormorant-VariableFont_wght.ttf'), size)
    
    def title(self, title):
        title_font = self.get_font(100)
        title_surf = title_font.render(title, True, COLOURS['white'])
        title_text = title_surf.get_frect(center = (WINDOW_WIDTH / 2, 75))
        self.window.blit(title_surf, title_text)

    def background(self):
        bg_rect = pygame.FRect(0,0, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.window, COLOURS['lightred'], bg_rect)
        pygame.draw.rect(self.window, COLOURS['gray'], bg_rect, 5)

    def displayButton(self, text, surf):
        self.btns.append(text)
        self.window.blit(surf, text)

    def renderMenu(self, font, options, return_btn = False):
        if return_btn:
            self.returnButton(font, options)

        for i in range(len(self.btns)):
            surf = font.render(options[i], True, COLOURS['black'])
            self.window.blit(surf, self.btns[i])
            self.hover(i, options, font)

    def returnButton(self, font, options):
        return_surf = font.render('Main Menu', True, COLOURS['black'])
        return_text = return_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
        if return_text not in self.btns:
            self.btns.append(return_text)
        options.append('Main Menu')
    
    def upgradeScroll(self):
        # mouse_scroll = pygame.mouse.get_rel()
        # if mouse_scroll[1] > 0:
        #     self.scroll_offset -= 10
        # elif mouse_scroll[1] < 0:
        #     self.scroll_offset += 10
        
        ## Scroll Bar ##
        pass

    ## Menus ##
    def start_menu(self):        
        self.title('Vampire UnSurvivors')        

        options_font = self.get_font(50)
        if len(self.btns) == 0:
            ## Options Menu ##
            options_rect = pygame.FRect(0, WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            for row in range(4):
                x = options_rect.left + 75
                y = 50 + options_rect.top + (options_rect.height / 4) * row

                ## text ## 
                option_surf = options_font.render(self.start_menu_options[row], True, COLOURS['black'])
                option_text = option_surf.get_frect(center = (x,y))

                self.btns.append(option_text)
            
            ## Upgrades Menu Button ##
            upgrade_surf = options_font.render('Upgrades', True, COLOURS['black'])
            upgrade_text = upgrade_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            self.btns.append(upgrade_text)

        self.renderMenu(options_font, self.start_menu_options)
        
    def character_menu(self):
        self.title('Select Your Character')

        character_font = self.get_font(50)
        character_rect = pygame.FRect(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        if len(self.btns) == 0:
            for i in range (3):
                x = character_rect.left + (character_rect.width / 2) * i
                y = WINDOW_HEIGHT / 2

                character_surf = character_font.render(self.character_list[i], True, COLOURS['black'])
                character_text = character_surf.get_frect(center = (x,y))

                self.btns.append(character_text)
        
        self.renderMenu(character_font, self.character_list, True)

    def upgrade_menu(self): ## TODO add buttons
        self.title('Upgrades')
        
        ## Gold ##
        gold_font = self.get_font(40)

        gold_bg = pygame.FRect(WINDOW_WIDTH - 375, 35, WINDOW_WIDTH / 4, (WINDOW_HEIGHT / 4) - 75)
        transparent_surface = pygame.Surface((gold_bg.width, gold_bg.height), pygame.SRCALPHA)
        transparent_surface.fill(COLOURS['transparent'])
        self.window.blit(transparent_surface, (gold_bg.x, gold_bg.y))
        pygame.draw.rect(self.window, COLOURS['gold'], gold_bg, 5, 5)

        gold_surface = gold_font.render(str(self.gold.balance), True, COLOURS['white'])
        gold_text = gold_surface.get_frect(center = (gold_bg.centerx,gold_bg.centery))
        self.window.blit(gold_surface, gold_text)

        ## Buttons ##
        self.upgradeScroll()

        upgrade_rect = pygame.FRect(WINDOW_WIDTH / 4, 200, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 350)

        ## Upgrade Bg ##
        upg_border_rect = upgrade_rect.inflate(250, 75)
        transparent_surface = pygame.Surface((upg_border_rect.width, upg_border_rect.height), pygame.SRCALPHA)
        transparent_surface.fill(COLOURS['transparent'])
        self.window.blit(transparent_surface, (upg_border_rect.x, upg_border_rect.y))
        pygame.draw.rect(self.window, COLOURS['gold'], upg_border_rect, 5, 5)

        self.btns.clear()
        self.labels.clear()
        cols = 3
        self.upgrade_keys = []

        if len(self.btns) == 0:
            for i in range(len(self.upgrades.upgrade_costs)):
                row = i // cols
                col = i % cols
                x = upgrade_rect.left + (upgrade_rect.width / 2) * col
                y = 100 + upgrade_rect.top + 160 * row + self.scroll_offset
              
                ## Boundaries ##
                if row == 0:
                    y = min(y, upgrade_rect.bottom - 50)
                    if y >= upgrade_rect.bottom - 50: self.scroll_offset -= self.scroll_distance
                elif row == (len(self.upgrades.upgrade_costs) - 1) // cols:
                    y = max(y, upgrade_rect.top + 50)
                    if y <= upgrade_rect.top + 50: self.scroll_offset += self.scroll_distance

                if upgrade_rect.top <= y < upgrade_rect.bottom:
                    upgrade_key = self.upgrades.getUpgradeCosts()[i]
                    self.upgrade_keys.append(upgrade_key)

                    ## Purchase Button ##
                    upgrade_surf = gold_font.render('Purchase', True, COLOURS['black'])
                    upgrade_text = upgrade_surf.get_frect(midtop = (x,y))

                    ## Label ##
                    label_surf = gold_font.render(
                        f'{upgrade_key} - {self.upgrades.upgrade_costs[upgrade_key]}', True, COLOURS['black']
                    )
                    label_text = label_surf.get_frect(midbottom = upgrade_text.midtop)

                    self.btns.append(upgrade_text)
                    self.labels[label_surf] = label_text

        self.renderMenu(gold_font, ['Purchase' for i in range(len(self.btns))], True)
        for surf, text in self.labels.items():
            self.window.blit(surf, text)

    def save_menu(self):
        self.title('Save')
        
        save_font = self.get_font(60)
        save_rect = pygame.FRect(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        save_arr = [f'Save Slot {i + 1}' for i in range(3)] 

        if len(self.btns) == 0:
            for i in range(3):
                x = save_rect.left + (save_rect.width / 2) * i
                y = WINDOW_HEIGHT / 2

                save_surf = save_font.render(f'Save Slot: {i + 1}', True, COLOURS['black'])
                save_text = save_surf.get_frect(center = (x,y))

                self.btns.append(save_text)

        self.renderMenu(save_font, save_arr, True)

    ## Rendering ##
    def update(self):
        self.input()
        
    def draw(self):
        self.background()

        match self.state:
            case 'start_menu': self.start_menu()

            case 'start': self.character_menu()

            case 'upgrades': self.upgrade_menu()

            case 'save': self.save_menu()

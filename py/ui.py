from settings import *

class UI():
    def __init__(self):
        self.window = pygame.display.get_surface()

        self.state = 'start_menu'

        self.start_menu_options = ['Start', 'Save', 'Load', 'Quit']
        self.character_list = ['Archer', 'Knight', 'Mage']
        self.btns = []

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
        if self.state == 'start_menu':
            match index:
                case 0: self.state = 'start'
                case 1: self.state = 'save'
                case 2: self.state = 'load'
                case 3: self.state = 'quit'
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

    def hover(self, index, options):
        font = self.get_font(50)

        if self.btns[index].collidepoint(self.mouse_pos):
            hover_surf = font.render(options[index], True, COLOURS['hoverred'])
            self.window.blit(hover_surf, self.btns[index])

    def get_font(self, size):
        return pygame.font.Font(join('data', 'Fonts', 'Cormorant', 'Cormorant-VariableFont_wght.ttf'), size)
    
    def background(self):
        bg_rect = pygame.FRect(0,0, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.window, COLOURS['lightred'], bg_rect)
        pygame.draw.rect(self.window, COLOURS['gray'], bg_rect, 5)

    def display(self, text, surf):
        self.btns.append(text)
        self.window.blit(surf, text)

    ## Menus ##
    def start_menu(self):

        ## Title ##
        title_font = self.get_font(100)
        title_surf = title_font.render('Vampire UnSurvivors', True, COLOURS['white'])
        title_text = title_surf.get_frect(center = (WINDOW_WIDTH / 2, 75))
        self.window.blit(title_surf, title_text)


        ## Options Menu ##
        options_font = self.get_font(50)
        options_rect = pygame.FRect(0, WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        for row in range(4):
            x = options_rect.left + 75
            y = 50 + options_rect.top + (options_rect.height / 4) * row

            ## text ## 
            option_surf = options_font.render(self.start_menu_options[row], True, COLOURS['black'])
            option_text = option_surf.get_frect(center = (x,y))

            self.display(option_text,option_surf)

            self.hover(row, self.start_menu_options)

    

    def character_menu(self):
        character_font = self.get_font(50)
        character_rect = pygame.FRect(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

        for row in range (3):
            x = character_rect.left + (character_rect.width / 2) * row
            y = WINDOW_HEIGHT / 2

            character_surf = character_font.render(self.character_list[row], True, COLOURS['black'])
            character_text = character_surf.get_frect(center = (x,y))

            self.display(character_text,character_surf)

            self.hover(row, self.character_list)

    def update(self):
        self.input()
        
    def draw(self):
        self.background()

        match self.state:
            case 'start_menu': self.start_menu()

            case 'start': self.character_menu()

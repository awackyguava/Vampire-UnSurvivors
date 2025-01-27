from settings import *

class UI():
    def __init__(self):
        self.window = pygame.display.get_surface()

        self.state = 'start_menu'

        self.start_menu_options = ['Start', 'Save', 'Load', 'Quit']
        self.option_btns = []

    def input(self):
        self.mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_just_pressed()

        if mouse[0]:
            for button in self.option_btns:
                if button.collidepoint(self.mouse_pos):
                        if self.option_btns.index(button) == 0:
                            self.state = 'start'
                        elif self.option_btns.index(button) == 1:
                            self.state = 'save'
                        elif self.option_btns.index(button) == 2:
                            self.state = 'load'
                        elif self.option_btns.index(button) == 3:
                            self.state = 'quit'
        
    def get_font(self, size):
        return pygame.font.Font(join('data', 'Fonts', 'Cormorant', 'Cormorant-VariableFont_wght.ttf'), size)

    def start_menu(self):
        ## bg ##
        bg_rect = pygame.FRect(0,0, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.window, COLOURS['lightred'], bg_rect)
        pygame.draw.rect(self.window, COLOURS['gray'], bg_rect, 5)

        ## Title ##
        title_font = self.get_font(100)
        title_surf = title_font.render('Vampire UnSurvivors', True, COLOURS['white'])
        title_text = title_surf.get_frect(center = (WINDOW_WIDTH / 2, 75))
        self.window.blit(title_surf, title_text)


        ## Options Menu ##
        options_font = self.get_font(50)
        options_rect = pygame.FRect(0, WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        x = options_rect.left + 75
        for row in range(4):
            y = 50 + options_rect.top + (options_rect.height / 4) * row

            ## text ## 
            option_surf = options_font.render(self.start_menu_options[row], True, COLOURS['black'])
            option_text = option_surf.get_frect(center = (x,y))

            self.option_btns.append(option_text)

            if option_text.collidepoint(self.mouse_pos):
                option_surf = options_font.render(self.start_menu_options[row], True, COLOURS['hoverred'])

            self.window.blit(option_surf, option_text)

    def update(self):
        self.input()
        
    def draw(self):
        if self.state == 'start_menu': self.start_menu()
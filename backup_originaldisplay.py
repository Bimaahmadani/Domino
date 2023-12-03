#Window configuration
pygame.init()
WIDTH, HEIGHT = 1400, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('TheMino: Ordinary Domino Game')

ICON = pygame.image.load("assets/DominoIcon.png").convert_alpha()
pygame.display.set_icon(ICON)

PLAYERS_NUM = 2
last_players_num = PLAYERS_NUM

BACKGROUND = pygame.image.load(f"assets/Table({PLAYERS_NUM}).png").convert_alpha()
PLAYER__ = pygame.image.load(f"assets/Dominos (Interface)/jugador#.png").convert_alpha()

SLEEP_TIME = .16
PLAYER__pos = (26, 606)
PLAYER_NUM_pos = (240, 599)
can_play_pos = (310, 614)
turn_pos = (625, 6)

WINDOW.blit(BACKGROUND, (0, 0))
WINDOW.blit(PLAYER__, PLAYER__pos)

OBJECTS = [] # list yang berisi semua objek yang ada di game
LAYERS = {0: Layer()} # dictionary yang berisi semua layer yang ada di game

PLAYERS = [Player(num) for num in range(PLAYERS_NUM)] # list yang berisi semua pemain yang ada di game

#Player
player = PLAYERS[0] # pemain yang sedang bermain

#computer
#PLAYERS[0].change_auto()
PLAYERS[1].change_auto() # mengubah pemain ke mode komputer
#PLAYERS[2].change_auto()
#PLAYERS[3].change_auto()

FPS = 60 # frame per second


text_color = (59, 32, 39) # warna teks
bck_color = (255, 194, 161) # warna background

# X = WIDTH # lebar window
# Y = HEIGHT # tinggi window

font = pygame.font.Font('assets/alagard.ttf', 32)

GAME_FINISHED_SOUND =  pygame.mixer.Sound('assets/Audio/gameFinished.wav') # suara yang akan diputar ketika game selesai
EXTRA_DOMINO_SOUND =  pygame.mixer.Sound('assets/Audio/newDomino.wav') # suara yang akan diputar ketika pemain mengambil kartu tambahan
BUTTOM_SOUND =  pygame.mixer.Sound('assets/Audio/Buttom.wav') # suara yang akan diputar ketika pemain menekan tombol
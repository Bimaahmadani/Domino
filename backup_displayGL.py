def display_init():
    # buat global variabel
    global PLAYERS, ICON, WINDOW, WIDTH, HEIGHT, BACKGROUND, PLAYER__, PLAYER__pos, PLAYER_NUM_pos, can_play_pos, turn_pos, player, SLEEP_TIME, PLAYERS_NUM, last_players_num, FPS, text_color, bck_color, font, GAME_FINISHED_SOUND, EXTRA_DOMINO_SOUND, BUTTOM_SOUND, OBJECTS, LAYERS
    material_ambient = (0.1, 0.1, 0.1, 1.0)
    material_diffuse = (0.7, 0.7, 0.7, 1.0)
    material_specular = (0.5, 0.5, 0.5, 1)
    pygame.init()
    WIDTH, HEIGHT = 1400, 800
    screen_size = (WIDTH, HEIGHT)
    WINDOW = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL)
    # WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    

    pygame.display.set_caption('TheMino: Ordinary Domino Game')
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_BLEND)

    # Set material properties
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)

    gluPerspective(70, (screen_size[0] / screen_size[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, 2.0)
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, -1, 0))

    glEnable(GL_DEPTH_TEST)

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

    font = pygame.font.Font('assets/alagard.ttf', 32) # jenis font

    GAME_FINISHED_SOUND =  pygame.mixer.Sound('assets/Audio/gameFinished.wav') # suara yang akan diputar ketika game selesai
    EXTRA_DOMINO_SOUND =  pygame.mixer.Sound('assets/Audio/newDomino.wav') # suara yang akan diputar ketika pemain mengambil kartu tambahan
    BUTTOM_SOUND =  pygame.mixer.Sound('assets/Audio/Buttom.wav') # suara yang akan diputar ketika pemain menekan tombol
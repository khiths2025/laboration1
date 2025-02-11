import sys, pygame, enum, collections, random, dataclasses

X_RESOLUTION = 1600
Y_RESOLUTION = 900
SCALING_FACTOR = 3
BORDER_SIZE = 8
BACKGROUND_COLOR = (8, 59, 23)
#Ugly indent but it needs to look this way to render properly
RULES_TEXT = """Press h to hit during your round.
Press s to stand and pass to the dealer.
Press n for a new round when the current one is over.
Good luck!"""
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 32
RULES_TEXT_COORD = (BORDER_SIZE * 4, BORDER_SIZE * 4)
STATE_TEXT_COORD = ((X_RESOLUTION // 4) * 3, Y_RESOLUTION // 6)
WRAP_LENGTH = 700

class GameState(enum.Enum):
    PLAYER_ROUND = enum.auto()
    DEALER_ROUND = enum.auto()
    PLAYER_WIN = enum.auto()
    DEALER_WIN = enum.auto()

def pretty_print_gamestate(gamestate: GameState):
    if gamestate == GameState.PLAYER_ROUND:
        return "Player's round"
    elif gamestate == GameState.DEALER_ROUND:
        return "Dealer's round"
    elif gamestate == GameState.PLAYER_WIN:
        return "You won! New round?"
    elif gamestate == GameState.DEALER_WIN:
        return "You lost! New round?"

@dataclasses.dataclass
class Card:
    id: int
    value: int

def get_img_path_from_card(card: Card) -> str:
    return f'assets/card_{card.id}.png'

def draw_card_to_hand(deck: list[Card], hand: list[Card]) -> None:
    hand.append(deck.pop())

def load_and_upscale_img(path: str) -> pygame.Surface:
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (img.get_width() * SCALING_FACTOR, img.get_height() * SCALING_FACTOR))

def calc_hand_value(hand: list[Card]) -> int:
    high_ace_value, low_ace_value = 0, 0
    for card in hand:
        high_ace_value += card.value
        low_ace_value += card.value
        #ace can be 1 and 11
        if card.value == 1:
            high_ace_value += 10
    if high_ace_value > 21:
        return low_ace_value
    else:
        return high_ace_value

def draw_hand_to_screen(screen: pygame.Surface, hand: list[Card], y_coordinate: int) -> None:
    for i, card in enumerate(hand):
        card_img = load_and_upscale_img(get_img_path_from_card(card))
        x_coordinate = (X_RESOLUTION // 2) - (card_img.get_width() // 2)
        if i % 2 == 1:
            x_coordinate -= ((i + 1) // 2) * card_img.get_width()
        else:
            x_coordinate += (i // 2)  * card_img.get_width()        
        screen.blit(card_img, (x_coordinate, y_coordinate))

class Blackjack:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('BLACKJACK')
        self.screen = pygame.display.set_mode((X_RESOLUTION, Y_RESOLUTION))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('assets/Minecraft.ttf', FONT_SIZE)
        self.font.align = pygame.FONT_LEFT
        self.new_round()
 
    def new_round(self):
        random.seed()
        self.gamestate = GameState.PLAYER_ROUND
        self.deck = [
            Card(1, 1),
            Card(2, 2), 
            Card(3, 3), 
            Card(4, 4), 
            Card(5, 5), 
            Card(6, 6),
            Card(7, 7),
            Card(8, 8),
            Card(9, 9),
            Card(10, 10),
            Card(11, 10),
            Card(12, 10),
            Card(13, 10),
            Card(14, 1),
            Card(15, 2), 
            Card(16, 3), 
            Card(17, 4), 
            Card(18, 5), 
            Card(19, 6),
            Card(20, 7),
            Card(21, 8),
            Card(22, 9),
            Card(23, 10),
            Card(24, 10),
            Card(25, 10),
            Card(26, 10),
            Card(27, 1),
            Card(28, 2), 
            Card(29, 3), 
            Card(30, 4), 
            Card(31, 5), 
            Card(32, 6),
            Card(33, 7),
            Card(34, 8),
            Card(35, 9),
            Card(36, 10),
            Card(37, 10),
            Card(38, 10),
            Card(39, 10),
            Card(40, 1),
            Card(41, 2), 
            Card(42, 3), 
            Card(43, 4), 
            Card(44, 5), 
            Card(45, 6),
            Card(46, 7),
            Card(47, 8),
            Card(48, 9),
            Card(49, 10),
            Card(50, 10),
            Card(51, 10),
            Card(52, 10),
            ]
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []   

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h and self.gamestate == GameState.PLAYER_ROUND:
                        draw_card_to_hand(self.deck, self.player_hand)
                        if calc_hand_value(self.player_hand) > 21:
                            self.gamestate = GameState.DEALER_WIN
                    elif event.key == pygame.K_s and self.gamestate == GameState.PLAYER_ROUND:
                        self.gamestate = GameState.DEALER_ROUND
                    elif event.key == pygame.K_n and (self.gamestate == GameState.DEALER_WIN or self.gamestate == GameState.PLAYER_WIN):
                        self.new_round()
                if self.gamestate == GameState.DEALER_ROUND:
                    while calc_hand_value(self.dealer_hand) < 17:
                        draw_card_to_hand(self.deck, self.dealer_hand)
                    if (calc_hand_value(self.player_hand) > calc_hand_value(self.dealer_hand)) or calc_hand_value(self.dealer_hand) > 21:
                        self.gamestate = GameState.PLAYER_WIN
                    else:
                        self.gamestate = GameState.DEALER_WIN

            self.screen.fill(BACKGROUND_COLOR)
            deck_img = load_and_upscale_img('assets/deck.png')
            self.screen.blit(deck_img, ((X_RESOLUTION // 2) - (deck_img.get_width() // 2), BORDER_SIZE))
            self.screen.blit(self.font.render(RULES_TEXT, False, TEXT_COLOR, wraplength=WRAP_LENGTH), RULES_TEXT_COORD)
            self.screen.blit(self.font.render(pretty_print_gamestate(self.gamestate), False, TEXT_COLOR), STATE_TEXT_COORD)
            draw_hand_to_screen(self.screen, self.dealer_hand, Y_RESOLUTION // 3)
            draw_hand_to_screen(self.screen, self.player_hand, (Y_RESOLUTION // 3) * 2)      
            pygame.display.update()
            self.clock.tick(60)
            
if __name__ == "__main__":
    Blackjack().run()

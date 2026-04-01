import pygame
pygame.init()
pygame.mixer.init()
width=1536
height=1536
dim=height/12
offset_x=(width-dim*8)/2
offset_y=(height-dim*8)/2
move_sound = pygame.mixer.Sound("Asset/Move.mp3")
check_sound = pygame.mixer.Sound("Asset/GenericNotify.mp3")
hugeFont = pygame.font.Font('freesansbold.ttf', 72)
font = pygame.font.Font('freesansbold.ttf', 48)
medFont = pygame.font.Font('freesansbold.ttf', 42)
whiteTurn = font.render("White's Turn",True,(252,246,227))
blackTurn = font.render("Black's Turn",True,(0,0,0))
ch = medFont.render("Check!",True,(247,35,35))
whiteWon = hugeFont.render("Checkmate White won!",True,(0,0,0))
blackWon = hugeFont.render("Checkmate Black won!",True,(0,0,0))
rst = font.render("Press R to restart",True,(0,0,0))
box = whiteTurn.get_rect()
box.center=(width/2,offset_y/2)
chBox = ch.get_rect()
chBox.center=(width/2,offset_y/2*1.5)
endBox = whiteWon.get_rect()
endBox.center=(width/2,height/2)
rstBox = rst.get_rect()
rstBox.center=(width/2,offset_y)
boardFont = pygame.font.SysFont('Arial', 32,bold=True)
columns=['A','B','C','D','E','F','G','H']
rows=['8','7','6','5','4','3','2','1']
CLOCK_TIME = 600
white_time = CLOCK_TIME
black_time = CLOCK_TIME
last_tick = pygame.time.get_ticks()
time_out = None

class square(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.color = color
        self.surf=pygame.Surface((dim,dim))
        if self.color=="black":
            self.surf.fill((94,94,112))
        else:
            self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)

    def updateColor(self):
        self.surf.fill((245,88,99))

    def resetColor(self):
        if self.color=="black":
            self.surf.fill((94,94,112))
        else:
            self.surf.fill((255,255,255))


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, piece_type, image_path, col, row, offset_x=(width-dim*8)/2, offset_y=(height-dim*8)/2):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.color = color
        self.piece_type = piece_type
        self.moved=False
        self.col = col
        self.row = row
        self.dim = dim
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.image_path = image_path
        self.image = pygame.transform.scale(self.image, (int(dim), int(dim)))
        self.updatePosition()

    def updatePosition(self):
        x_pos=self.offset_x+(self.col*self.dim)
        y_pos=self.offset_y+(self.row*self.dim)
        self.rect.center=(x_pos+self.dim//2,y_pos+self.dim//2)

tab=[]
for row in range(8):
    cur=[]
    for col in range(8):
        x_pos=offset_x+col*dim
        y_pos=offset_y+row*dim
        if(row+col)%2==0:
            color="white"
        else:
            color="black"
        patrat=square(color,x_pos,y_pos)
        cur.append(patrat)
    tab.append(cur)

pionNegru=pygame.image.load("Asset/black-pawn.png")
regeNegru=pygame.image.load("Asset/black-king.png")
reginaNeagra=pygame.image.load("Asset/black-queen.png")
nebunNegru=pygame.image.load("Asset/black-bishop.png")
calNegru=pygame.image.load("Asset/black-knight.png")
turaNeagra=pygame.image.load("Asset/black-rook.png")
pionAlb=pygame.image.load("Asset/white-pawn.png")
regeAlb=pygame.image.load("Asset/white-king.png")
reginaAlba=pygame.image.load("Asset/white-queen.png")
nebunAlb=pygame.image.load("Asset/white-bishop.png")
calAlb=pygame.image.load("Asset/white-knight.png")
turaAlba=pygame.image.load("Asset/white-rook.png")

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Sah")

timer = pygame.time.Clock()
fps = 60

allPiece=pygame.sprite.Group()
def setPieces():
    for col in range(8):
        pionN=Piece("black","pion","Asset/black-pawn.png",col,1,offset_x,offset_y)
        pionA=Piece("white","pion","Asset/white-pawn.png",col,6,offset_x,offset_y)
        allPiece.add(pionN)
        allPiece.add(pionA)
    for col in range(8):
        if col==0 or col==7:
            turaN=Piece("black","tura","Asset/black-rook.png",col,0,offset_x,offset_y)
            turaA=Piece("white","tura","Asset/white-rook.png",col,7,offset_x,offset_y)
            allPiece.add(turaN)
            allPiece.add(turaA)
        elif col==1 or col==6:
            calN=Piece("black","cal","Asset/black-knight.png",col,0,offset_x,offset_y)
            calA=Piece("white","cal","Asset/white-knight.png",col,7,offset_x,offset_y)
            allPiece.add(calN)
            allPiece.add(calA)
        elif col==2 or col==5:
            nebunN=Piece("black","nebun","Asset/black-bishop.png",col,0,offset_x,offset_y)
            nebunA=Piece("white","nebun","Asset/white-bishop.png",col,7,offset_x,offset_y)
            allPiece.add(nebunN)
            allPiece.add(nebunA)
        elif col==4:
            regeN=Piece("black","rege","Asset/black-king.png",col,0,offset_x,offset_y)
            regeA=Piece("white","rege","Asset/white-king.png",col,7,offset_x,offset_y)
            allPiece.add(regeN)
            allPiece.add(regeA)
        elif col==3:
            reginaN=Piece("black","regina","Asset/black-queen.png",col,0,offset_x,offset_y)
            reginaA=Piece("white","regina","Asset/white-queen.png",col,7,offset_x,offset_y)
            allPiece.add(reginaN)
            allPiece.add(reginaA)


def draw_inner_glow(screen, color, glow_thickness=40):
    glow_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    screen_w, screen_h = screen.get_size()
    r, g, b = color
    for i in range(glow_thickness):
        alpha = int(255 - (255 * (i / glow_thickness)))
        inset_rect = pygame.Rect(
            i,
            i,
            screen_w - (i * 2),
            screen_h - (i * 2)
        )
        pygame.draw.rect(glow_surface, (r, g, b, alpha), inset_rect, width=1)
    screen.blit(glow_surface, (0, 0))

def check(color):
    for p in allPiece:
        if p.piece_type=="rege" and p.color==color:
            Reg=p
            break
    for p in allPiece:
        if p!=Reg and p.color!=color:
            if checkMove(p,Reg.col,Reg.row,simulate=True):
                return True

def squareAttacked(col, row, byColor):
    for p in allPiece:
        if p.color == byColor:
            if checkMove(p, col, row, simulate=True):
                return True
    return False

def checkMate(color):
    Mate = True
    for p in list(allPiece):
        if p.color == color:
            for i in range(8):
                for j in range(8):
                    if checkMove(p, i, j, simulate=True):
                        oldX, oldY = p.col, p.row
                        victim = None
                        for other in allPiece:
                            if other.col == i and other.row == j and other != p:
                                victim = other
                                break
                        if victim:
                            victim.kill()
                        p.col, p.row = i, j
                        if not check(color):
                            Mate = False
                        p.col, p.row = oldX, oldY
                        if victim:
                            allPiece.add(victim)
                        if not Mate:
                            return False
    return Mate
def checkMove(piece,col,row,simulate=False):
    if piece.col==col and piece.row==row:
        return False
    if piece.piece_type=="pion":
        if piece.color=="white":
            if abs(piece.col-col)==1:
                if row==piece.row-1:
                    for p in allPiece:
                        if p.color=="black" and p.row==row and p.col==col:
                            return True
                        if p.piece_type=="pion" and p.color=="black" and p.moved==True and p.col==col and p.row==row+1:
                            return True
                    return False
                else:
                    return False
            elif piece.col==col:
                if piece.row==6:
                    if row==5 or row==4:
                        for p in allPiece:
                            if (p!=piece and p.col==col and (p.row==row or p.row==row+1)):
                                return False
                        if row==4 and not simulate:
                            piece.moved=True
                        return True
                    else:
                        return False
                else:
                    if row==piece.row-1:
                        for p in allPiece:
                            if p.col==col and p.row==row:
                                return False
                        return True
            else:
                return False
        else:
            if abs(piece.col - col) == 1:
                if row == piece.row + 1:
                    for p in allPiece:
                        if p.color == "white" and p.row == row and p.col == col:
                            return True
                        if p.piece_type=="pion" and p.color=="white" and p.moved==True and p.col==col and p.row==row-1:
                            return True
                    return False
                else:
                    return False
            elif piece.col == col:
                if piece.row == 1:
                    if row == 2 or row == 3:
                        for p in allPiece:
                            if (p!=piece and p.col==col and (p.row==row or p.row==row-1)):
                                return False
                        if row==3 and not simulate:
                            piece.moved=True
                        return True
                    else:
                        return False
                else:
                    if row == piece.row + 1:
                        for p in allPiece:
                            if p.col==col and p.row==row:
                                return False
                        return True
            else:
                return False
    elif piece.piece_type=="tura":
        if piece.col==col:
            if row<piece.row:
                for p in allPiece:
                    if p.col==piece.col and p.row>row and p.row<piece.row:
                        return False
                    if p.row==row and p.col==col:
                        if p.color==piece.color:
                            return False
                return True
            if row>piece.row:
                for p in allPiece:
                    if p.col==piece.col and p.row>piece.row and p.row<row:
                        return False
                    if p.row==row and p.col==col:
                        if p.color==piece.color:
                            return False
                return True
        elif piece.row==row:
            if col<piece.col:
                for p in allPiece:
                    if p.row==piece.row and p.col>col and p.col<piece.col:
                        return False
                    if p.row==row and p.col==col:
                        if p.color==piece.color:
                            return False
                return True
            if col>piece.col:
                for p in allPiece:
                    if p.row==piece.row and p.col>piece.col and p.col<col:
                        return False
                    if p.row==row and p.col==col:
                        if p.color==piece.color:
                            return False
                return True
        else:
            return False
    elif piece.piece_type=="cal":
        xMove=abs(piece.col-col)
        yMove=abs(piece.row-row)
        if (xMove==2 and yMove==1) or (xMove==1 and yMove==2):
            for p in allPiece:
                if p.col==col and p.row==row:
                    if piece.color==p.color:
                        return False
                    else:
                        return True
            return True
        else:
            return False
    elif piece.piece_type=="nebun":
        maxrow=max(piece.row,row)
        maxcol=max(piece.col,col)
        minrow=min(piece.row,row)
        mincol=min(piece.col,col)
        if abs(piece.col-col)==abs(piece.row-row):
            for p in allPiece:
                if p.row<maxrow and p.row>minrow and p.col<maxcol and p.col>mincol:
                    if abs(piece.col-p.col)==abs(piece.row-p.row):
                        return False
                if p.row==row and p.col==col:
                    if p.color==piece.color:
                        return False
            return True
        else:
            return False
    elif piece.piece_type=="rege":
        if abs(piece.row-row)>1 or abs(piece.col-col)>1:
            if simulate==True:
                return False
            if piece.moved==True:
                return False
            else:
                enemy = "black" if piece.color == "white" else "white"
                if squareAttacked(piece.col, piece.row, enemy):
                    return False
                rookS = None
                if col==piece.col-2:
                    if squareAttacked(piece.col - 1, piece.row, enemy):
                        return False
                    for p in allPiece:
                        if p.piece_type=="tura" and p.col==piece.col-4 and p.moved==False:
                            rookS=p
                        elif p.col<piece.col and p.col>0 and p.row==piece.row:
                            return False
                    if rookS==None:
                        return False
                    else:
                        rookS.col=rookS.col+3
                        rookS.updatePosition()
                        return True
                elif col==piece.col+2:
                    if squareAttacked(piece.col + 1, piece.row, enemy):
                        return False
                    for p in allPiece:
                        if p.piece_type=="tura" and p.col==piece.col+3 and p.moved==False:
                            rookS=p
                        elif p.col>piece.col and p.col<7 and p.row==piece.row:
                            return False
                    if rookS==None:
                        return False
                    else:
                        rookS.col=rookS.col-2
                        rookS.updatePosition()
                        return True
        else:
            for p in allPiece:
                if p.row==row and p.col==col:
                    if p.color==piece.color:
                        return False
                    else:
                        return True
            return True
    elif piece.piece_type=="regina":
        maxrow = max(piece.row, row)
        maxcol = max(piece.col, col)
        minrow = min(piece.row, row)
        mincol = min(piece.col, col)
        if abs(piece.col-col)==abs(piece.row-row):
            for p in allPiece:
                if p.row<maxrow and p.row>minrow and p.col<maxcol and p.col>mincol:
                    if abs(piece.col-p.col)==abs(piece.row-p.row):
                        return False
                if p.row==row and p.col==col:
                    if p.color==piece.color:
                        return False
            return True
        elif col==piece.col:
            for p in allPiece:
                if p.row<maxrow and p.row>minrow and p.col==piece.col:
                    return False
                if p.row==row and p.col==col:
                    if p.color==piece.color:
                        return False
            return True
        elif row==piece.row:
            for p in allPiece:
                if p.col<maxcol and p.col>mincol and p.row==piece.row:
                    return False
                if p.row==row and p.col==col:
                    if p.color==piece.color:
                        return False
            return True
        else:
            return False
def rebuild_layout():
    global dim, offset_x, offset_y, box, chBox, endBox, rstBox, width, height
    dim = min(width, height) / 12
    offset_x = (width - dim * 8) / 2
    offset_y = (height - dim * 8) / 2
    box.center = (width / 2, offset_y / 2)
    chBox.center = (width / 2, offset_y / 2 * 3)
    endBox.center = (width / 2, height / 2)
    rstBox.center = (width / 2, offset_y / 2)
    for r in range(8):
        for c in range(8):
            sq = tab[r][c]
            sq.surf = pygame.Surface((dim, dim))
            sq.resetColor()
            sq.rect.topleft = (offset_x + c * dim, offset_y + r * dim)
    for p in allPiece:
        p.dim = dim
        p.offset_x = offset_x
        p.offset_y = offset_y
        img = pygame.image.load(p.image_path).convert_alpha()
        p.image = pygame.transform.scale(img, (int(dim), int(dim)))
        p.rect = p.image.get_rect()
        p.updatePosition()

def drawPromotionMenu(color):
    options = ["regina", "tura", "nebun", "cal"]
    images = {
        "white": ["Asset/white-queen.png", "Asset/white-rook.png", "Asset/white-bishop.png", "Asset/white-knight.png"],
        "black": ["Asset/black-queen.png", "Asset/black-rook.png", "Asset/black-bishop.png", "Asset/black-knight.png"],
    }
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))
    box_w, box_h = 500, 160
    box_x = width // 2 - box_w // 2
    box_y = height // 2 - box_h // 2
    pygame.draw.rect(screen, (240, 235, 220), (box_x, box_y, box_w, box_h), border_radius=16)
    pygame.draw.rect(screen, (100, 100, 100), (box_x, box_y, box_w, box_h), width=2, border_radius=16)
    label = font.render("Promote to:", True, (0, 0, 0))
    screen.blit(label, (box_x + box_w // 2 - label.get_width() // 2, box_y + 10))
    for i, img_path in enumerate(images[color]):
        img = pygame.image.load(img_path).convert_alpha()
        img = pygame.transform.scale(img, (80, 80))
        ix = box_x + 20 + i * 115
        iy = box_y + 65
        screen.blit(img, (ix, iy))

def format_time(seconds):
    seconds = max(0, int(seconds))
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"

def reset_game():
    global turn, selectedPiece, squareSel, previousPiece, inCheck, mated, dragging, original_col, original_row,promoting,promotingPawn,promotingColor,white_time,black_time,last_tick,time_out
    turn = "white"
    inCheck = False
    mated = False
    promoting = False
    promotionPawn = None
    promotionColor = None
    if squareSel != None:
        squareSel.resetColor()
    squareSel = None
    selectedPiece = None
    previousPiece = None
    dragging = False
    original_col = 0
    original_row = 0
    white_time = CLOCK_TIME
    black_time = CLOCK_TIME
    last_tick = pygame.time.get_ticks()
    time_out = None
    allPiece.empty()
    setPieces()
turn = "white"
inCheck = False
mated = False
squareSel = None
selectedPiece = None
previousPiece = None
dragging = False
original_col = 0
original_row = 0
promoting = False
promotionPawn = None
promotionColor = None
running=True
setPieces()
while running:
    screen.fill((141, 177, 235))
    now = pygame.time.get_ticks()
    dt = (now - last_tick) / 1000.0
    last_tick = now
    if not mated and not promoting and time_out is None:
        if turn == "white":
            white_time -= dt
            if white_time <= 0:
                white_time = 0
                time_out = "white"
        else:
            black_time -= dt
            if black_time <= 0:
                black_time = 0
                time_out = "black"
    if check(turn):
        if not inCheck:
            check_sound.play()
            inCheck = True
        if checkMate(turn):
            mated=True
            screen.fill((247,228,228))
            screen.blit(rst,rstBox)
            if turn=="white":
                screen.blit(blackWon,endBox)
            else:
                screen.blit(whiteWon,endBox)
        else:
            draw_inner_glow(screen, (255, 0, 0), glow_thickness=75)
            screen.blit(ch,chBox)
    else:
        inCheck = False
    if time_out is not None:
        mated = True
        screen.fill((247, 228, 228))
        winner = "White" if time_out == "black" else "Black"
        msg = hugeFont.render(f"{winner} wins on time!", True, (0, 0, 0))
        msg_rect = msg.get_rect(center=(width / 2, height / 2))
        screen.blit(msg, msg_rect)
        screen.blit(rst, rstBox)
    if not mated:
        for row_index,row in enumerate(tab):
            for col_index,square in enumerate(row):
                screen.blit(square.surf,square.rect)
        for i in range(8):
            text_surf = boardFont.render(columns[i], True, (0, 0, 0))
            x_center = offset_x + (i * dim) + dim/2
            text_rect = text_surf.get_rect(center=(x_center, offset_y + dim * 8 + dim * 0.5))
            screen.blit(text_surf, text_rect)
            text_surf = boardFont.render(rows[i], True, (0, 0, 0))
            y_center = offset_y + (i * dim) + dim/2
            text_rect = text_surf.get_rect(center=(offset_x - dim * 0.5, y_center))
            screen.blit(text_surf, text_rect)
        allPiece.draw(screen)
        clock_bg_white = (255, 255, 255) if turn == "white" else (180, 180, 180)
        clock_bg_black = (50, 50, 50) if turn == "black" else (120, 120, 120)
        wt_surf = font.render(format_time(white_time), True, (0, 0, 0))
        wt_rect = wt_surf.get_rect()
        wt_rect.bottomright = (offset_x + dim * 9.5, offset_y + dim * 8)
        pygame.draw.rect(screen, clock_bg_white,
                         wt_rect.inflate(20, 10), border_radius=8)
        screen.blit(wt_surf, wt_rect)
        bt_surf = font.render(format_time(black_time), True, (255, 255, 255))
        bt_rect = bt_surf.get_rect()
        bt_rect.topright = (offset_x + dim * 9.5, offset_y)
        pygame.draw.rect(screen, clock_bg_black,bt_rect.inflate(20, 10), border_radius=8)
        screen.blit(bt_surf, bt_rect)
        if turn=="white":
            screen.blit(whiteTurn,box)
        else:
            screen.blit(blackTurn,box)
    for event in pygame.event.get():
        attempt_move = False
        targetCol = -1
        targetRow = -1
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if mated==True:
                    reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            if promoting:
                options = ["regina", "tura", "nebun", "cal"]
                imgs = {
                    "white": ["Asset/white-queen.png", "Asset/white-rook.png", "Asset/white-bishop.png",
                              "Asset/white-knight.png"],
                    "black": ["Asset/black-queen.png", "Asset/black-rook.png", "Asset/black-bishop.png",
                              "Asset/black-knight.png"],
                }
                box_x = width // 2 - 250
                box_y = height // 2 - 80
                for i, piece_type in enumerate(options):
                    ix = box_x + 20 + i * 115
                    iy = box_y + 65
                    if ix <= x <= ix + 80 and iy <= y <= iy + 80:
                        img_path = imgs[promotionColor][i]
                        col = promotionPawn.col
                        row = promotionPawn.row
                        promotionPawn.kill()
                        newPiece = Piece(promotionColor, piece_type, img_path, col, row, offset_x, offset_y)
                        allPiece.add(newPiece)
                        if promotionColor == "white":
                            turn = "black"
                        else:
                            turn = "white"
                        promoting = False
                        promotionPawn = None
                        promotionColor = None
                        break
                continue
            if mated==True:
                continue
            if x >= offset_x and x < width-offset_x and y >= offset_y and y < height-offset_y:
                clickedCol = int((x - offset_x) // dim)
                clickedRow = int((y - offset_y) // dim)
                if selectedPiece != None and not dragging:
                    clicked_own_piece = False
                    for p in allPiece:
                        if p.col == clickedCol and p.row == clickedRow and p.color == turn:
                            clicked_own_piece = True
                            break
                    if not clicked_own_piece:
                        attempt_move = True
                        targetCol = clickedCol
                        targetRow = clickedRow
                    else:
                        selectedPiece = None
                if not attempt_move:
                    for p in allPiece:
                        if p.col == clickedCol and p.row == clickedRow and p.color == turn:
                            selectedPiece = p
                            dragging = True
                            original_col = p.col
                            original_row = p.row
                            if squareSel != None:
                                squareSel.resetColor()
                            squareSel = tab[clickedRow][clickedCol]
                            squareSel.updateColor()
                            break
        elif event.type == pygame.MOUSEMOTION:
            if dragging and selectedPiece != None:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selectedPiece.rect.center = (mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging and selectedPiece != None:
                dragging = False
                (x, y) = pygame.mouse.get_pos()
                if x >= offset_x and x < width-offset_x and y >= offset_y and y < height-offset_y:
                    releasedCol = int((x - offset_x) // dim)
                    releasedRow = (int((y - offset_y) // dim))
                    if releasedCol == original_col and releasedRow == original_row:
                        selectedPiece.updatePosition()
                    else:
                        attempt_move = True
                        targetCol = releasedCol
                        targetRow = releasedRow
                else:
                    selectedPiece.col = original_col
                    selectedPiece.row = original_row
                    selectedPiece.updatePosition()
                    selectedPiece = None
                    if squareSel != None:
                        squareSel.resetColor()
                        squareSel = None
        elif event.type in (pygame.VIDEORESIZE, pygame.WINDOWRESIZED):
                        width, height = screen.get_size()  # works for both
                        rebuild_layout()
        if attempt_move and selectedPiece != None:
            if checkMove(selectedPiece, targetCol, targetRow):
                captured = None
                for p in allPiece:
                    if p.col == targetCol and p.row == targetRow and p != selectedPiece:
                        captured = p
                        break
                if captured:
                    captured.kill()
                selectedPiece.col = targetCol
                selectedPiece.row = targetRow
                if check(turn):
                    selectedPiece.col = original_col
                    selectedPiece.row = original_row
                    selectedPiece.updatePosition()
                    if captured:
                        allPiece.add(captured)
                    selectedPiece = None
                    if squareSel != None:
                        squareSel.resetColor()
                        squareSel = None
                    continue
                enPassant = False
                if selectedPiece.piece_type == "pion" and original_col != targetCol and captured is None:
                    enPassant = True
                selectedPiece.updatePosition()
                move_sound.play()
                if selectedPiece.piece_type == "pion":
                    if (selectedPiece.color == "white" and selectedPiece.row == 0) or (selectedPiece.color == "black" and selectedPiece.row == 7):
                        promoting = True
                        promotionPawn = selectedPiece
                        promotionColor = selectedPiece.color
                if selectedPiece.piece_type == "rege" or selectedPiece.piece_type == "tura":
                    selectedPiece.moved = True
                if previousPiece != None and previousPiece.piece_type == "pion":
                    previousPiece.moved = False
                previousPiece = selectedPiece
                if not promoting:
                    if turn == "white":
                        turn = "black"
                        for p in allPiece:
                            if p.color == "black" and p.row == targetRow and p.col == targetCol:
                                p.kill()
                        if enPassant:
                            for p in allPiece:
                                if p.col == targetCol and p.row == targetRow + 1:
                                    p.kill()
                                    break
                    else:
                        turn = "white"
                        for p in allPiece:
                            if p.color == "white" and p.row == targetRow and p.col == targetCol:
                                p.kill()
                        if enPassant:
                            for p in allPiece:
                                if p.col == targetCol and p.row == targetRow - 1:
                                    p.kill()
                                    break
                selectedPiece = None
                if squareSel != None:
                    squareSel.resetColor()
                    squareSel = None
            else:
                selectedPiece.col = original_col
                selectedPiece.row = original_row
                selectedPiece.updatePosition()
                selectedPiece = None
                if squareSel != None:
                    squareSel.resetColor()
                    squareSel = None
    if promoting:
        drawPromotionMenu(promotionColor)
    pygame.display.flip()
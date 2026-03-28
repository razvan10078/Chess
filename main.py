import pygame
pygame.init()
dim=128

font = pygame.font.Font('freesansbold.ttf', 48)
whiteTurn = font.render("White's Turn",True,(252,246,227))
blackTurn = font.render("Black's Turn",True,(0,0,0))
box = whiteTurn.get_rect()
box.center=(700,94)
boardFont = pygame.font.SysFont('Arial', 32,bold=True)
columns=['A','B','C','D','E','F','G','H']
rows=['8','7','6','5','4','3','2','1']

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
    def __init__(self, color, piece_type, image_path, col, row, offset_x=188, offset_y=188):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.color = color
        self.piece_type = piece_type
        self.col = col
        self.row = row
        self.dim = dim
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.updatePosition()

    def updatePosition(self):
        x_pos=self.offset_x+(self.col*dim)
        y_pos=self.offset_y+(self.row*dim)
        self.rect.center=(x_pos+dim//2,y_pos+dim//2)

tab=[]
for row in range(8):
    cur=[]
    for col in range(8):
        x_pos=188+col*dim
        y_pos=188+row*dim
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

WIDTH, HEIGHT = 1400, 1400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sah")

timer = pygame.time.Clock()
fps = 60

allPiece=pygame.sprite.Group()

for col in range(8):
    pionN=Piece("black","pion","Asset/black-pawn.png",col,1)
    pionA=Piece("white","pion","Asset/white-pawn.png",col,6)
    allPiece.add(pionN)
    allPiece.add(pionA)

for col in range(8):
    if col==0 or col==7:
        turaN=Piece("black","tura","Asset/black-rook.png",col,0)
        turaA=Piece("white","tura","Asset/white-rook.png",col,7)
        allPiece.add(turaN)
        allPiece.add(turaA)
    elif col==1 or col==6:
        calN=Piece("black","cal","Asset/black-knight.png",col,0)
        calA=Piece("white","cal","Asset/white-knight.png",col,7)
        allPiece.add(calN)
        allPiece.add(calA)
    elif col==2 or col==5:
        nebunN=Piece("black","nebun","Asset/black-bishop.png",col,0)
        nebunA=Piece("white","nebun","Asset/white-bishop.png",col,7)
        allPiece.add(nebunN)
        allPiece.add(nebunA)
    elif col==4:
        regeN=Piece("black","rege","Asset/black-king.png",col,0)
        regeA=Piece("white","rege","Asset/white-king.png",col,7)
        allPiece.add(regeN)
        allPiece.add(regeA)
    elif col==3:
        reginaN=Piece("black","regina","Asset/black-queen.png",col,0)
        reginaA=Piece("white","regina","Asset/white-queen.png",col,7)
        allPiece.add(reginaN)
        allPiece.add(reginaA)

def checkMove(piece,col,row):
    if piece.col==col and piece.row==row:
        return False
    if piece.piece_type=="pion":
        if piece.color=="white":
            if abs(piece.col-col)==1:
                if row==piece.row-1:
                    for p in allPiece:
                        if p.color=="black" and p.row==row and p.col==col:
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
                    return False
                else:
                    return False
            elif piece.col == col:
                if piece.row == 1:
                    if row == 2 or row == 3:
                        for p in allPiece:
                            if (p!=piece and p.col==col and (p.row==row or p.row==row-1)):
                                return False
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
squareSel=None
selectedPiece=None
running = True
turn="white"
while running:
    screen.fill((141, 177, 235))
    for row_index,row in enumerate(tab):
        for col_index,square in enumerate(row):
            screen.blit(square.surf,square.rect)
    for i in range(8):
        text_surf = boardFont.render(columns[i], True, (0, 0, 0))
        x_center = 188 + (i * 128) + 64
        text_rect = text_surf.get_rect(center=(x_center, 1250))
        screen.blit(text_surf, text_rect)
        text_surf = boardFont.render(rows[i], True, (0, 0, 0))
        y_center = 188 + (i * 128) + 64
        text_rect = text_surf.get_rect(center=(150, y_center))
        screen.blit(text_surf, text_rect)
    allPiece.draw(screen)
    if turn=="white":
        screen.blit(whiteTurn,box)
    else:
        screen.blit(blackTurn,box)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (x,y) = pygame.mouse.get_pos()
            if x>=188 and x<1212 and y>=188 and y<1212:
                if squareSel!=None:
                    squareSel.resetColor()
                selectedCol=(x-188)//128
                selectedRow=(y-188)//128
                select=tab[selectedRow][selectedCol]
                squareSel=select
                if selectedPiece==None:
                    for p in allPiece:
                        if p.col==selectedCol and p.row==selectedRow and p.color==turn:
                            selectedPiece=p
                            select.updateColor()
                            break
                else:
                    if checkMove(selectedPiece,selectedCol,selectedRow):
                        selectedPiece.col=selectedCol
                        selectedPiece.row=selectedRow
                        selectedPiece.updatePosition()
                        selectedPiece=None
                        if turn=="white":
                            for p in allPiece:
                                if p.color=="black" and p.col==selectedCol and p.row==selectedRow:
                                    p.kill()
                            turn="black"
                        else:
                            for p in allPiece:
                                if p.color=="white" and p.col==selectedCol and p.row==selectedRow:
                                    p.kill()
                            turn="white"
                    else:
                        selectedPiece=None
            pygame.display.flip()



    pygame.display.flip()

import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650 #スクリーン
DELTA ={
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとんrctまたは爆弾rct
    戻り値:判定結果タプル(横,縦)
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate = True,True
    if rct.left<0 or WIDTH<rct.right:
        yoko = False
    if rct.top<0 or HEIGHT<rct.bottom:
        tate = False
    return yoko,tate
def gameover(screen:pg.Surface)->None:
    img=pg.image.load("fig/8.png")
    fonto=pg.font.Font(None,80)
    txt_rct=fonto.render("GAME OVER",255,255,255)
    screen.blit(txt_rct,[370,320])
    screen.blit(img,[300,700])
    screen.blit(img,[700,300])
    bb=pg.Surface((WIDTH+HEIGHT))
    pg.draw.rect(bb,(0,0,0),(0,0,WIDTH,HEIGHT))
    screen.blit(txt_rct,[370,320])
    screen.blit(img,[300,300])
    screen.blit(img,[700,300])
    pg.display.update()
    time.sleep(5)
    return
def init_bb_imgs() ->tuple[list[pg.Surface],list[int]]:
    bb_accs=[a for a in range(1,11)]
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.c(bb_img,(255,0,0),(10*r,10*r),10*r)
        return
    vx =1
    tmr=r
    bb_imgs,bb_accs=init_bb_imgs()
    avx = vx*bb_accs[min(tmr//500,9)]
    bb_img=bb_imgs[min(tmr//500,9)]


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bb_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_ing = pg.Surface((20,20))
    pg.draw.circle(bb_ing,(255,0,0,),(10,10),10)
    bb_rct = bb_ing.get_rect()
    bb_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    bb_img.set_colorkey((0,0,0))
    vx,vy=+5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bb_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            print("GAME OVER")
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        

        #if key_lst[pg.K_UP]:
         #   sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
         #   sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
         #   sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
         #   sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        screen.blit(bb_ing,bb_rct)
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx *=-1
        if not tate:
            vy *=-1 
        pg.display.update()
        tmr += 1
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            time.sleep(5)
            return
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

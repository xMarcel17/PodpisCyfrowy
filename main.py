import cv2
import numpy as np

def calculateColor(px):
    ret = px[2]
    ret = ret << 8
    ret += px[1]
    ret = ret << 8
    ret += px[0]
    return ret

def calculateColorI(x,y,px):
    if(x == 0): # dodalem to zeby nie bylo bledow ze zczytuje kolor z poza obrazka
        x += 1  # narazie zostawiam, zobaczymy czy dziala
    if(x == 639): # dziala
        x -= 1
    if(y == 0):
        y += 1
    if(y == 359):
        y -= 1
    return (
        calculateColor(px[y-1][x-1])+calculateColor(px[y][x-1])+calculateColor(px[y+1][x-1])+
        calculateColor(px[y-1][x])+calculateColor(px[y][x])+calculateColor(px[y+1][x])+
        calculateColor(px[y-1][x+1])+calculateColor(px[y][x+1])+calculateColor(px[y+1][x+1])
    )/9

randomBits = []
filename = 'Kanye_West_-_Gotcha'
vc = cv2.VideoCapture(filename+'.mp4')
audio = open(filename+'.wav', 'rb')
c = 1
# wymiary obrazu
W = 640
H = 356
# vt i th
img = cv2.imread("frames/90.jpg")
vt = np.var(img)/2
th = 100
# zmienne initial value
R,G,B = 0,0,0
R1,G1,B1 = 0,0,0
R2,G2,B2 = 0,0,0
if vc.isOpened():
    rval , frame = vc.read()
else:
    rval = False
# rozmiar 640x356       indeksowanie pikseli od 0
state = 0
audio_content = bytearray(audio.read())
ranBitCnt=0
i = 0  # i = 0-7
runcnt = 0
K = 500
x = int(W/2)
y = int(H/2)
SN1=0
SN2=0
SN3=0
SN4=0
SN5=0
watchdog=0
j=1
while c<=162:
    if(state == 0):
        img = cv2.imread("frames/"+str(c)+".jpg")
        print(c)
        # a----------------------------------------------------------------
        px = img[y][x]

        R = px[2]
        G = px[1]
        B = px[0]

        color = calculateColorI(x,y,img)
        x = round((color)%(W/2)+(W/4))
        y = round((color)%(H/2)+(H/4))
        # b----------------------------------------------------------------
        
        state = 1
    elif(state == 1):
        # d----------------------------------------------------------------
        watchdog = 0
        while (True):
            diff = (R-R1)**2 + (G-G1)**2 + (B-B1)**2

            if(diff < vt):
                x = (x + (R ^ G) + 1) % W
                y = (y + (G ^ B) + 1) % H
                px = img[y][x]
                watchdog+=1
                if(watchdog > th):
                    c+=1
                    state = 0
                    break
                continue
            state = 2
            break  
        
    elif(state == 2):
        # c----------------------------------------------------------------
        Gx = G
        Gy = G
        Gz = G
        Ga = G
        Gb = G
        n1 = (10 + (R*i + (Gx << 2) + B + runcnt)%(K/2))
        n2 = (15 + (R*i + (Gy << 3) + B + runcnt)%(K/2))
        n3 = (20 + (R*i + (Gz << 4) + B + runcnt)%(K/2))
        n4 = (5 + (R*i + (Ga << 1) + B + runcnt)%(K/2))
        n5 = (25 + (R*i + (Gb << 5) + B + runcnt)%(K/2))

        SN1 = audio_content[30000+j*K+int(n1)] 
        SN2 = audio_content[30000+j*K+int(n2)]
        SN3 = audio_content[30000+j*K+int(n3)]
        SN4 = audio_content[30000+j*K+int(n4)]
        SN5 = audio_content[30000+j*K+int(n5)]
        j+=1
        state = 3
    elif(state == 3):
        # e----------------------------------------------------------------
        ranBit = (1 & (R^G^B^R1^G1^B1^R2^G2^B2^SN1^SN2^SN3^SN4^SN5))
        randomBits.append(ranBit)
        ranBitCnt+=1
        # wynik = 0
        # if(ranBitCnt%8 == 0):
        #     for i in range (0,8):
        #         wynik += (2**(7-i))*randomBits[i]
        #     randomBits.clear()
        #     ranBitCnt=0
        #     with open("TEMP1.txt", 'w') as temp1:
        #         temp1.write(str(wynik)+'\n')
        print(str(c))
        i+=1
        R1 = R
        G1 = G
        B1 = B

        x = (((R^x) << 4)^(G^y))%W
        y = (((G^x) << 4)^(B^y))%H
        state = 2
        if(i==8):
            # g----------------------------------------------------------------
            R2 = R
            G2 = G
            B2 = B
            i = 0
            c += 1
            state = 0 
# f----------------------------------------------------------------
l = 0
with open("RandomBits.txt", 'w') as temp1:
    for i, bit in enumerate(randomBits):
        temp1.write(str(bit))
for i in randomBits:
    print("Bit numer "+str(l)+" = "+str(i))
    l += 1

audio.close()

# import cv2

# vc = cv2.VideoCapture('Kanye_West_-_Gotcha.mp4')
# c=1

# if vc.isOpened():
#     rval , frame = vc.read()
# else:
#     rval = False

# while rval:
#     rval, frame = vc.read()
#     cv2.imwrite('frames/'+str(c) + '.jpg',frame)
#     c = c + 1
#     cv2.waitKey(1)
# vc.release()
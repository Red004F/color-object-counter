import numpy as np
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX #font utilizzato per il contatore


webcam = cv2.VideoCapture(0 + cv2.CAP_DSHOW) #seleziona la webcam

color_search = np.zeros((200,200,3), np.uint8)
color_pick = np.zeros((200,200,3), np.uint8)

hue = 0
def color_select(event, x, y, flags, param): #funzione per selezionare il colore
    global hue
    B= frame[y,x][0]
    G= frame[y,x][1]
    R= frame[y,x][2]
    color_search[:] = (B,G,R)

    if event == cv2.EVENT_LBUTTONDOWN: #premendo tasto SX mouse seleziona il colore della finestra 'image'
        color_pick[:] = (B,G,R)
        hue = hsv[y,x][0]

def create_contour(mask): #funzione per creare i contour
    contours_count = 0
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    #cv2.CHAIN_APPROX_SIMPLE considera solo gli angoli del contour, serve a salvare memoria

    for contour in contours:
        area = cv2.contourArea(contour)
        if 200 < area < 10000: #il contour è creato se il blocco di pixel è tra 200 e 10000 pixel
            cv2.drawContours(frame, contour, -1,(79,0,255), 1)
            contours_count += 1
    return contours_count

def nothing(x):
    pass

cv2.namedWindow('image')
cv2.setMouseCallback('image', color_select)

cv2.namedWindow('slider')
cv2.resizeWindow('slider', 400, 80)
cv2.createTrackbar('Lower_hue', 'slider', 0, 179, nothing)
cv2.createTrackbar('Upper_hue', 'slider', 0, 179, nothing)

while True:
    _, frame = webcam.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    diff_lower_hue = cv2.getTrackbarPos('Lower_hue', 'slider')
    diff_upper_hue = cv2.getTrackbarPos('Upper_hue', 'slider')

    lower_hue = 0 \
        if hue - diff_lower_hue < 0 \
        else hue - diff_lower_hue
    upper_hue = hue + diff_upper_hue \
        if hue + diff_upper_hue < 179 \
        else 179
    #soglia minima e massima, basata sul colore selezionato
    lower_hsv = np.array([lower_hue,50,20])
    upper_hsv = np.array([upper_hue,255,255])

    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    count = create_contour(mask)

    cv2.putText(frame, 'Count: ' + str(count), (10, 20), font, 0.5, (79, 0, 255), 2)
    cv2.putText(frame, 'Upper: ' + str(upper_hsv), (10, 40), font, 0.5, (79, 0, 255), 2)
    cv2.putText(frame, 'Lower: ' + str(lower_hsv), (10, 60), font, 0.5, (79, 0, 255), 2)



    cv2.imshow('image', frame)
    #cv2.imshow('mask', mask) #finestra maschera colori
    #cv2.imshow('color_search', color_search) #finestra colore sul puntatore
    #cv2.imshow('color_pick', color_pick) #finestra colore selezionato

    if cv2.waitKey(1) & 0xFF == ord('q'): #chiude quando è premuto il tasto 'q'
        break

cv2.destroyAllWindows()

import cv2 as cv
import numpy as np

CIRCLE_RADIUS = 5
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CENTER_COORDINATES = (320, 240)
def find_direction(pos1, pos2):
    diff = pos1 - pos2
    if (diff < 0):
        print('-', diff, ' unit')
    else:
        print('+', diff, ' unit')
def print_path(circle_center):
    # roll
    print('Roll: ')
    find_direction(circle_center[0], CENTER_COORDINATES[0])
    # pitch
    print('Pitch: ')
    find_direction(circle_center[1], CENTER_COORDINATES[1])
def main():
    # Kamera ayarları
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    # Sarı halka için renk aralığı
    lower_range = np.array([20, 100, 100])
    upper_range = np.array([40, 255, 255])

    # Görüntülemede sorun varsa döngüyü sonlandırır
    while True:
        basarili, frame = camera.read()

        # Görüntüyü HSV renk uzayına dönüştürür
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Renk aralığını uygular
        mask = cv.inRange(hsv, lower_range, upper_range)

        # Maskeyi ortalama bir görüntüye dönüştür
        converted_mask = cv.medianBlur(mask, 5)

        # calculate moments of binary image
        M = cv.moments(converted_mask)
        (cX, cY) = CENTER_COORDINATES

        # find circle center
        if (M["m00"] != 0):
            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv.circle(frame, (cX, cY), 5, (255, 255, 255), -1)

        # draw line between circle-center and camera-center
        cv.line(frame, (cX, cY), CENTER_COORDINATES, (0, 255, 0), 2)
        cv.circle(frame, CENTER_COORDINATES, 1, (255, 0, 0), 3)

        # print path
        print_path((cX, cY))

        # Display the resulting frame
        cv.imshow('frame', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice

        if not basarili or cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()

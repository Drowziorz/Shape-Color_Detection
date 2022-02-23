import cv2
import numpy as np


class Outline:

    def __init__(self, image):
        self.image = cv2.imread(image)

    def thresh(self):
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, [5, 5], 0)
        ret, thresh = cv2.threshold(img_blur, 150, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return contours

    def color(self, kontur):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        kolory = [
            [50, 20, 20],    # zielony              górna granica
            [70, 255, 255],                        #dolna granica
            [170, 100, 20],  # czerwony
            [180, 255, 255],
            [110, 100, 20],  # niebieski
            [130, 255, 255],
            [0, 0, 0],       # czarny
            [180, 255, 50],
            [135, 100, 20],  # fioletowy
            [150, 255, 255]
        ]

        i = 0
        while i != len(kolory):

            lower_bound = np.array(kolory[i])
            upper_bound = np.array(kolory[i+1])

            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #result = cv2.bitwise_and(self.image, self.image, mask=mask)
            #cv2.drawContours(result, contours, 0, (140, 140, 0), 3)

            for cnt in contours:
                if len(cv2.approxPolyDP(cnt, 0.005 * cv2.arcLength(cnt, True), True)) == len(kontur):
                    return i

            i = i + 2

    def ksztalt(self, kontur):
        if len(kontur) == 4:
            return "Prostokat"

        elif len(kontur) == 6:
            return "Szesciokat"

        elif len(kontur) == 10:
            return "Gwiazda"

        elif len(kontur) in range(10, 17):
            return "Okrag"

        else:
            return "Serce"

    def sz(self, i):
        if i == 0:
            return "Zielony"

        elif i == 2:
            return "Czerwony"

        elif i == 4:
            return "Niebieski"

        elif i == 6:
            return "Czarny"

        elif i == 8:
            return "Fioletowy"

    def all(self):
        contours = self.thresh()
        img2 = self.image.copy()

        for cnt in contours:
            kontur = cv2.approxPolyDP(cnt, 0.005 * cv2.arcLength(cnt, True), True)

            x = kontur.ravel()[0]  # zmiana macierzy na ciąg znaków
            y = kontur.ravel()[1]

            shape = self.ksztalt(kontur)
            kolor = self.sz(self.color(kontur))

            cv2.putText(img2, ( kolor + ", " + shape ), (x, y), cv2.FONT_HERSHEY_SIMPLEX, .7, 0)
            cv2.imshow("koniec", img2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    #image = 'pcy.png'
    image = 'pct.png'
    #image = 'pcp.png'
    #image = 'pck.png'
    obj = Outline(image)
    obj.all()

import os

import cv2, time
import HandTrackingModule as htm


def get_next_question(cap):
    Ptime = 0

    FolderPath = "FingerImages"

    myFingers = os.listdir(FolderPath)

    OverlayList = []

    for imPath in myFingers:
        image = cv2.imread(f'{FolderPath}/{imPath}')
        OverlayList.append(image)

    tipIds = [4, 8, 12, 16, 20]

    detector = htm.HandDetector(detection=0.75)

    choosen_option = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

    totalFingers = 0

    t_end = time.time() + 10 * 1

    cap.set(3, 640)
    cap.set(4, 480)

    while time.time() < t_end :

        success, img = cap.read()
        img = detector.FindHands(img, draw=False)

        lmList = detector.FindPosition(img, draw=False)

        Ctime = time.time()
        fps = 1 / (Ctime - Ptime)
        Ptime = Ctime

        cv2.putText(img, f'FPS: {int(fps)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 2)

        cv2.imshow("Game", img)

        if len(lmList) != 0:
            fingers = []

            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)

            if totalFingers == 0:
                choosen_option[totalFingers] += 1
                if choosen_option[0] > 15:
                    return 0

            h, w, c = OverlayList[totalFingers - 1].shape
            #
            img[0:h, 0:w] = OverlayList[totalFingers - 1]


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return 0


def get_option(cap):
    Ptime = 0

    FolderPath = "FingerImages"

    myFingers = os.listdir(FolderPath)

    OverlayList = []

    for imPath in myFingers:
        image = cv2.imread(f'{FolderPath}/{imPath}')
        OverlayList.append(image)

    tipIds = [4, 8, 12, 16, 20]

    detector = htm.HandDetector(detection=0.75)

    choosen_option = {1: 0, 2: 0, 3: 0, 4: 0}

    totalFingers = 0

    t_end = time.time() + 30 * 1

    cap.set(3, 640)
    cap.set(4, 480)

    while time.time() < t_end:

        success, img = cap.read()
        img = detector.FindHands(img, draw=False)

        lmList = detector.FindPosition(img, draw=False)

        Ctime = time.time()
        fps = 1 / (Ctime - Ptime)
        Ptime = Ctime

        cv2.putText(img, f'FPS: {int(fps)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 2)

        cv2.imshow("Game", img)


        if len(lmList) != 0:
            fingers = []

            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)

            if totalFingers != 0 and totalFingers != 5:
                choosen_option[totalFingers] += 1
                if choosen_option[1] > 20:
                    return 1
                elif choosen_option[2] > 20:
                    return 2
                elif choosen_option[3] > 20:
                    return 3
                elif choosen_option[4] > 20:
                    return 4

            h, w, c = OverlayList[totalFingers - 1].shape
            #
            img[0:h, 0:w] = OverlayList[totalFingers - 1]


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(totalFingers, choosen_option)

    max_value = max(list(choosen_option.values()))

    for key, value in choosen_option.items():
        if value == max_value:
            return value

    return totalFingers




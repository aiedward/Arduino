import cv2
import serial
import time

face_recognizer = cv2.createEigenFaceRecognizer()
face_recognizer.load("C:\Users\Rainer\Documents\PycharmProjects\HelloWorld\HelloWorld\setfaces.yaml")
faces_detector = cv2.CascadeClassifier("C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml")
eyes_detector = cv2.CascadeClassifier("C:\opencv\sources\data\haarcascades\haarcascade_eye.xml")
cam = cv2.VideoCapture()
know_faces, unknow_faces = [], []
my_serial = serial.Serial('COM3', 115200)
time.sleep(1)

while True:
    if my_serial.inWaiting() > 0:
        """ Data received from the PIR sensor.. 1 - camera on, 0 - camera off """
        data = my_serial.read()

        if ord(data) == 0 and cam.isOpened():  # stop the camera
            cam.release()
            cv2.destroyAllWindows()

            if len(know_faces) == 0 == len(unknow_faces):
                print "Ninjas o Fantasmas!! :)"

            if len(know_faces) > 0:  # OK
                my_serial.write(str(0))
                print "Cara conocida. Todo OK. Musica favorita ON! Luces encedidas, Abrir ventanas!!"

                count = 0
                for i in know_faces:
                    cv2.imwrite('./knowfaces/subject'+str(count)+'.jpg', i)
                    count += 1
            else:
                if len(unknow_faces) > 0:  # KO
                    print "Cara desconocida. Alarma. Call 911. Guardar imagenes.."
                    my_serial.write(str(1))

            count = 0
            for i in unknow_faces:
                cv2.imwrite('./unknowfaces/subject'+str(count)+'.jpg', i)
                count += 1

        elif ord(data) == 1:  # start the camera
            know_faces, unknow_faces = [], []
            cam.open(0)

    if cam.isOpened():
        ret, img = cam.read()
        if ret:
            gray = cv2.cvtColor(img, cv2.cv.CV_BGR2GRAY)
            # gray = cv2.equalizeHist(gray)
            # gray = cv2.GaussianBlur(gray, (3, 3), 25)
            faces = faces_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(60, 60),
                                                    flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in faces:
                roi = gray[y:y + h, x:x + w]
                eyes = eyes_detector.detectMultiScale(roi, scaleFactor=1.3, minNeighbors=3, minSize=(10, 10),
                                                      flags=cv2.CASCADE_SCALE_IMAGE)

                if len(eyes) == 2:
                    resize = cv2.resize(roi, (40, 40))
                    label, confidence = face_recognizer.predict(resize)

                    if label == 0:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(img, time.ctime(time.time()), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(img, 'Rainer', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        know_faces.append(img)
                    else:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(img, time.ctime(time.time()), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.putText(img, 'unknow', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        unknow_faces.append(img)

                    cv2.imshow("FaceSecure & Arduino", img)
                    if cv2.waitKey(1) == 27:
                        break
                else:
                    cv2.imshow("FaceSecure & Arduino", img)
                    if cv2.waitKey(1) == 27:
                        break
            cv2.imshow("FaceSecure & Arduino", img)
            if cv2.waitKey(1) == 27:
                break
        else:
            print "Error Info: Camera disconnected."
            break

cam.release()
cv2.destroyAllWindows()

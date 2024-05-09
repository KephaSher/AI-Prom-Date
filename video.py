import cv2
from fer import FER
from time import time
from colors import *
import argparse

def main():
    def rescaleFrame(frame, scale=0.75):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale) 
        dimensions = (width, height)
        
        return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

    detector = FER(mtcnn=True)
    print(f"{blue}[INFO] Detector setup{reset}")

    camera = cv2.VideoCapture(0)
    print(f"{blue}[INFO] Camera setup{reset}")

    frame_width = int(camera.get(3)) 
    frame_height = int(camera.get(4)) 
    
    size = (frame_width, frame_height) 
    if save_video:
        result = cv2.VideoWriter('saved_video.avi',  
                            cv2.VideoWriter_fourcc(*'MJPG'), 
                            10, size) 


    file = open("emotion.txt", "w")
    file.write("neutral 62.0 1714516700.559366\n")
    file.close()
    print(f"{blue}[INFO] 'emotion.txt' setup{reset}")

    while True:
        _, img = camera.read()

        if save_video:
            result.write(image=img) 
        
        img = rescaleFrame(img)

        faces = detector.detect_emotions(img)

        for i, face in enumerate(faces):
            emotion = detector.top_emotion(img)
            if (len(emotion) == 0):
                continue
            if (not any(emotion)):
                continue
            box = face['box']

            x, y, w, h = box
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
            cv2.putText(img, emotion[0] + " " + str(round(emotion[1] * 100, 1)) + "%", 
                (x - 10, y), cv2.FONT_HERSHEY_COMPLEX, 2.0, (0, 255, 0), thickness=2)
            
            if i == 0:
                print(f"{blue}[INFO] Wrote emotion {emotion[0]} to 'emotion.txt at time {time()}'{reset}")
                with open("emotion.txt", "w") as f:
                    f.write(emotion[0] + " " + str(round(emotion[1] * 100, 1)) + " " + str(time()) + "\n")

                # emotion_count += 1

                # print(emotion_count)
                # if emotion_count % 10 == 0:
                #     with open("emotion.txt", "w") as f:
                #         f.write(emotion[0] + " " + str(round(emotion[1] * 100, 1)) + " " + str(time()) + "\n")
                #     emotion_count %= 10

        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            camera.release()
            if save_video:
                result.release()
            cv2.destroyAllWindows() 
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_video", default=False, 
                        help = "Save video or not")
    args = parser.parse_args()
    global save_video
    save_video = bool(args.save_video)
    main()
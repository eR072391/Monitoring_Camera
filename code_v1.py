import cv2
import datetime


class Color:
    RED = '\033[31m'#(文字)赤
    GREEN = '\033[32m'#(文字)緑
    YELLOW = '\033[33m'#(文字)黄
    RESET = '\033[0m'#全てリセット

red = (0,0,255)


def camera_check():
    for i in range(0, 5): 
        cap1 = cv2.VideoCapture(i)
        if cap1.isOpened(): 
            print(Color.GREEN + "VideoCapture(", i, ") : Found" + Color.RESET)
        else:
            print(Color.RED + "VideoCapture(", i, ") : None" + Color.RESET)
        cap1.release() 


def main():
    input(Color.YELLOW + 'Enterを押して、カメラ認識チェック処理を開始してください。' + Color.RESET)
    camera_check()
    camera_id = input(Color.YELLOW + '使用するカメラIDを入力してください(0-5)>' + Color.RESET)
    
    while True:
        print("動体検知の感度を選択してください。")
        print("""
            [1] 少(30)
            [2] 中(60)
            [3] 大(100)
            [4] 任意の数値を入力
            """)
        flag2 = input('> ')
        if flag2 == '1':
            value = 30
            break
        elif flag2 == '2':
            value = 60
            break
        elif flag2 == '3':
            value = 100
            break
        elif flag2 == '4':
            value == int(input('数値を入力> '))
            break
        else:
            print("[1-4]の範囲内で選択してください。")
    
    cap = cv2.VideoCapture(int(camera_id))
    #fps = int(cap.get(cv2.CAP_PROP_FPS))
    avg = None
    date = None
    flag = 0
    
    print(Color.YELLOW + "カメラを起動します。" + Color.RESET)
    print(Color.YELLOW + "①動体検知の通知を始めるタイミングで「s」キーを入力してください。" + Color.RESET)
    print(Color.YELLOW + "②監視を中止するには「x」キーを入力してください。" + Color.RESET)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        #グレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if avg is None:
            #比較するためのフレームを切り出す
            avg = gray.copy().astype("float")
            continue
        
        #現在の画像と移動平均の差を求める
        cv2.accumulateWeighted(gray, avg, 0.6)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
        
        
        
        #デルタ画像の閾値処理を行う
        thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
        #閾値を設定して２値化する
        contours = cv2.findContours(thresh.copy(),
                                    cv2.RETR_EXTERNAL, 
                                    cv2.CHAIN_APPROX_SIMPLE)[0]
        
        #差分があった点を画面に描く
        for target in contours:
            x, y, w, h = cv2.boundingRect(target)
            if w < value: continue #検知感度
            #求めた閾値からオリジナルの四角フレーム(rectangle)に描画する
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h), red ,2)
            if flag == 1:
                dt_now = datetime.datetime.now()
                dt_now = dt_now.strftime('%m月%d日 %H:%M:%S')
                if dt_now != date:
                    date = dt_now
                    print(date + "  動体を検出")
        
        #出力
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(30)
        if key == ord('s'):
            flag = 1
        elif key == ord('x'):
            break
    
    print(Color.YELLOW + "終了します。" + Color.RESET)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
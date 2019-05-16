#zlog側でモード周波数帯変更したときに対応（9700）
import serial

#zlog側の表示しているモード、周波数を取る
a='読み込んだモード'
b='読み込んだ周波数'


#モードを変える16進数
modeLSB=FEFE'受信アドレス''送信アドレス'010001FD
modeUSB=FEFE'受信アドレス''送信アドレス'010101FD
modeAM=FEFE'受信アドレス''送信アドレス'010201FD
modeCW=FEFE'受信アドレス''送信アドレス'010301FD
modeRTTY=FEFE'受信アドレス''送信アドレス'010401FD
modeFM=FEFE'受信アドレス''送信アドレス'010501FD

#そのaのモードに合わせてic9700に送るコード
if a=="SSB":
    ser = serial.Serial('送信先',9600,timeout=None)#送信先、bps、タイムアウト時間を決める
    ser.write("modeUSB")#送る
    ser.close()#閉じる

if a=="AM":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("modeAM")
    ser.close()

if a=="CW":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("modeCW")
    ser.close()

if a=="RTTY":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("modeRTTY")
    ser.close()

if a=="FM":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("modeFM")
    ser.close()

else:
    print("error")

#周波数変更のための16進数（モード、周波数によって違う）
b144fm=FEFE'受信アドレス''送信アドレス'000000004501FD
b430fm=FEFE'受信アドレス''送信アドレス'000000003304FD
b12gfm=FEFE'受信アドレス''送信アドレス'000000009512FD

b144ssb=FEFE'受信アドレス''送信アドレス'000000254401FD
b430ssb=FEFE'受信アドレス''送信アドレス'000000253004FD
b12gssb=FEFE'受信アドレス''送信アドレス'000000009412FD

b144cw=FEFE'受信アドレス''送信アドレス'000000104401FD
b430cw=FEFE'受信アドレス''送信アドレス'000000103004FD
b12gcw=FEFE'受信アドレス''送信アドレス'000000009412FD

#周波数ごとにic9700に送る１６進数を変える
if b==144 and a=="SSB":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b144ssb")
    ser.close()

if b==144 and a=="AM":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b144ssb")
    ser.close()

if b==144 and a=="CW":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b144cw")
    ser.close()

if b==144 and a=="RTTY":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b144cw")
    ser.close()

if b=430 and a="SSB":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b430ssb")
    ser.close()

if b==430 and a=="AM":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b430ssb")
    ser.close()

if b==430 and a=="CW":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b430cw")
    ser.close()

if b==430 and a=="RTTY":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b430cw")
    ser.close()

if b==12g and a=="SSB":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b12gssb")
    ser.close()

if b==12g and a=="AM":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b12gssb")
    ser.close()

if b==12g and a=="CW":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b12gcw")
    ser.close()

if b==12g and a=="RTTY":
    ser = serial.Serial('送信先',9600,timeout=None)
    ser.write("b12gcw")
    ser.close()

else:
    print("error")

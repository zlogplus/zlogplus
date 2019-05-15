import serial

whatfre=FEFE'受信アドレス''送信アドレス'03FD #周波数を知るためのコード
whatmode=FEFE'受信アドレス''送信アドレス'04FD #モードを知るためのコード

#読取り部
ser = serial.Serial('送信先',9600,timeout=None)#送り先を定義する
ser.write("whatmode") #モード何？
mode16= ser.readline() #１６進数で読み取り
ser.close() #閉じる

ser = serial.Serial('送信先',9600,timeout=None)
ser.write("whatfre") #周波数何？
fre16=ser.readline() #16進数で読み取り
ser.close()

#解読部
mode=mode16[10:12] #必要部分を取り出す
fre=fre16[19:21]+fre16[17:19] #ここはMHz 必要な部分を取り出してMHzの形に

#print部
#mode 数字によってmodeがわかるのでそれを示す
if mode==00 or mode==01:
  print("SSB")
if mode==02:
  print("AM")
if mode==03:
  print("CW")
if mode==04:
  print("RTTY")
if mode=05:
  print("FM")
else:
  print("other")

#周波数 バンドを示すために幅で検索
if fre>140 and fre<150:
  print("144MHz")
if fre>430 and fre<435:
  print("430MHz")
if fre>1200 and fre<1300:
  print("1.2GHz")
else:
  print("not amatuer band")

# -*- coding: utf-8 -*-

import codecs
import struct
import datetime

# zlogファイルの各チャンクをばらす
# クラス名はキャメルケースなので要注意
class ZlogData():
    def __init__(self, chunk = None):
        # データ全体
        self.all = chunk
        # 時刻: float(TDateTime)型, 0x00-0x07
        # 0x00 最下位 ... 0x07 最上位のため反転処理
        # time(self)も参照のこと
        self.time_hex = chunk[0x00:0x08][::-1]
        # コールサイン: char型, 0x08-0x14
        # chunk[0x08]に文字数あり
        self.cs_count = chunk[0x08]
        self.cs = chunk[0x09:0x09+chunk[0x08]].decode()
        # 送信ナンバー: char型, 0x15-0x33
        # chunk[0x15]に文字数あり
        self.tx_num_count = chunk[0x15]
        self.tx_num = chunk[0x16:0x16+chunk[0x15]].decode()
        # 受信ナンバー: char型, 0x34-0x53
        # chunk[0x34]に文字数あり
        self.rx_num_count = chunk[0x34]
        self.rx_num = chunk[0x35:0x35+chunk[0x34]].decode()
        # 送信RST: int型, 0x54-0x55
        # 上位は2バイト目のため反転処理
        self.tx_rst = int.from_bytes(chunk[0x54:0x56][::-1], 'big')
        # 受信RST: int型, 0x56-0x57
        # 上位は2バイト目のため反転処理
        self.rx_rst = int.from_bytes(chunk[0x56:0x58][::-1], 'big')
        # モード int型, 0x5C
        self.mode_num = chunk[0x5C] \
                if type(chunk[0x5C]) == int \
                else int.from_bytes(chunk[0x5C], 'big')
        # バンド int型, 0x5D
        self.band_num = chunk[0x5D] \
                if type(chunk[0x5D]) == int \
                else int.from_bytes(chunk[0x5D], 'big')
        # 相手の出力 int型, 0x5E
        self.output_num = chunk[0x5E] \
                if type(chunk[0x5E]) == int \
                else int.from_bytes(chunk[0x5E], 'big')
        # マルチ: char型, 0x5F-0x9C
        # chunk[0x5F]に文字数あり
        self.multi_count = chunk[0x5F]
        self.multi = chunk[0x60:0x60+chunk[0x5F]].decode()
        # Newマルチ int型, 0x9D
        self.newmulti_num = chunk[0x9D] \
                if type(chunk[0x9D]) == int \
                else int.from_bytes(chunk[0x9D], 'big')
        # 得点 int型, 0x9F
        self.point = chunk[0x9F] \
                if type(chunk[0x9F]) == int \
                else int.from_bytes(chunk[0x9F], 'big')
        # オペレータ char型, 0xA0-0xAE
        # chunk[0xA0]に文字数あり
        self.op_count = chunk[0xA0]
        self.op = chunk[0xA1:0xA1+chunk[0xA0]].decode('sjis')
        # メモ char型, 0xAF-0xF1
        # chunk[0xAF]に文字数あり
        self.memo_count = chunk[0xAF]
        self.memo = chunk[0xB0:0xB0+2*chunk[0xAF]].decode('sjis')

    def time(self):
        # bytesをdouble型に変換
        time_double = struct.unpack('!d', self.time_hex)[0]
        # time_double(1899/1/1 00:00:00からの経過日数)を日付形式に変換
        ref_time = datetime.datetime(1899, 1, 1, 0, 0, 0, 000000)
        t = ref_time + datetime.timedelta(days = time_double)
        return [t.year, t.month, t.day, \
                t.hour, t.minute, t.second, t.microsecond]

    def mode(self):
        # モードは1バイトで表される
        # 0:CW, 1:SSB, 2:FM, 3:AM, 4:RTTY, 5:Others
        mode = ['CW', 'SSB', 'FM', 'AM', 'RTTY', 'Others']
        return mode[self.mode_num] \
                if self.mode_num < len(mode) else 'Unknown'

    def band(self):
        # バンドは1バイトで表される
        band = ['1.9MHz', '3.5MHz', '7MHz', '10MHz', '14MHz', 
                '18MHz', '21MHz', '24MHz', '28MHz', '50MHz', 
                '144MHz', '430MHz', '1.2GHz', '2.4GHz', '5.6GHz', 
                '10GHz以上']
        return band[self.band_num] \
                if self.band_num < len(band) else 'Unknown'

    def output(self):
        # 出力は1バイトで表される
        # 0:P, 1:L, 2:M, 3:H
        output = ['P', 'L', 'M', 'H']
        return output[self.output_num] \
                if self.output_num < len(output) else 'Unknown'
    
    def newmulti(self):
        # 出力は1バイトで表される
        # 0:DUPLICATE, 1:NEW
        newmulti = ['DUPLICATE', 'NEW']
        return newmulti[self.newmulti_num] \
                if self.newmulti_num < len(newmulti) else 'Unknown'

    def data_all(self):
        return {
                'time': self.time(), 
                'cs_count': self.cs_count, 
                'cs': self.cs, 
                'tx_num_count': self.tx_num_count,
                'tx_num': self.tx_num,
                'rx_num_count': self.rx_num_count,
                'rx_num': self.rx_num,
                'tx_rst': self.tx_rst,
                'rx_rst': self.rx_rst,
                'mode': self.mode(),
                'band': self.band(),
                'output': self.output(),
                'multi': self.multi,
                'newmulti': self.newmulti(),
                'point': self.point,
                'op_count': self.op_count,
                'op': self.op,
                'memo_count': self.memo_count,
                'memo': self.memo
                }

def read_zlog(filename):
    filename = str(filename)
    zlogfile = open(filename, 'r+b')
    while True:
        data = zlogfile.read(256)
        if not data:
            break
        else:
            chunk = ZlogData(data)
        print(chunk.data_all())


if __name__ == "__main__":
    filename = input("filename: ")
    read_zlog(filename)

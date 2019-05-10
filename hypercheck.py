# -*- coding: utf-8 -*-

import re
import csv
import xml.etree.ElementTree as ET
import requests

def hypercheck(query):
	query = str(query)

	# 総務省から検索結果を取得
	xml_url = "https://www.tele.soumu.go.jp/musen/list?ST=1&OF=3&DA=1&OW=AT&DC=1&SC=1&MA=" + query
	res = requests.get(xml_url)
	root = ET.fromstring(res.text)

	# 検索文字列に一致する無線局のリストを作成
	hams = []
	for ham in root:
		if ham.tag == "musen":
			# ＊＊＊＊＊＊（JA1ZLO）のカッコ内を抜き出す
			callsign = re.sub("(.+（|）)", "", ham[0][1].text)
			place = ham[0][2].text
			hams.append([callsign, place])
	hams = sorted(list(map(list, set(map(tuple, hams)))))
	# コンテストナンバーをjcc.datから取得
	jccfile = open("jcc.dat", 'r')
	jcclist = csv.reader(jccfile, delimiter = '\t')
	for jcc in jcclist:
		for i in range(len(hams)):
			if hams[i][1] == jcc[1]:
				hams[i].append(jcc[0])
	
	return hams

if __name__ == "__main__":
	query = input("query: ")
	print(hypercheck(query))

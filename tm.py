from tradingview_ta import TA_Handler, Interval, Exchange
import datetime
import time
import tkinter as Tk
import sys


if len(sys.argv) < 4:
	print("")
	print("*** INVALID NUMBER OF ARGUMENTS ***")
	print("tm by damballahoueddo - V1.0")
	print("usage exemple: python tm.py VETUSDT CRYPTO BINANCE")
	print("")
	exit()

def get_price(symBol,ecran,bourse):
	symbol = symBol
	symbInterval = Interval.INTERVAL_1_MINUTE
	currAnalys = TA_Handler(symbol=symbol, screener=ecran, exchange=bourse, interval=symbInterval)
	analyse=currAnalys.get_analysis()
	prix=analyse.indicators['close']
	return prix


def GET_MESURE(symbol,ecran,bourse, symbInterval):
    currAnalys = TA_Handler(symbol=symbol, screener="crypto", exchange="binance", interval=symbInterval)
    mesure = currAnalys.get_analysis().summary
    return mesure
# ex: GET_MESURE("VETBUSD", "crypto", "binance" , Interval.INTERVAL_15_MINUTES)

def reDefresponse(reponse):
	if reponse=="BUY":
		reponse="B"
	if reponse=="STRONG_BUY":
		reponse="B"
	elif reponse=="SELL":
		reponse="S"
	elif reponse=="STRONG_SELL":
		reponse="S"
	elif reponse=="NEUTRAL":
		reponse="N"
	
	return reponse

def encadrementChaine(chaine):
	longueur=len(chaine)
	l1="-" * (longueur + 4)
	l2="| " + chaine + " |"
	l3=l1
	nChaine=l1 + "\n" + l2 + "\n" + l3
	return nChaine


def getAllMesureOf(symbol, ecran, bourse):
	
	
	# GET_MESURE(symbol,ecran,bourse, symbInterval)
	# ex: GET_MESURE("VETBUSD", "crypto", "binance" , Interval.INTERVAL_15_MINUTES)
	
	m5M = GET_MESURE(symbol, ecran, bourse, Interval.INTERVAL_5_MINUTES)
	m15M = GET_MESURE(symbol, ecran, bourse, Interval.INTERVAL_15_MINUTES)
	m1H = GET_MESURE(symbol, ecran, bourse, Interval.INTERVAL_1_HOUR)
	m4H = GET_MESURE(symbol, ecran, bourse, Interval.INTERVAL_4_HOURS)
	m1D = GET_MESURE(symbol, ecran, bourse, Interval.INTERVAL_1_DAY)
	m1W = GET_MESURE(symbol, ecran, bourse,Interval.INTERVAL_1_WEEK)
	
	
	m5M=m5M['RECOMMENDATION']
	m15M=m15M['RECOMMENDATION']
	m1H=m1H['RECOMMENDATION']
	m4H=m4H['RECOMMENDATION']
	m1D=m1D['RECOMMENDATION']
	m1W=m1W['RECOMMENDATION']
	
	m5M=reDefresponse(m5M)
	m15M=reDefresponse(m15M)
	m1H=reDefresponse(m1H)
	m4H=reDefresponse(m4H)
	m1D=reDefresponse(m1D)
	m1W=reDefresponse(m1W)
	
	mesuresPourImage=[m5M,m15M,m1H,m4H,m1D,m1W]
	
	chaineL1=symbol + " --> " + bourse.upper()
	chaineL1=encadrementChaine(chaineL1)
	
	chaineL2="[5m][15m][1h][4h][1d][1w]"
	chaineL3=" " + m5M + "    "+ m15M + "   " + m1H + "   " + m4H + "   " + m1D + "   " + m1W
	
	chaineComplete=chaineL1 + "\n" + chaineL2 + "\n" + chaineL3
	
	price=get_price(symbol, ecran, bourse)
	
	ImageMesure(mesuresPourImage,symbol,price)
	
	return chaineComplete

def ImageMesure(mesures,cryptoMesure,price):
	
	
	dDLM = datetime.datetime.now()
	dateDeLaMesure=(dDLM.strftime("%c"))
	
	root = Tk.Tk()
	root.title("CryptoMesure")
	root.configure(background='white')
	chaineTitre="CryptoMesure : " + cryptoMesure
	lTitre = Tk.Label(root, text = chaineTitre, font="Courier 12 bold",fg="black", bg="white")
	lTitre.pack()
	
	lechelleDeTemps=Tk.Label(root, text = " 5m  15m  1h  4h  1d  1w " , font="Courier 10 bold",fg="black", bg="white")
	lechelleDeTemps.pack()
	
	canvas = Tk.Canvas(root, bg="light grey",height=35, width=250)
	canvas.pack()
		
	pos=0
	cpt=0
	
	mMesureSortie = list()
	
	
	for n in mesures:
		cpt=cpt+1
		
		if n=="S":
			pastille = canvas.create_oval(30,30,50,50,width=1,fill="red", outline="")
			
		elif n=="B":
			pastille = canvas.create_oval(30,30,50,50,width=1,fill="green", outline="")
			
		elif n=="N":
			pastille = canvas.create_oval(30,30,50,50,width=1,fill="grey", outline="")
			
		#Positionnement de la pastille
		if cpt==1:
			pos=5
		elif cpt==2:
			pos=39
		elif cpt==3:
			pos=75
		elif cpt==4:
			pos=108
		elif cpt==5:
			pos=140
		elif cpt==6:
			pos=170
		
		mMesureSortie.append(n)
		
		canvas.move(pastille,pos,-20)
	
	#print(mMesureSortie)
	
	#Sens bullish
	#------------
	if mMesureSortie==(['B','B','B','B','B','B']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" + str(price) +"\n\n" + "For resume : \n\nAll is mega bullish, you can sleep now !" + "\n"
	
	elif mMesureSortie==(['S','B','B','B','B','B']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" +str(price) + "\n\n" +"For resume : \n\nAll is mega bullish, again !" + "\n"
	
	elif mMesureSortie==(['S','S','B','B','B','B']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" +str(price) + "\n\n" +"For resume : \n\nNo need to worry, but if the H1 turns red, it may be a trend reversal is brewing." + "\n"
	
	elif mMesureSortie==(['S','S','S','B','B','B']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" +str(price) + "\n\n" +"For resume : \n\nA trend reversal in H1 is not nothing in trading, it is advisable to look at \nthe MACD and the RSI to ensure that the trendline is still respected." + "\n"
	
	elif mMesureSortie==(['S','S','S','S','B','B']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" +str(price) + "\n\n" +"For resume : \n\nOkay, a bearish divergence is emerging in H4. You need to watch if the \ntrendline is not broken, if the RSI is going down, if a golden cross has appeared \non the MACD and check the number of candles red in volume.\nIt might be time to take some profit." + "\n"
		
	elif mMesureSortie==(['S','S','S','S','S','B']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" +str(price) + "\n\n" +"For resume : \n\nWarning, the trend is clearly bearish and does not bode very well. \nIt would be wise, as a safety measure, \nto sell so as not to lose too much of your investment." + "\n"
	
	elif mMesureSortie==(['S','S','S','S','S','S']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" +str(price) + "\n\n" +"For resume : \n\nIf you are a trader and you have not sold sooner, you are in deficit, \nit would be better not to try anything for the moment, not to sell and to wait for a significant rise. \nIf, on the contrary, you wish to enter, wait a little until the D1 and the H4 are clearly in the green, \it is preferable." + "\n"
	
	#Sens bearish
	#------------
	if mMesureSortie==(['B','S','S','S','S','S']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" + str(price) +"\n\n" + "For resume : \n\nIf you are a trader and you have not sold sooner, you are in deficit, \nit would be better not to try anything for the moment, not to sell and to wait for a significant rise. \nIf, on the contrary, you wish to enter, wait a little until the D1 and the H4 are clearly in the green, \it is preferable." + "\n"
	
	if mMesureSortie==(['B','B','S','S','S','S']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" + str(price) +"\n\n" + "For resume : \n\A slight bullish burst at 15 minutes is not really a sign of a rise ... \nLet's be patient."
	
	if mMesureSortie==(['B','B','B','S','S','S']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" + str(price) +"\n\n" + "For resume : \n\There, it starts to be interesting. A golden cross should take shape in H1 \nand this trend should be continued in H4. Get ready, there may be an interesting buy signal. \nCheck the RSI and MACD."
	
	if mMesureSortie==(['B','B','B','B','S','S']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" + str(price) +"\n\n" + "For resume : \n\There a bullish divergence in H4 is a strong buy signal. Check if the trend line \nis going up and see if the 1D volume starts to fill up properly. If a golden cross appears in 1D, \nit's a buy signal!"
	
	if mMesureSortie==(['B','B','B','B','B','S']):
		advisory="\n"+ dateDeLaMesure + "\n" + "Price : $" + str(price) +"\n\n" + "For resume : \n\If you are a trader and have taken a buy position in H4 or 1D, you have done well. \nIf the uptrend continues in 1D for a week, we are clearly in an uptrend. Keep this position \nat least until a downtrend in 1D or 4H."
	
	MessageAvertissement=Tk.Label(root, text = advisory , font="Courier 10",fg="black", bg="white")
	MessageAvertissement.pack()
	
	SignatureDamballah=Tk.Label(root, text = "***This is not a professional financial advise***\n[Thanks for watching]\n\n {CryptoMesure} By @damballahoueddo" , font="Verdana 8 italic",fg="purple", bg="white")
	SignatureDamballah.pack()
	
	root.mainloop()

try:
	param1 = sys.argv[1]
	param2 = sys.argv[2]
	param3 = sys.argv[3]
	getAllMesureOf(param1,param2,param3)
except ValueError:
	print("An error as ended the program, sorry")











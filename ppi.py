
# http://en.wikipedia.org/wiki/Comparison_of_e-book_readers
#  go & sort by PPI descending

from math import *
#import math
def sqr(x):return x*x
def ppi(px,py,dinch): return sqrt(sqr(px)+sqr(py))/dinch
#print ppi, pixel-per-inch 
def pr_ppi(name, px,py,dinch): print name,", %.1f\" :"%dinch, "\t%.1f"%ppi(px,py,dinch)
#ppmm()= ppi()/25.4

def main():
  pr_ppi("Acer Aspire 5920 ",       1280 , 800, 15.4 )
  pr_ppi("Apple iPhone 4S",         960, 640, 3.5 ) #Multi-Touch display ! # 326 ppi
  pr_ppi("Samsung SyncMaster 720B", 1280, 1024, 17)
  pr_ppi("Dell Latitude E6430",       1366, 768, 14.0)

  pr_ppi("ONDA v975m", 2048,1536,9.7)
  pr_ppi("Samsung Galaxy Tab Pro 8.4", 2560, 1600, 8.4)
  pr_ppi("Xiaomi MiPad 2014"         , 1536,2048,7.9)
  print
  pr_ppi("Google Nexus 7 ASUS (2013)", 1920, 1200,7 )
  pr_ppi("Google Nexus 6 Moto (2014)", 2560,1440, 5.96 )
  pr_ppi("Google Nexus 5 LG (2013)", 1920, 1080, 4.95 )
  pr_ppi("LG G3 (2014)", 2560, 1440, 5.5 )
  print
  pr_ppi("Asus Fonepad Note 6",        1080,1920,6)
  pr_ppi("AXGIO NEON N3 5\" HD", 1280, 800, 5.0)
  print
  pr_ppi("OnePlus One (2014)", 1920,1080, 5.5)
  pr_ppi("Elephone P6000", 1280, 720, 5.0)
  pr_ppi("Alcatel Onetouch Pop C1", 480,320, 3.5)
  print

  pr_ppi("ALLFINE7 7\" ATM7029 Quad Core Android 4.1.1 Tablet with 4K Play & Front Camera", 1024,600,7 ) #$80+$7shipmnt
  pr_ppi("Ainol 7 Venus Tablet", 1280, 800, 7)
  pr_ppi("HyperTAB 7\" Capacitive A23 Dual core Tablet Android 4.2 4GB Cam WIFI", 800, 480, 7)
  pr_ppi("MP Mini S5 Smartphone 4.5 Inch", 854,480, 4.5)
  pr_ppi("Colorfly E708 Q1 7\" Android 4.2 Quad-Core IPS", 1280,800,7.0)
  pr_ppi("Axgio Neon N1 5\" IPS HD 1.3GHz MTK6582 4-Core OS Neonado-1.0", 1280,800,5.0)
  pr_ppi("Elephone 2000 5.5\" IPS HD 1.7GHz MTK6592 8-core", 1280,720,5.5)
  print

  pr_ppi("'ModernMonitor LG 22MP55HQ", 1920, 1080, 21.5) #0.248mm px-size
  pr_ppi("Samsung U28D590D", 3840, 2160, 28)
  pr_ppi("stgconn ASUS MB168B+ ", 1920,1080, 15.6)
  pr_ppi("Dell UP2414Q", 3840,2160,  23.8)
  pr_ppi("Dell Venue 8 Pro", 1280, 800, 8.0)
  print

  print "E-book reader:"
  pr_ppi("Kobo Aura eReader Wi-Fi 6\" 4Gb Black Touchscreen", 1014,758, 6.0)
  pr_ppi("Nook GlowLight (E Ink) 6\"", 1024, 758, 6.0) #http://en.wikipedia.org/wiki/Barnes_%26_Noble_Nook#Nook_GlowLight_.28E_Ink.29

main()





'''
Acer Aspire 5920  , 15.4" : 	  98.0
Apple iPhone 4S , 3.5" : 	 329.7
Samsung SyncMaster 720B , 17.0":  96.4
ONDA v975m , 9.7" : 	263.9
Samsung Galaxy Tab Pro 8.4":     359.4
Xiaomi MiPad 2014 , 7.9" : 	 324.1
Asus Fonepad Note 6 , 6.0" : 	 367.2

Monitor LG 22MP55HQ , 21.5" : 	 102.5  //yvn

Samsung U28D590D , 28.0" : 	 157.4

stgconn ASUS MB168B+  , 15.6" :  141.2
Dell UP2414Q , 23.8" : 	         185.1
Apple_Thunderbolt_Display 27"  2560x1440 pixels (QHD) 27 inches, ppi 109 
'''

def __x():  
  """Samsung Galaxy Tab Pro 8.4 LTE
Размер экрана: 	8.4
Разрешение экрана (px): 	2560 x 1600
Тип экрана: 	Super Clear LCD """

  """Xiaomi MiPad 2014 
Размер экрана: 	7.9
Разрешение экрана (px): 	1536 x 2048
Тип экрана: 	IPS
Видеоускоритель: 	192 NVIDIA CUDA® Cores 
"""  
  """ ? ONDA v975m
Размер экрана: 	9.7
Разрешение экрана (px): 	1536 x 2048
Тип экрана: 	IPS """
  
  """Asus Fonepad Note 6 
Размер экрана: 	6
Разрешение экрана (px): 	1080 x 1920
Тип экрана: 	Super IPS+ """

  """Acer Aspire 5920 
Display size 	15.4 inches
Resolution 	1280 x 800 pixels
Graphics"""

  """Apple iPhone 4S 
    Retina display
    3.5-inch (diagonal) widescreen Multi-Touch display
    960-by-640-pixel resolution at 326 ppi  #calcs give us 329 ppi
    800:1 contrast ratio (typical)"""  
  """Samsung SyncMaster 720B
   17", 1280x1024, 
    5:4, 12 MS, TN+Film, 300 CD/m2 600:1, 160°/160° """

  """LG 22MP55HQ 	
 LED monitor, 21.5" Wide 5mc Full HD IPS 	85000 dr	205USD 	Wide 0.248mm, 1920x1080@60Hz,
 contrasting 1000:1 (DCR 10M:1), brightness 250cd/m2, 5ms S-IPS matrix (great picture quality -72%), 178°/178°, 16.7mln. colors, VGA, DVI, HDMI, Audio out, 20Wt, Ultra Slim"""
  """Samsung U28D590D
цена Средняя: 7 006 грн ($ 584)
Разрешение, точек 	3840х2160  Диагональ экрана, дюймов 	28
Тип ЖК-матрицы 	TN+film  Формат 16:9   Время реакции (G-to-G), мс (1мс) """

  """ASUS MB168B+ 
Разрешение, точек 	1920х1080 Диагональ экрана, дюймов 	15,6
Тип ЖК-матрицы 	TN+Film  Формат 16:9 
Средняя цена: 3 343 грн ($ 279) """

  """Dell UP2414Q 
Разрешение, точек 	3840х2160  Диагональ экрана, дюймов 	23,8
Тип ЖК-матрицы 	IPS Формат изображения 	16:9 Время реакции (G-to-G), мс 	8 
Средняя цена: 15 350 грн ($ 1 308)
"""
  """Apple Thunderbolt Display 27"  2560x1440 pixels (QHD) 27 inches, ppi 109 
   http://en.wikipedia.org/wiki/Apple_Thunderbolt_Display
   TFT IPS active-matrix LCD, glossy glass covered screen, """

"""ASUS Google Nexus 7 (2013) 16GB (ASUS-1A051A)
 Планшет • 7" • IPS • 1920x1200 
"""
"""dell-venue-8-pro 8,0" WXGA 1280 x 800 """
"""
Ainol 7 Venus Tablet PC planshet + stexnashar (keyboard) 55000 dr Android 4.1
CPU Quad core 1.2 Ghz RAM 1Gb HDD 16Gb
Ekran IPS 1280 x 800
"""
"""Alcatel Onetouch Pop C1 (Android 4.2.2) 480x320 3.5inch 164ppi """
"""HyperTAB 7" Capacitive A23 Dual core Tablet Android 4.2 4GB Cam WIFI 800 x 480 7inch $45! """

"""
MP Mini S5 Smartphone Android 4.2 MTK6572 4.5 Inch Screen Dual SIM WIFI FM MP4
4.5 Inch
Type	TFT, capacitive touch screen
Resolution	854 x 480 pixels 
 """

""" Colorfly E708 Q1 7" Android 4.2 Quad-Core IPS Capacitive Touch Screen Tablet PC WiFi 8GB (996-03090454WT)
Display Size:  7 Inch
Display Technology: IPS Capacitive Touch Screen
Multi-Touch:  Yes, 10 Points
Display Resolution: 1280 x 800 pixels 
"Colorfly E708 Q1 7" Android 4.2 Quad-Core IPS", 1280,800,7.0
"""
"""
Kobo Aura eReader Wi-Fi 6'' 4 GB Black Touchscreen
1014x758 6inch"""
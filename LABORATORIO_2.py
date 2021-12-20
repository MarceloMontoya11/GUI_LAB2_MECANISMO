# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 15:54:13 2021

@author: GRUPO
"""


import sys
import numpy as np
import math
import pylab as pl
import random
from GUI_FINAL import*
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import QWidget,QApplication,QVBoxLayout
from PyQt5.uic import loadUi


from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


        
class MiApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.title="MECANISMO"
        
        self.ui.aplicate1_btn.clicked.connect(self.resultados)
        self.ui.aplicate2_btn.clicked.connect(self.resultados2)
        
        
        self.figure = plt.figure()
        self.dummy=3.0

        # Creacion del Objeto    
        self.graficar = FigureCanvas(self.figure)
        self.graficar2 = FigureCanvas(self.figure)
        
        # Agrega el objeto al layout de la Interfaz
        
        self.ui.grafica_uno.addWidget(self.graficar)
        self.ui.grafica_dos.addWidget(self.graficar2)
        
        self.ui.update_graf1_btn.clicked.connect(self.plot)
        self.ui.update_graf2_btn.clicked.connect(self.plot2)
    def ecuaciones(self,x):
        global matriz_y1
        x1=x[0][0]
        y1=x[0][1]
        x2=x[0][2]
        y2=x[0][3]
        
        matriz_y1=np.zeros([4,1])
        matriz_y1[0]=x1**2+y1**2-1.
        matriz_y1[1]=(x2-x1)**2+(y2-y1)**2-2.
        matriz_y1[2]=(x2-2)**2+y2**2-1.
        matriz_y1[3]=x1-1
        return matriz_y1
 
    def jacobiano(self,x):
        global matriz_j1
        x1=x[0][0]
        y1=x[0][1]
        x2=x[0][2]
        y2=x[0][3]
        matriz_j1=np.zeros([4,4])
        matriz_j1[0]=[2*x1, 2*y1, 0, 0]
        matriz_j1[1]=[-2*(x2-x1), -2*(y2-y1), 2*(x2-x1), 2*(y2-y1)]
        matriz_j1[2]=[0, 0, 2*(x2-2), 2*y2]
        matriz_j1[3]=[1, 0, 0, 0]
        return matriz_j1

    def resultados(self):
        global matriz_x1
        x1_0=self.ui.x1_0_A.text()
        y1_0=self.ui.y1_0_A.text()
        x2_0=self.ui.x2_0_A.text()
        y2_0=self.ui.y2_0_A.text()
        
        matriz_x1 =np.zeros([1,4])
        matriz_x1[0]=[x1_0,y1_0,x2_0,y2_0]
        
        for i in range(50):
            self.ecuaciones(matriz_x1)
            self.jacobiano(matriz_x1)
            
            dx=np.linalg.solve(matriz_j1,-matriz_y1)
            matriz_x1 = matriz_x1 + np.transpose(dx)
            
        self.ui.x1_A.setText(str(round(matriz_x1[0][0],3)))
        self.ui.y1_A.setText(str(round(matriz_x1[0][1],3)))
        self.ui.x2_A.setText(str(round(matriz_x1[0][2],3)))
        self.ui.y2_A.setText(str(round(matriz_x1[0][3],3)))
        #return x[0][0],x[0][1],x[0][2],x[0][3]
        
    def plot(self):
           
        self.figure.clear()
        
        m11 = (0, matriz_x1[0][0])
        n11 = (0, matriz_x1[0][1])
        m12 = (matriz_x1[0][0], matriz_x1[0][2])
        n12 = (matriz_x1[0][1], matriz_x1[0][3])
        m13 = (matriz_x1[0][2], 2)
        n13 = (matriz_x1[0][3], 0)
        m12 = (matriz_x1[0][0], matriz_x1[0][2])
        n12 = (matriz_x1[0][1], matriz_x1[0][3])
        m13 = (matriz_x1[0][2], 2)
        n13 = (matriz_x1[0][3], 0)
        
        plt.grid(True)
          
        plt.plot(m11,n11,'g-',m12,n12,'r-',m13,n13,'r-')
        self.graficar.draw()


    def ecuaciones2(self,x):
        global y
        y=np.zeros([8,1])
        y[0] = x[0][0]**2.+x[0][1]**2.-18.
        y[1] = (x[0][2]-x[0][0])**2.+(x[0][3]-x[0][1])**2.-16.
        y[2] = (x[0][2]-x[0][6])**2.+(x[0][3]-x[0][7])**2.-1.
        y[3] = (x[0][4]-x[0][6])-(2.*(x[0][2]-x[0][6]))
        y[4] = (x[0][5]-x[0][7])-(2.*(x[0][3]-x[0][7]))
        y[5] = (9-x[0][4])**2.+(6-x[0][5])**2.-8.
        y[6] = (9-x[0][6])**2.+(2-x[0][7])**2.-4.
        y[7] = x[0][1]-self.dummy
        return y
    
    def jacobiano2(self,x):
        global j
        j = np.zeros([8, 8])
        j[0] = [2.*x[0][0], 2.*x[0][1], 0, 0, 0, 0, 0, 0]
        j[1] = [-2.*(x[0][2]-x[0][0]), -2.*(x[0][3]-x[0][1]), 2.*(x[0][2]-x[0][0]), 2.*(x[0][3]-x[0][1]), 0, 0, 0, 0]
        j[2] = [0, 0, 2.*(x[0][2]-x[0][6]), 2.*(x[0][3]-x[0][7]), 0, 0,-2.*(x[0][2]-x[0][6]) , -2.*(x[0][3]-x[0][7])]
        j[3] = [0, 0, -2, 0, 1, 0, 1, 0]
        j[4] = [0, 0, 0, -2, 0, 1, 0, 1]
        j[5] = [0, 0, 0, 0, -18 + 2*(x[0][4]), -12 + 2*(x[0][5]),0,0]
        j[6] = [0, 0, 0, 0, 0, 0,-18 + 2*(x[0][6]),-4 + 2*(x[0][7])]
        j[7] = [0, 1, 0, 0, 0, 0, 0, 0]
        return j

    def resultados2(self):
        global x
        x1_0=self.ui.x1_0.text()
        y1_0=self.ui.y1_0.text()
        self.dummy=float(y1_0)
        x2_0=self.ui.x2_0.text()
        y2_0=self.ui.y2_0.text()
        x3_0=self.ui.x3_0.text()
        y3_0=self.ui.y3_0.text()
        x4_0=self.ui.x4_0.text()
        y4_0=self.ui.y4_0.text()
        
        x =np.zeros([1,8])
        x[0]=[x1_0,y1_0,x2_0,y2_0,x3_0,y3_0,x4_0,y4_0]
        
        for i in range(1000):
            y=self.ecuaciones2(x)
            j=self.jacobiano2(x)

            dx=np.linalg.solve(j,-y)
            x = x + np.transpose(dx)
            
        #print(self.x)
        self.ui.x1.setText(str(round(x[0][0],3)))
        self.ui.y1.setText(str(round(x[0][1],3)))
        self.ui.x2.setText(str(round(x[0][2],3)))
        self.ui.y2.setText(str(round(x[0][3],3)))
        self.ui.x3.setText(str(round(x[0][4],3)))
        self.ui.y3.setText(str(round(x[0][5],3)))
        self.ui.x4.setText(str(round(x[0][6],3)))
        self.ui.y4.setText(str(round(x[0][7],3)))
        return x
        
    def plot2(self):
           
        self.figure.clear()
        

        m11 = (0, x[0][0])
        n11 = (0, x[0][1])
        m12 = (x[0][0], x[0][2])
        n12 = (x[0][1], x[0][3])
        m13 = (x[0][2], x[0][4])
        n13 = (x[0][3], x[0][5])
        m14 = (x[0][2], x[0][6])
        n14 = (x[0][3], x[0][7])
        m15 = (x[0][4], 9)
        n15 = (x[0][5], 6)
        m16 = (x[0][6], 9)
        n16 = (x[0][7], 2)
        plt.plot(m11,n11,'b-',m12,n12,'r-',m13,n13,'g-',m14,n14,'y-',m15,n15,'r-',m16,n16,'g-')
        plt.grid(True)
        plt.xlim(0,10)
        plt.ylim(0,10)
        self.graficar2.draw()

        x1_0=self.ui.x1_0.text()
        y1_0=self.ui.y1_0.text()
        self.dummy=float(y1_0)
        x2_0=self.ui.x2_0.text()
        y2_0=self.ui.y2_0.text()
        x3_0=self.ui.x3_0.text()
        y3_0=self.ui.y3_0.text()
        x4_0=self.ui.x4_0.text()
        y4_0=self.ui.y4_0.text()
        
        X =np.zeros([1,8])
        X[0]=[x1_0,y1_0,x2_0,y2_0,x3_0,y3_0,x4_0,y4_0]
        print(self.dummy)

        if self.dummy==3 or self.dummy==2 or self.dummy==1:
            y1_array = np.linspace(self.dummy,0.,50)
    
            for elemento in y1_array:
                X[0][1] = elemento
                self.dummy = X[0][1]
    
                for i in range(100):
                    columna=self.ecuaciones2(X)
                    jacobiano=self.jacobiano2(X)
    
                    dx=np.linalg.solve(jacobiano,-columna)
    
                    X = X + np.transpose(dx)
                plt.grid(True)
                plt.xlim(0,10)
                plt.ylim(0,10)   
                plt.plot(X[0][0],X[0][1], '.')
                plt.plot(X[0][2],X[0][3], '.')
                plt.plot(X[0][4],X[0][5], '.')
                plt.plot(X[0][6],X[0][7], '.')
                
                self.graficar2.draw()

          
                   
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec_())
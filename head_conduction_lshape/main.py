import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math as m

class Esq:
	def __init__(self, a1, a2, b1, b2):
		self.a1 = a1
		self.a2 = a2
		self.b1 = b1
		self.b2 = b2

def gfunc(ag):
	return lambda x1,x2: ag*m.sqrt(x1**2+x2**2)

ficflex = [
	lambda x1, x2: (1 - x1)*(1 - x2),
	lambda x1, x2: x1*(1 - x2),
	lambda x1, x2: x1*x2,
	lambda x1, x2: (1 - x1)*x2
]

def fi(i,e,x1,x2):
	if(x1<e.b1 or x1 > 1 + e.b1):
		return 0
	if(x2<e.b2 or x2 > 1 + e.b2): 
		return 0
	return ficflex[i-1]((x1-e.b1)/e.a1,(x2-e.b2)/e.a2)

def df_jdx_i(e,j,i):
	dfi = [
		[-1/e.a1,1/e.a1,1/e.a1,-1/e.a1],
		[-1/e.a2,-1/e.a2,1/e.a2,1/e.a2]
	]
	return dfi[i-1][j-1]
	
def b_ij(e,i,j):
	res = 0
	for ix in range(1,3):
		res += df_jdx_i(e,i,ix)*df_jdx_i(e,j,ix)
	return e.a1*e.a2*res

def b_ui(e,i,j,u0):
	res = 0
	for ix in range(1,3):
		res += df_jdx_i(e,i,ix)*df_jdx_i(e,j,ix)
	return e.a1*e.a2*res*u0

def onNeumann(p1,p2):
	return p1 != (0,0) and p2 != (0,0)

def l_i(e,g,i):
	points = [(0,0),(1,0),(1,1),(0,1)]
	res = 0
	for j in range(0,len(points)):
		p1 = points[j]
		p2 = points[(j+1)%len(points)]
		p1 = (p1[0] + e.b1, p1[1] + e.b2)
		p2 = (p2[0] + e.b1, p2[1] + e.b2)
		if(onNeumann(p1,p2)):
			ps = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
			res += g(ps[0], ps[1])*fi(i,e,ps[0],ps[1])*( e.a2 if p1[0]==p2[0] else e.a1)
	return res
	
def gauss(A,Y):
	B = []
	for i in range(0, len(A)):
		tmp = []
		for j in range(0, len(A[i])):
			tmp.append(A[i][j])
		tmp.append(Y[i])
		B.append(tmp)
			
	for i in range(0,len(B)):
		for j in range(i+1,len(B)):
			if(B[j][i]>B[i][i]):
				B[j],B[i]=B[i],B[j]
		a = B[i][i]
		if(a!=0):
			for j in range(i+1,len(B)):
				coef = B[j][i]/a
				for k in range(i,len(B[j])):
					B[j][k]-=B[i][k]*coef
	X = []
	for i in reversed(range(0,len(B))):
		tmp = B[i][-1]
		for j in reversed(range(i+1,len(B[i])-1)):
			tmp -= B[i][j]*X[len(B[i])-j-2]
		X.append(tmp/B[i][i])	
	X.reverse()	
	return X			

E = [Esq(1,1,-1,0),Esq(1,1,0,0),Esq(1,1,0,-1)]
ag = float(input())
u0 = float(input())
g = gfunc(ag)

fiToe = [
	[3,4,1,0],
	[4,5,2,1],
	[6,7,5,4]
]

B = [[0 for i in range(0,8)] for j in range(0,8)]
L = [0 for i in range(0,8)]
for k in range(0,len(E)):
	for i in range(1,5):
		i1 = fiToe[k][i-1]
		L[i1] += l_i(E[k], g, i) 
		for j in range(1,5):
			if(i==1 or (k==0 and i ==2) or (k==2 and i==4)):
				L[i1] -= b_ui(E[k], j, i, u0)
			j1 = fiToe[k][j-1]
			B[i1][j1] += b_ij(E[k],i,j)	
			
for j in range(0, 8):
	B[3][j]=0
	B[4][j]=0
	B[6][j]=0
L[3]=0
L[4]=0
L[6]=0
B[3][3]=1
B[4][4]=1 
B[6][6]=1 		
X = gauss(B,L)
def u (x1,x2): 
	if(x1<0 and x2<0):
		return u0
	res = 0
	for i in range(0,3):
		for j in range(0,4):
			res += X[fiToe[i][j]]*fi(j+1,E[i],x1,x2)
	return max(res,0) + u0
x = np.arange(-1,1,0.01)
y = np.arange(-1,1,0.01)
xs, ys = np.meshgrid(x,y)
print(u(0.5,-0.5), u(-0.5, 0.5))
#z = np.array([[ u(x[i],y[j]) for j in range(0,len(y))] for i in range(0,len(x))])
zs = np.array([max(u(x,y),0) for x,y in zip(np.ravel(xs), np.ravel(ys))])
zs = zs.reshape(xs.shape)
#plt.pcolormesh(xs,ys,z,cmap=plt.cm.hot)
#plt.show()
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(xs,ys,zs)	
plt.show()	

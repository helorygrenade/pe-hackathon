import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from xcover import covers_bool as xc



RAW_SHAPES = {
    "F": np.array([[1, 1, 0], [0, 1, 1], [0, 1, 0]]),
    "I": np.array([[1, 1, 1, 1, 1]]),
    "L": np.array([[1, 0, 0, 0], [1, 1, 1, 1]]),
    "N": np.array([[1, 1, 0, 0], [0, 1, 1, 1]]),
    "P": np.array([[1, 1, 1], [1, 1, 0]]),
    "T": np.array([[1, 1, 1], [0, 1, 0], [0, 1, 0]]),
    "U": np.array([[1, 1, 1], [1, 0, 1]]),
    "V": np.array([[1, 1, 1], [1, 0, 0], [1, 0, 0]]),
    "W": np.array([[1, 0, 0], [1, 1, 0], [0, 1, 1]]),
    "X": np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
    "Y": np.array([[0, 1, 0, 0], [1, 1, 1, 1]]),
    "Z": np.array([[1, 1, 0], [0, 1, 0], [0, 1, 1]]),
}

PENTOMINOS = [np.array(shape) for shape in RAW_SHAPES.values()]


# 0 means the spot is free; 1 means its not in the shape to fill

# rectangles
BOARD_3_20 = np.zeros((3, 20))
BOARD_4_15 = np.zeros((4, 15))
BOARD_5_12 = np.zeros((5, 12))
BOARD_6_10 = np.zeros((6, 10))

# 8x8 with a 2x2 hole in the middle
BOARD_8_8 = np.zeros((8, 8))
BOARD_8_8[3:5, 3:5] = 1

# 2 separate 3x10 rectangles
# has no solution
NO_BOARD_2_3_10 = np.zeros((3, 21))
NO_BOARD_2_3_10[:, 10] = 1

# 2 separate 5x6 rectangles
BOARD_2_5_6 = np.zeros((5, 13))
BOARD_2_5_6[:, 6] = 1

# 3 separate 4x5 rectangles
# has no solution
NO_BOARD_3_4_5 = np.zeros((3, 23))
NO_BOARD_3_4_5[:, 5:6] = 1

BOARD_8_9 = np.zeros((8, 9))
BOARD_8_9[::7, ::8] = 1
BOARD_8_9[1::5, ::8] = 1
BOARD_8_9[::7, 1::6] = 1


SMALL_BOARD = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 0]])
SMALL_PIECE = np.array([[0, 1], [1, 1]])

#création des fonctions utiles

def rotation(piece):
    p,q=piece.shape
    rot=np.zeros((q,p))
    for i in range(q):
        for j in range(p):
            rot[i,j]=piece[j,p-i]
    return rot
rotation(RAW_SHAPES["I"])

def symetrie(piece):
    p,q=piece.shape
    sym=np.zeros((p,q))
    for i in range(p):
        for j in range(q):
            sym[i,j]=piece[i,q-j-1]
    return sym

symetrie(rotation(RAW_SHAPES["I"]))

def is_array_in_list(array, list_of_arrays):
    return any(np.array_equal(array, arr) for arr in list_of_arrays)

def variantes(piece):
    l=[]
    tab=piece
    for _ in range(2):
        for _ in range(4):
            if not is_array_in_list(tab,l):
                l.append(tab)
            tab=np.rot90(tab)
        tab=symetrie(tab)
    return l
variantes(RAW_SHAPES["I"])

#création des listes de vecteurs
l=[]
board=BOARD_6_10
index=0
for piece in RAW_SHAPES.values():
    m,n=board.shape
    num=np.zeros((12),dtype=np.uint8)
    num[index]=1
    for tab in variantes(piece):
        p,q=tab.shape
        for i in range(m-p):
            for j in range(n-q):
                sol=np.zeros((m,n), dtype=np.uint8)
                sol[i:i+p,j:j+q]=tab
                sol=sol.reshape(60)
                l.append(np.concatenate((num,sol),axis=None))
    index+=1

def first_true (l) :
    b = False
    i = 0
    while not b :
        b = l[i]
        i+= 1
    return i

def liste_true (l) :
    res = []
    for i in range (60) :
        if l[i] :
            res.append(i)
    return res
l=np.array(l)
l=l[l==1]
def blah (m) :
    u = next(xc(m))
    res = [0]*60
    for elt in u :
        l = m[elt]
        k = first_true (l)
        pos = liste_true (l[12:])
        for i in range (len(pos)) :
            res[pos[i]] = k
    return res

def format (L, c, l):
    ser = []
    for k in range (l) :
        ser.append (L[k*c : (k+1)*c])
    return ser




#Quand on a la solution
solution = np.array(format(blah(l),10,6))

cmap = plt.get_cmap('inferno', 12)
print(solution.shape)
plt.imshow(solution, cmap=cmap, vmin=1, vmax=12)
plt.show()
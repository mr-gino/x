import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF

# =========================
# ===== ZADANIE 1 =========
# =========================

# STAŁE
a = 2
b = 4
c = 0
d = 1

# PARAMETRY
N = 10000
t_ls = np.linspace(0, 10, 200)

# (b) U posiada rozkład Poissona o intensywności (1 + a // 2);
U = npr.poisson(1 + a//2, N)

# (d) V posiadaja jednorodny rozkład na przedziałe [0, b];
V = npr.uniform(0, b, N)

# --- proces ---
def X_t(t):
    return c * t * U + d * V

# --- E(Xt), Var(Xt), P(...) ---
E_vals = []
Var_vals = []
P_vals = []

for t in t_ls:
    X = X_t(t)
    E_vals.append(np.mean(X))
    Var_vals.append(np.var(X))

    dol = min(5*a*c, b*d)/2
    gora = max(5*a*c, b*d)/2

    P_vals.append(np.mean((X > dol) & (X < gora)))

# --- wykresy ---
plt.plot(t_ls, E_vals, label='E(Xt)')
plt.plot(t_ls, Var_vals, label='Var(Xt)')
plt.plot(t_ls, P_vals, label='P(...)')
plt.legend()
plt.title("Zadanie 1")
plt.show()

# --- kowariancja K(t,s) ---
def K(t, s):
    X1 = X_t(t)
    X2 = X_t(s)
    return np.mean(X1 * X2) - np.mean(X1)*np.mean(X2)

print("K(2,5) =", K(2,5))

# g) X(t) = ct E(U) + dV;
EU = np.mean(U)

def Xg(t):
    return c*t*EU + d*V

# dystrybuanta 1D
X_sample = Xg(5)
ecdf = ECDF(X_sample)
plt.plot(ecdf.x, ecdf.y)
plt.title("Dystrybuanta 1D")
plt.show()

# =========================
# ===== ZADANIE 2 =========
# =========================

# PARAMETRY (tabelka 7)
lam = 4
mu = 4

a = 3
b = 3
c = 0
d = 2
e = 1
f = 4
g = 4
i = 1
j = 5
h = 3
k = 3
m = 4
n = 1
p = 3
q = 4

# --- procesy Poissona ---
def X(t):
    return npr.poisson(lam * t)

def Y(t):
    return npr.poisson(mu * t)

def Z(t):
    return X(t) + 2*Y(t)

# --- (a) intensywność ---
print("Intensywność Z:", lam + 2*mu)

# --- (c) P(Xe = g | Ze = f) ---
prob = 0
proby = 100000

licz = 0
war = 0

for _ in range(proby):
    Xt = npr.poisson(lam*e)
    Yt = npr.poisson(mu*e)
    Zt = Xt + 2*Yt

    if Zt == f:
        war += 1
        if Xt == g:
            licz += 1

if war > 0:
    print("P(Xe=g | Ze=f) =", licz/war)

# --- (d) P(Zn+1 = q | Xn = p) ---
licz = 0
war = 0

for _ in range(proby):
    Xn = npr.poisson(lam*n)
    Yn = npr.poisson(mu*n)

    if Xn == p:
        war += 1
        Xn1 = Xn + npr.poisson(lam)
        Yn1 = Yn + npr.poisson(mu)
        Zn1 = Xn1 + 2*Yn1

        if Zn1 == q:
            licz += 1

if war > 0:
    print("P(Zn+1=q | Xn=p) =", licz/war)

# --- (f) P(Zh = k oraz Zj - Zi = m) ---
licz = 0

for _ in range(proby):
    Zh = Z(h)
    Zi = Z(i)
    Zj = Z(j)

    if Zh == k and (Zj - Zi) == m:
        licz += 1

print("P(Zh=k i Zj-Zi=m) =", licz/proby)

# --- (i) Wiener ---
# Wt ~ N(0,t)

licz = 0

for _ in range(proby):
    Zi = npr.normal(0, np.sqrt(i))
    Zj = npr.normal(0, np.sqrt(j))

    if abs(Zj - Zi - m) < 0.1:  # przybliżenie
        licz += 1

print("Wiener approx =", licz/proby)
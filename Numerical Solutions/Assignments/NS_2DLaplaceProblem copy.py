import math

# parameters
dx = 0.01
dy = 0.01
NX = 2
NY = 1
nx = int(NX/dx)
ny = int(NY/dy)
tol = 0.0001
it = 0
pi = 3.141592653589793
uold = [[None] * int(nx + 1)] * int(nx + 1)
unew = [[None] * int(nx + 1)] * int(nx + 1)
error = [[None] * int(nx + 1)] * int(nx + 1)

# boundary conditions
for i in range(0, nx+1):
  uold[i][0] = 0.0
  unew[i][0] = 0.0
for i in range(0, nx+1):
  uold[i][ny] = 0.0
  unew[i][ny] = 0.0
for j in range(0, ny):
  uold[0][j] = math.sin(pi*(dy*j))
  unew[0][j] = math.sin(pi*(dy*j))
for j in range(0, ny):
  uold[nx][j] = math.exp(2)*math.sin(pi*(dy*j))
  unew[nx][j] = math.exp(2)*math.sin(pi*(dy*j))

# Results
def Output():
  outputFile = open("outputFile2.txt", "w")
  for i in range(0, nx+1):
    for j in range(0, ny+1):
      outputFile.write("{}\t{}\n".format(i*dx, unew[50][i]))
    outputFile.write("{}\t{}\t{}\n".format(i*dx, j*dy, unew[i][j]))

while(True):
  # Jacobi Iteration
  for i in range(1, nx):
    for j in range(1, ny):
      unew[i][j] = 0.25*(uold[i-1][j]+uold[i+1][j]+uold[i][j-1]+uold[i][j+1]) + ((dx**2)/4)*(pi**2 - 1)*math.exp((dx*i))*math.sin(pi*(dy*j))
  
  # Gauss-Seidel Iteration
  # for i in range(1, nx):
  #   for j in range(1, ny):
  #     unew[i][j] = 0.25*(unew[i-1][j]+uold[i+1][j]+unew[i][j-1]+uold[i][j+1]) + ((dx**2)/4)*(pi**2 - 1)*math.exp((dx*i))*math.sin(pi*(dy*j))

  # Check Convergence
  for i in range(1, nx):
    for j in range(1, ny):
      error[i][j] = abs(unew[i][j] - uold[i][j])
  
  errmax = 0.0
  for i in range(1, nx):
    for j in range(1, ny):
      if (error[i][j] > errmax):
        errmax = error[i][j]
  
  if (errmax <= tol):
    Output()
    break

  for i in range(0, nx+1):
    for j in range(0, ny+1):
      uold[i][j] = unew[i][j]
  
  print("it = {}\terrmax = {}".format(it, errmax))
  it += 1

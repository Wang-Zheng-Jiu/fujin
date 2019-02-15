import travel_tools
from math import acos, cos, sin, ceil, sqrt, atan2
import numpy as np
import itertools
import time

def getNeighbors(i, m, n, env, obstacleFlag = 1):


    B = []

    upAllowed        = False
    downAllowed      = False
    leftAllowed      = False
    rightAllowed     = False
    upleftAllowed    = False
    uprightAllowed   = False
    downleftAllowed  = False
    downrightAllowed = False

    # Up
    if(i[0] - 1 >= 0):
        if(env[i[0] - 1][i[1]] != obstacleFlag):
            upAllowed = True
            B.append((i[0] - 1, i[1], "^"))
    # Down
    if(i[0] + 1 < m):
        if(env[i[0] + 1][i[1]] != obstacleFlag):
            downAllowed = True
            B.append((i[0] + 1, i[1], "v"))
    # Left
    if(i[1] - 1 >= 0):
        if(env[i[0]][i[1] - 1] != obstacleFlag):
            leftAllowed = True
            B.append((i[0], i[1] - 1, "<"))
    # Right
    if(i[1] + 1 < n):
        if(env[i[0]][i[1] + 1] != obstacleFlag):
            rightAllowed = True
            B.append((i[0], i[1] + 1, ">"))
    # Up-Left
    if(i[0] - 1 >= 0 and i[1] - 1 >= 0):
        if(env[i[0] - 1][i[1] - 1] != obstacleFlag):
            upleftAllowed = True
            B.append((i[0] - 1, i[1] - 1, "a"))
    # Up-Right
    if(i[0] - 1 >= 0 and i[1] + 1 < n):
        if(env[i[0] - 1][i[1] + 1] != obstacleFlag):
            uprightAllowed = True
            B.append((i[0] - 1, i[1] + 1, "b"))
    # Down-Left
    if(i[0] + 1 < m and i[1] - 1 >= 0):
        if(env[i[0] + 1][i[1] - 1] != obstacleFlag):
            downleftAllowed = True
            B.append((i[0] + 1, i[1] - 1, "c"))
    # Down-Right
    if(i[0] + 1 < m and i[1] + 1 < n):
        if(env[i[0] + 1][i[1] + 1] != obstacleFlag):
            downrightAllowed = True
            B.append((i[0] + 1, i[1] + 1, "d"))
    # Up-Up-Left
    if(i[0] - 2 >= 0 and i[1] - 1 >= 0 and upAllowed and upleftAllowed and leftAllowed):
        if(env[i[0] - 2][i[1] - 1] != obstacleFlag):
            B.append((i[0] - 2, i[1] - 1, "m"))
    # Up-Up-Right
    if(i[0] - 2 >= 0 and i[1] + 1 < n and upAllowed and uprightAllowed and rightAllowed):
        if(env[i[0] - 2][i[1] + 1] != obstacleFlag):
            B.append((i[0] - 2, i[1] + 1, "n"))
    # Up-Left-Left
    if(i[0] - 1 >= 0 and i[1] - 2 >= 0 and upAllowed and upleftAllowed and leftAllowed):
        if(env[i[0] - 1][i[1] - 2] != obstacleFlag):
            B.append((i[0] - 1, i[1] - 2, "o"))
    # Up-Right-Right
    if(i[0] - 1 >= 0 and i[1] + 2 < n and upAllowed and uprightAllowed and rightAllowed):
        if(env[i[0] - 1][i[1] + 2] != obstacleFlag):
            B.append((i[0] - 1, i[1] + 2, "p"))
    # Down-Down-Left
    if(i[0] + 2 < m and i[1] - 1 >= 0 and downAllowed and downleftAllowed and leftAllowed):
        if(env[i[0] + 2][i[1] - 1] != obstacleFlag):
            B.append((i[0] + 2, i[1] - 1, "w"))
    # Down-Down-Right
    if(i[0] + 2 < m and i[1] + 1 < n and downAllowed and downrightAllowed and rightAllowed):
        if(env[i[0] + 2][i[1] + 1] != obstacleFlag):
            B.append((i[0] + 2, i[1] + 1, "x"))
    # Down-Left-Left
    if(i[0] + 1 < m and i[1] - 2 >= 0 and downAllowed and downleftAllowed and leftAllowed):
        if(env[i[0] + 1][i[1] - 2] != obstacleFlag):
            B.append((i[0] + 1, i[1] - 2, "y"))
    # Down-Right-Right
    if(i[0] + 1 < m and i[1] + 2 < n and downAllowed and downrightAllowed and rightAllowed):
        if(env[i[0] + 1][i[1] + 2] != obstacleFlag):
            B.append((i[0] + 1, i[1] + 2, "z"))
    return B


def getWorldActionsForCell(row, col, ugrids, vgrids, errors):

    numVectors = len(ugrids)

    uranges = [None for i in range(numVectors)]
    vranges = [None for i in range(numVectors)]

    numActions = 1

    for g in range(numVectors):
        uranges[g] = np.linspace(ugrids[g][row][col] - errors[g], ugrids[g][row][col] + errors[g], 10)
        vranges[g] = np.linspace(vgrids[g][row][col] - errors[g], vgrids[g][row][col] + errors[g], 10)
        numActions = numActions * len(uranges[g])

    uactionspace = list(itertools.product(*uranges))
    vactionspace = list(itertools.product(*vranges))

    world_actionspace = { "uactions"   : uactionspace,
                          "vactions"   : uactionspace,
                          "num"        : numActions,
                        }

    return world_actionspace



def getVectorSum(us, vs, weights):
    utotal = 0
    vtotal = 0

    numVectors = len(us)

    for i in range(numVectors):
        utotal = utotal + weights[i] * us[i]
        vtotal = vtotal + weights[i] * vs[i]

    return (utotal, vtotal)


def getVectorDiff(us, vs, weights):
    utotal = 0
    vtotal = 0

    numVectors = len(us)

    for i in range(numVectors):
        utotal = utotal - weights[i] * us[i]
        vtotal = vtotal - weights[i] * vs[i]

    return utotal, vtotal


def magdir2uv(mag, dir_radians):
    u = mag * cos(dir_radians)
    v = mag * sin(dir_radians)
    return u, v

def uv2magdir(u, v):
    m = sqrt(u * u + v * v)
    d = atan2(v, u)
    return m, d

def getOutcome(move, us, vs, weights, traveler, D_max,
        cost2go = None, row = None, col = None):


    # Get resultant vector of all weighted world sources
    uw, vw = getVectorSum(us, vs, weights)

    # Break traveler magnitude, direction into vector
    ut, vt = magdir2uv(traveler["speed_cps"], traveler["action2radians"][move])

    # Get vector difference (required applied force)
    ua, va = getVectorDiff([uw, ut], [vw, vt], [1, 1])

    # Combine applied u, v to get mag, dir
    maga, dira = uv2magdir(ua, va)

    # Calculate work
    work = maga  # Proportional to magnitude the speed is 'per cell'
    workc = work
    # Dynamic programming: include cost2go
    if cost2go is not None and row is not None and col is not None:

        m = len(cost2go)
        n = len(cost2go[0])

        if move == "^":
        #    if row > 0:
            workc = work + cost2go[row - 1][col]
        #    else:
        #        workc = work + d_max
        elif move == "v":
        #    if row < len(cost2go) - 1:
            workc = work + cost2go[row + 1][col]
        #    else:
        #        workc = work + d_max
        elif move == "<":
        #    if col > 0:
            workc = work + cost2go[row][col - 1]
        #    else:
        #        workc = work + d_max
        elif move == ">":
        #    if col < len(cost2go[0]) - 1:
            workc = work + cost2go[row][col + 1]
        #    else:
        #        workc = work + d_max
        elif move == "a":
        #    if row - 1 >= 0 and col - 1 >= 0:
            workc = work + cost2go[row - 1][col - 1]
        #    else:
        #        workc = work + d_max
        elif move == "b":
        #    if row - 1 >= 0 and col + 1 < n:
            workc = work + cost2go[row - 1][col + 1]
        #    else:
        #        workc = work + d_max
        elif move == "c":
        #    if row + 1 < m and col - 1 >= 0:
            workc = work + cost2go[row + 1][col - 1]
        #    else:
        #        workc = work + d_max
        elif move == "d":
        #    if row + 1 < m and col + 1 < n:
            workc = work + cost2go[row + 1][col + 1]
        #    else:
        #        workc = work + d_max
        elif move == "m":
        #    if (row - 2 >= 0 and col - 1 >= 0) and \
        #           (col - 1 >= 0) and (row - 1 >= 0) and \
        #           (row - 1 >= 0 and col - 1 >= 0):
            workc = work + cost2go[row - 2][col - 1]
        #    else:
        #        workc = work + d_max
        elif move == "n":
        #    if (row - 2 >= 0 and col + 1 < n) and \
        #           (row - 1 >= 0) and (col + 1 < n) and \
        #           (row - 1 >= 0 and col + 1 < n):
            workc = work + cost2go[row - 2][col + 1]
        #    else:
        #        workc = work + d_max
        elif move == "o":
        #    if (row - 1 >= 0 and col - 2 >= 0) and \
        #           (row - 1 >= 0) and (col - 1 >= 0) and \
        #           (row - 1 >= 0 and col - 1 >= 0):
            workc = work + cost2go[row - 1][col - 2]
        #    else:
        #        workc = work + d_max
        elif move == "p":
        #    if (row - 1 >= 0 and col + 2 < n) and \
        #           (row - 1 >= 0) and (col + 1 < n) and \
        #           (row - 1 >= 0 and col + 1 < n):
            workc = work + cost2go[row - 1][col + 2]
        #    else:
        #        workc = work + d_max
        elif move == "w":
        #    if (row + 2 < m and col - 1 >= 0) and \
        #           (row + 1 < m) and (col - 1 >= 0) and \
        #           (row + 1 < m and col - 1 >= 0):
            workc = work + cost2go[row + 2][col - 1]
        #    else:
        #        workc = work + d_max
        elif move == "x":
        #    if (row + 2 < m and col + 1 < n) and \
        #           (row + 1 < m) and (col + 1 < n) and \
        #           (row + 1 < m and col + 1 < n):
            workc = work + cost2go[row + 2][col + 1]
        #    else:
        #        workc = work + d_max
        elif move == "y":
        #    if (row + 1 < m and col - 2 >= 0) and \
        #           (row + 1 < m) and (col - 1 >= 0) and \
        #           (row + 1 < m and col - 1 >= 0):
            workc = work + cost2go[row + 1][col - 2]
        #    else:
        #        workc = work + d_max
        elif move == "z":
        #    if (row + 1 < m and col + 2 < n) and \
        #           (row + 1 < m) and (col + 1 < n) and \
        #           (row + 1 < m and col + 1 < n):
             workc = work + cost2go[row + 1][col + 2]
        #    else:
        #        workc = work + d_max
        elif move == "*":
                workc = d_max

        else:
            print("Invalid move")


    return workc, work

def getGameForCell(row, col, traveler, ugrids, vgrids, errors, weights, env, D_max, cost2go = None):
    world_actionspace = getWorldActionsForCell(row, col, ugrids, vgrids, errors)

    game = [[0 for wa in range(world_actionspace["num"])] for ta in traveler["actionspace"]]
    game_work = [[0 for wa in range(world_actionspace["num"])] for ta in traveler["actionspace"]]

    B = getNeighbors((row, col), env.shape[0], env.shape[1], env)
    Bmove = [b[2] for b in B]
    if(row == 532 and col == 327):
        print(Bmove)

    for r in range(len(game)):
        Bvalid = False
        #print(Bmove, traveler["actionspace"][r])
        if traveler["actionspace"][r] in Bmove:
            Bvalid = True
        for c in range(len(game[0])):
            if Bvalid:
                if(row == 532 and col == 327):
                    print(traveler["actionspace"][r])
                game[r][c], game_work[r][c] = getOutcome(traveler["actionspace"][r],
                        world_actionspace["uactions"][c], world_actionspace["vactions"][c],
                        weights, traveler, D_max, cost2go, row, col)
            else: # If invalid move, do not bother with work
                game[r][c], game_work[r][c] = D_max, D_max


    if(row == 532 and col == 327):
        for rr in range(len(game)):
            print (rr, game[rr])

    game      = np.array(game)
    game_work = np.array(game_work)
    return game, game_work


def solve_williams(payoff_matrix, iterations=100):
    '''
    Source: http://code.activestate.com/recipes/496825-game-theory-payoff-matrix-solver/

    Approximate the strategy oddments for 2 person zero-sum games of perfect information.

    Applies the iterative solution method described by J.D. Williams in his classic
    book, The Complete Strategyst, ISBN 0-486-25101-2.   See chapter 5, page 180 for details.
    '''

    payoff_matrix = (-1) * payoff_matrix

    from operator import add, neg
    'Return the oddments (mixed strategy ratios) for a given payoff matrix'
    transpose = zip(*payoff_matrix)
    numrows = len(payoff_matrix)
    numcols = len(transpose)
    row_cum_payoff = [0] * numrows
    col_cum_payoff = [0] * numcols
    colpos = range(numcols)
    rowpos = map(neg, xrange(numrows))
    colcnt = [0] * numcols
    rowcnt = [0] * numrows
    active = 0
    for i in xrange(iterations):
        rowcnt[active] += 1
        col_cum_payoff = map(add, payoff_matrix[active], col_cum_payoff)
        active = min(zip(col_cum_payoff, colpos))[1]
        colcnt[active] += 1
        row_cum_payoff = map(add, transpose[active], row_cum_payoff)
        active = -max(zip(row_cum_payoff, rowpos))[1]
    value_of_game = (max(row_cum_payoff) + min(col_cum_payoff)) / 2.0 / iterations
    return np.array(rowcnt).astype(float) / iterations, np.array(colcnt).astype(float) / iterations

def solve_gambit(game):
    import gambit

    #game = (-1) * np.array([ [10, 0], [0, 0] ])
    game = game

    m = game.shape[0]
    n = game.shape[1]

    g = gambit.Game.new_table([m, n])
    g.title = "solve cell"
    g.players[0].label = "traveler"
    g.players[1].label = "fujin"

    # Populate game
    for row in range(m):
        for col in range(n):
            g[row, col][0] = int(game[row][col] * 1000)
            g[row, col][1] = (-1) * int(game[row][col] * 1000)

    solver = gambit.nash.ExternalEnumMixedSolver()
    solution = solver.solve(g)
    solution = np.asarray(solution[0])
    y = solution[0:m]
    z = solution[m:m+n]
    return y, z

def solve_nashpy(game):
    import nashpy as nash

    rps = nash.Game(game)
    eqs = list(rps.support_enumeration())

    y = eqs[0]
    z = eqs[1]

    return y, z

def solveGame(game, method = 0):

    '''
       methods
       ------------
       0 : williams
       1 : gambit
       2 : nashpy
    '''

    if   method == 0:
        y, z = solve_williams(game)
    elif method == 1:
        y, z = solve_gambit(game)
    elif method == 2:
        y, z = solve_nashpy(game)

    # Convert to pure policy
    i = np.argmax(y)
    j = np.argmax(z)
    v = game[i][j]

    return (y, z, i, j, v)


def printGame(game):
    for row in range(len(game)):
        for col in range(len(game[0])):
            print("{0:.2f}".format(game[row][col])),
        print ("")

def printSolution(solution, name = ""):
    print("Nash Solution " + name)
    print("Player 1:" )
    print("    Pure security policy: {}".format(solution[2]))
    print("    Security policy: ")
    print("    "),
    for num in solution[0]:
        print("{} ".format(num)),
    print("")
    print("Player 2:" )
    print("    Pure security policy: {}".format(solution[3]))
    print("    Security policy: ")
    print("    "),
    for num in solution[1]:
        print("{} ".format(num)),
    print("")
    print("Security level: {}".format(solution[4]))


def getCost2go(traveler, occgrid, ugrids, vgrids, egrids, wgrids,
        bounds = None, verbose = False, iterations = None, method = 0):

    # Destination position
    G = (traveler["target"][0], traveler["target"][1])

    # Environment size
    full_m, full_n = occgrid.shape
    m = abs(bounds["lowerright"][0] - bounds["upperleft"][0])
    n = abs(bounds["lowerright"][1] - bounds["upperleft"][1])
    M = m * n # Num cells

    # Minimum distance between neighbors
    d_min = 0
    # Maximum distance between neighbors
    d_max = sqrt(2) * 10 # Put 1000 but unsure max work
    # Maximum cost
    D_max = M * d_max * 100000000000 * 10000000000  # D_max must be > (M - 1) * d_max

    if iterations == None:
        iterations = M

    # Get neighbors
    # Distance between location i and j
    def distance(i, j):
        dist = pow((pow(i[0] - j[0], 2) + pow(i[1] - j[1], 2)), 0.5)
        return dist

    def f(i, m, n, cost2go, D_max, env):
        B = getNeighbors(i, m, n, env)

        cost_min = D_max
        b_min = (None, None, "-")
        for b in B:
            cost = distance(i, b) + cost2go[b[0]][b[1]]
            if cost < cost_min:
                cost_min = cost
                b_min = b

        return cost_min, b_min

    def f_work(i, m, n, cost2go, D_max, env,
            traveler, ugrids, vgrids, egrids, wgrids,
            method):
        errors = [e[row][col] for e in egrids]
        weights = [w[row][col] for w in wgrids]
        g, g_work = getGameForCell(i[0], i[1], traveler, ugrids, vgrids,
                                             errors, weights, env, D_max, cost2go)

        solution             = solveGame(g, method)


        if(i[0] == 532 and i[1] == 327):
            print(solution, traveler["actionspace"][solution[2]])

        #cost2go[row][col]    = solution[4]
        #work2go[row][col]    = g_work[solution[2], solution[3]]
        #actiongrid[row][col] = traveler["actionspace"][solution[2]]
        return (solution[4], traveler["actionspace"][solution[2]])


    def getNewCost(i, G, occgrid, m, n, cost2go, D_max,
            traveler, ugrids, vgrids, egrids, wgrids):
        cost = D_max
        action = " "

        # Check if target location
        if i == G:
            cost = 0
            action = "*"

        # Check if obstacle
        elif occgrid[i[0]][i[1]] == 1:
            cost = D_max

        # Check if surrounded by D_max
        elif    cost2go[i[0] - 1][i[1]] == D_max and cost2go[i[0] - 1][i[1] - 1] == D_max and \
                cost2go[i[0] - 1][i[1]] == D_max and cost2go[i[0] - 1][i[1] + 1] == D_max and \
                cost2go[i[0]][i[1] - 1] == D_max and cost2go[i[0] + 1][i[1] - 1] == D_max and \
                cost2go[i[0]][i[1] + 1] == D_max and cost2go[i[0] + 1][i[1] + 1] == D_max:
            cost = D_max
            action = "-"

        # Else, calculate cost normally
        else:
            c, b = f_work(i, occgrid.shape[0], occgrid.shape[1], cost2go, D_max,
                    occgrid, traveler, ugrids, vgrids, egrids, wgrids, 0)
            if c >= D_max:
                cost = D_max
                action = '-'
            else:
                cost = c
                action = b

        return cost, action

    cost2go = np.zeros((full_m, full_n)) + D_max
    work2go = np.zeros((full_m, full_n))
    action2go = np.array([["-" for col in range(full_n)] for row in range(full_m)])
    history = None

    for k in range(iterations):

        # Queue of locations to evaluate
        visitQueue = [G]
        # Queue history
        visitHistory = set()
        # Bound on number of locations can solve per iteration
        maxCount = 100000;
        # Loop counter
        count = 0

        import time
        while visitQueue: # and count < maxCount:
                #t0outer = time.time()
                count = count + 1
                #print (count)
                i = visitQueue.pop(0)
                # Assign cost2go at i
                #t0inner = time.time()
                cost2go[i[0]][i[1]], action2go[i[0]][i[1]] = \
                    getNewCost(i, G, occgrid, m, n, cost2go, D_max,
                            traveler, ugrids, vgrids, egrids, wgrids)
                #t1inner = time.time()
                # Add i's neighbors to list
                B = getNeighbors(i, occgrid.shape[0], occgrid.shape[1], occgrid)
                for b in B:
                    b = (b[0], b[1])

                    if     b[0] > bounds["upperleft"][0] and b[0] < bounds["lowerright"][0] and \
                           b[1] > bounds["upperleft"][1] and b[1] < bounds["lowerright"][1]:
                        if b not in visitHistory:
                            visitQueue.append(b)
                            visitHistory.add(b)
                #t1outer = time.time()
                #print("Full time", t1outer - t0outer, "new cost time", t1inner - t0inner)

        print("Iteration: " + str(k) + "/" + str(iterations))

    return cost2go, work2go, action2go, history

def writeActiongrid(actiongrid, actionfile, bounds = None):
    numrows = len(actiongrid)
    numcols = len(actiongrid[0])

    if bounds == None:
        bounds = { "upperleft"  : (0, 0),
                   "lowerright" : (actiongrid.shape[0], actiongrid.shape[1]),
                 }

    af = open(actionfile, 'w')
    for row in range(numrows):
        for col in range(numcols):
            af.write("%s" % actiongrid[row][col])
        af.write("\n")
    af.close()

def readActiongrid(actionfile):
    actiongrid = np.genfromtxt(actionfile, delimiter = 1, dtype = "string")
    return actiongrid


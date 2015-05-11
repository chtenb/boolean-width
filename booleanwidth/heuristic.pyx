# cython: profile=False
from .bitset import (iterate, subsets, subsets_of_size, size, invert, tostring, subtract,
                     index, domain, contains, first)
#from .bitset128 import (iterate, subsets, subsets_of_size, size, invert, tostring, subtract,
                        #index, domain, contains)
from .bitset128 cimport uint128
import math
from .components import components, bfs
from .utils import shuffled

Infinity = float('inf')

# NOTE: we leave out the leaf cases, because they are annoying and don't mean anything


def get_neighborhood(N, subset):
    result = 0L
    for v in iterate(subset):
        result |= N[v]
    return result


def get_neighborhood_2(N, subset):
    result = get_neighborhood(N, subset)
    for v in iterate(result):
        result |= N[v]
    return result


def find_startvertex(graph, start):
    v = list(bfs(graph, start))[-1]
    return list(bfs(graph, v))[-1]


#
# SCORE FUNCTIONS
#

def lun(N, left, right, v):
    n_left = get_neighborhood(N, left)
    return size(subtract(N[v], n_left) & right)

def new_lun(N, left, right, v):
    n_left = get_neighborhood(N, left) & right
    return size(N[v] - (n_left & N[v]))

def relative_neighborhood2(N, left, right, v):
    n_left = get_neighborhood(N, left) & right
    numerator = size(N[v] & right - (n_left & N[v]))
    denominator = size(N[v] & n_left) # ~ size(N[v] & right)
    if denominator == 0:
        return numerator
    return float(numerator) / float(denominator)

def relative_neighborhood3(N, left, right, v):
    n_left = get_neighborhood(N, left)
    numerator = size(N[v] & right - (n_left & N[v]))
    denominator = size(N[v] & (n_left | left))
    if denominator == 0:
        return numerator
    return float(numerator) / float(denominator)

def relative_neighborhood4(N, left, right, v):
    n_left = get_neighborhood(N, left)
    numerator = size(N[v] - (n_left & N[v]))
    denominator = size(N[v] & (n_left | left))
    if denominator == 0:
        return numerator
    return float(numerator) / float(denominator)

def relative_neighborhood5(N, left, right, v):
    n_left = get_neighborhood(N, left) & right
    numerator1 = size(N[v] - (n_left & N[v]))
    numerator2 = size(N[v] & right - (n_left & N[v]))
    denominator = size(N[v] & n_left)
    p = N[0]
    #numerator = p * numerator1 + (1 - p) * numerator2
    #numerator = numerator1 ** p + numerator2 ** (1 - p)
    numerator = numerator1 if p > 0.2 else numerator2
    if denominator == 0:
        return numerator
    return float(numerator) / float(denominator)

def relative_neighborhood6(N, left, right, v):
    n_left = get_neighborhood(N, left) & right
    numerator = size(N[v] & right - (n_left & N[v]))
    #denominator = size(N[v] & n_left) # ~ size(N[v] & right)
    denominator = size(N[v])
    if denominator == 0:
        return numerator
    return float(numerator) / float(denominator)

def relative_neighborhood7(N, left, right, v):
    n_left = get_neighborhood(N, left) & right
    numerator = size(N[v] - (n_left & N[v]))
    denominator = size(N[v] & right)

    if denominator == 0:
        return numerator
    return float(numerator) / float(denominator)


def relative_neighborhood(N, left, right, v):
    n_left = get_neighborhood(N, left) & right
    numerator = size(N[v] & right - (n_left & N[v]))
    denominator = size(N[v] & right)
    return float(numerator) / float(denominator)

def relative_neighborhood_dense(N, left, right, v):
    n_left = get_neighborhood(N, left) & right
    numerator = size(N[v] - (n_left & N[v]))
    denominator = size(N[v])
    return float(numerator) / float(denominator)

def relative_neighborhood_sparse(N, left, right, v):
    n_left = get_neighborhood(N, left) & right
    numerator = size(N[v] & right - (n_left & N[v]))
    denominator = size(N[v])
    return float(numerator) / float(denominator)


def neighborhood_size(N, left, right, v):
    return size(N[v])


def minfront(N, left, right, v):
    new_n_left = get_neighborhood(N, left | v) & (right - v)
    new_n_right = get_neighborhood(N, right - v) & (left | v)
    new_front_size = min(size(new_n_left), size(new_n_right))

    return new_front_size

def minfront2(N, left, right, v):
    new_n_left = get_neighborhood(N, left | v) & (right - v)
    new_n_right = get_neighborhood(N, right - v) & (left | v)
    new_front_size = max(size(new_n_left), size(new_n_right))

    return new_front_size

def minfront3(N, left, right, v):
    new_n_left = get_neighborhood(N, left | v) & (right - v)
    return size(new_n_left)

def minfront4(N, left, right, v):
    new_n_right = get_neighborhood(N, right - v) & (left | v)
    return size(new_n_right)

def minfront5(N, left, right, v):
    new_n_left = get_neighborhood(N, left | v) & (right - v)
    a = size(new_n_left)
    b = min_cover_size(N, left, right, v)
    return a + (1 - 1.0 / b)


def min_cover_size(N, left, right, v):
    """
    Return an approximation of the number of neighborhoods from left in right needed
    to cover the the neighborhood of v in right.
    """
    universe = N[v] & right
    sets = {N[u] & universe for u in iterate(left)}
    cover = 0
    sets_needed = 0


    while not contains(cover, universe):
        if not sets:
            return sets_needed + 1

        # Choose set covering the most uncovered elements
        uncovered = universe - cover
        bestset = max(sets, key=lambda s: size(uncovered & s))
        sets.remove(bestset)
        cover |= bestset
        sets_needed += 1

    return sets_needed


def min_cover_front(N, left, right, v):
    return min_cover_size(N, left, right, v) + minfront(N, left, right, v)


def lun_mincover(N, left, right, v):
    return (min_cover_size(N, left, right, v) + lun(N, left, right, v))


def next_un(N, un_left, left, right, v):
    U = set()
    for S in un_left:
        U.add(S - (v & S))
        U.add(S - (v & S) | (N[v] & (right - (v & right))))
    return U


# Lets introduce UND: unions of neighborhoods by degree
def next_und(N, und_left, left, right, v):
    new_und = [set(0)] # There is only 1 union of degree 0

    for i in range(1, len(und_left)):
        new_und.append(set())
        for S in und_left[i]:
            new_und[i].add(S - (v & S)) # Update existing unions
        for S in und_left[i-1]:
            new_und.add(S - (v & S) | (N[v] & (right - (v & right))))

    return new_und


#
# RANDOM
#

def random_decomposition(graph):
    decomposition = []
    for component in components(graph):
        decomposition.extend(shuffled([v for v in iterate(component)]))
    return decomposition

#
# WIDTH
#

def check_decomposition(G, decomposition):
    un = {0L}
    lboolw = 1
    left = 0L
    right = G.vertices

    for v in decomposition:
        un = next_un(G.neighborhoods, un, left, right, v)
        #print(len(un))
        #print_un(un)
        lboolw = max(lboolw, len(un))
        left = left | v
        right = subtract(right, v)

    return lboolw


def greedy(G, depth=0):
    lboolw_components = []
    decomposition_components = []

    for component in components(G):
        best_lboolw = Infinity
        best_decomposition = None
        for i, start in enumerate(iterate(component)):
            print('{}th starting vertex'.format(i))
            right = subtract(component, start)
            left = start
            un_left = next_un(G.neighborhoods, {0L}, 0L, component, start)
            booldim_left = 1

            decomposition = [start]
            lboolw = len(un_left)

            for _ in range(size(component) - 1):
                #print('next vertex')
                best_vertex, best_un, _ = greedy_step(G, left, right, un_left, booldim_left,
                        depth, {}, Infinity)
                booldim_left = len(best_un)
                lboolw = max(lboolw, booldim_left)
                un_left = best_un

                decomposition.append(best_vertex)
                right = subtract(right, best_vertex)
                left = left | best_vertex

            #print(lboolw)
            #print(math.log(lboolw, 2))
            if lboolw < best_lboolw:
                best_lboolw = lboolw
                best_decomposition = decomposition
        lboolw_components.append(best_lboolw)
        decomposition_components.append(best_decomposition)

    total_lboolw = max(lboolw_components)
    total_decomposition = [v for part in decomposition_components for v in part]

    return total_lboolw, total_decomposition


def greedy_step(G, left, right, un_left, booldim_left, depth, un_table, bound):
    best_vertex = None
    best_booldim = Infinity
    best_un = None

    if size(right) == 1:
        return right, {0L}, 1

    assert size(right) > 1

    candidates = get_neighborhood_2(G.neighborhoods, left) & right

    # Trivial cases are slow
    for v in iterate(candidates):
        if trivial_case(G.neighborhoods, left, right, v):
            new_un = next_un(G.neighborhoods, un_left, left, right, v)
            new_booldim = len(new_un)
            return v, new_un, new_booldim

    ties = 0 # TEST

    for v in iterate(candidates):
        if left | v not in un_table:
            un_table[left | v] = next_un(G.neighborhoods, un_left, left, right, v)
        new_un = un_table[left | v]
        new_booldim = len(new_un)

        # Apply pruning
        if new_booldim >= bound:
            #print('pruning')
            continue

        if depth > 0:
            _, _, recursive_booldim = greedy_step(G, left | v, subtract(right, v), new_un,
                    new_booldim, depth - 1, un_table, best_booldim)
            new_booldim = max(new_booldim, recursive_booldim)

        if new_booldim == best_booldim:
            #print('Same value')
            # TODO: relative neighborhoods lookahead
            pass

        if new_booldim == best_booldim:
            ties += 1

        if new_booldim < best_booldim:
            ties = 0
            best_vertex = v
            best_booldim = new_booldim
            best_un = new_un

        # Better is not possible
        #if float(booldim_left) / float(new_booldim) > 1.5:
            #print(booldim_left / new_booldim)
        #if float(booldim_left) / float(new_booldim) > 1.5:
            #print('Better is not possible')
            #break

    # If nothing found
    if best_vertex == None:
        best_un = next_un(G.neighborhoods, un_left, left, right, v)
        best_booldim = len(best_un)
        best_vertex = v

    #print('Ties: {}'.format(ties))

    assert best_vertex != None
    return best_vertex, best_un, best_booldim


def trivial_case(N, left, right, v):
    # No neighbors
    if contains(left, N[v]):
        return True

    # Twins
    for u in iterate(left):
        if N[v] & right == subtract(N[u], v) & right:
            return True

    return False

#
# LIGHT HEURISTICS
#

def greedy_light(G, score_function, depth=0):
    component_scores = []
    component_decompositions = []

    for component in components(G):
        best_score = Infinity
        best_decomposition = None
        for i, start in enumerate(iterate(component)):
            #print('{}th starting vertex'.format(i))
            right = subtract(component, start)
            left = start
            decomposition = [start]
            score = 0
            for _ in range(size(component) - 1):
                best_vertex, best_value = greedy_light_step(G, score_function, left, right, depth)
                decomposition.append(best_vertex)
                right = subtract(right, best_vertex)
                left = left | best_vertex
                #score = max(score, best_value)
                score += best_value

            if score < best_score:
                best_score = score
                best_decomposition = decomposition
        component_scores.append(best_score)
        component_decompositions.append(best_decomposition)

    total_score = max(component_scores)
    total_decomposition = [v for part in component_decompositions for v in part]

    return total_score, total_decomposition

def greedy_light_single_start(G, score_function, depth=0):
    component_decompositions = []

    # HACK
    #print(len(list(G.edges)))
    #print((len(G) ** 2))
    p = G.density
    #print(p)
    G.neighborhoods[0] = p

    for component in components(G):
        start = find_startvertex(G, first(component))
        #start = 2
        #print(tostring(G.vertices))
        #print(contains(G.vertices, 1))
        #print('WARNING: STARTING POINT IS FIXED')
        right = subtract(component, start)
        left = start
        decomposition = [start]
        for _ in range(size(component) - 1):
            best_vertex, score = greedy_light_step(G, score_function, left, right, depth)
            #print('Choosing {} with a score of {}'.format(index(best_vertex), score))
            decomposition.append(best_vertex)
            right = subtract(right, best_vertex)
            left = left | best_vertex

        component_decompositions.append(decomposition)
    total_decomposition = [v for part in component_decompositions for v in part]
    return total_decomposition

def greedy_light_step(G, score_function, left, right, depth):
    best_vertex = None
    best_score = Infinity

    if size(right) == 1:
        return right, 0

    assert size(right) > 1
    assert size(left) > 0

    candidates = get_neighborhood_2(G.neighborhoods, left) & right
    #candidates = get_neighborhood(G.neighborhoods, left) & right
    assert size(candidates) > 0
    #print('Candidates: {}'.format(size(candidates)))

    # Trivial cases are slow
    for v in iterate(candidates):
        if trivial_case(G.neighborhoods, left, right, v):
            return v, 100

    for v in iterate(candidates):
    #print(tostring(right))
    #for v in iterate(right):
        new_score = score_function(G.neighborhoods, left, right, v)
        #if size(left) == 2:
            #print('asd ' + str(new_score))

        if depth > 0:
            assert 0
            _, recursive_score = greedy_light_step(G, score_function, left | v,
                    subtract(right, v), depth - 1)
            new_score += recursive_score

        if new_score < best_score:
            best_vertex = v
            best_score = new_score

    assert best_vertex != None
    return best_vertex, best_score


#
# COST VARIANT
#

def greedy_cost(G, depth=0):
    lboolc_components = []
    decomposition_components = []

    for component in components(G):
        best_lboolc = Infinity
        best_decomposition = None
        for i, start in enumerate(iterate(component)):
            print('{}th starting vertex'.format(i))
            right = subtract(component, start)
            left = start
            un_left = next_un(G.neighborhoods, {0L}, 0L, component, start)
            booldim_left = 2

            decomposition = [start]
            lboolc = len(un_left)

            for _ in range(size(component) - 1):
                #print('next vertex')
                best_vertex, best_un, _ = greedy_cost_step(G, left, right, un_left, booldim_left,
                        depth, {})
                #best_vertex, best_un, _ = greedy_cost_ties_step(G, left, right, un_left,
                        #booldim_left, depth, {})
                booldim_left = len(best_un)
                lboolc += booldim_left
                un_left = best_un

                decomposition.append(best_vertex)
                right = subtract(right, best_vertex)
                left = left | best_vertex

            if lboolc < best_lboolc:
                best_lboolc = lboolc
                best_decomposition = decomposition
        lboolc_components.append(best_lboolc)
        decomposition_components.append(best_decomposition)

    total_lboolc = sum(lboolc_components)
    total_decomposition = [v for part in decomposition_components for v in part]

    return total_lboolc, total_decomposition


def greedy_cost_step(G, left, right, un_left, booldim_left, depth, un_table):
    if size(right) == 1:
        return right, {0L}, 1

    assert size(right) > 1

    best_vertex = None
    best_cost = Infinity
    best_un = None

    candidates = get_neighborhood_2(G.neighborhoods, left) & right

    ties = 0 # TEST

    for v in iterate(candidates):
        if left | v not in un_table:
            un_table[left | v] = next_un(G.neighborhoods, un_left, left, right, v)
        new_un = un_table[left | v]
        new_cost = len(new_un)

        if depth > 0:
            _, _, recursive_cost = greedy_cost_step(G, left | v, subtract(right, v), new_un,
                    new_cost, depth - 1, un_table)
            new_cost = new_cost + recursive_cost

        if new_cost == best_cost:
            ties += 1
        if new_cost < best_cost:
            ties = 0
            best_vertex = v
            best_cost = new_cost
            best_un = new_un

    print('Ties: {}'.format(ties))

    assert best_vertex != None
    return best_vertex, best_un, best_cost


def check_decomposition_cost(G, decomposition):
    assert len(decomposition) == size(G.vertices)
    un = {0L}
    lboolc = 0
    left = 0L
    right = G.vertices

    for v in decomposition:
        un = next_un(G.neighborhoods, un, left, right, v)
        #un_leaf = next_un(G.neighborhoods, {0L}, 0L, G.vertices, v)
        #print(len(un))
        #print_un(un)
        #lboolc += len(un) + len(un_leaf)
        lboolc += len(un)
        left = left | v
        right = subtract(right, v)

    return lboolc


#
# RECURSE ON TIES
#

def greedy_cost_ties(G, depth=0):
    lboolc_components = []
    decomposition_components = []

    for component in components(G):
        best_lboolc = Infinity
        best_decomposition = None
        for i, start in enumerate(iterate(component)):
            print('{}th starting vertex'.format(i))
            right = component - (start & component)
            left = start
            un_left = next_un(G.neighborhoods, {0L}, 0L, component, start)
            booldim_left = 2

            decomposition = [start]
            lboolc = len(un_left)

            for _ in range(size(component) - 1):
                best_vertex, best_un, _ = greedy_cost_ties_step(G, left, right, un_left,
                        booldim_left, depth, {})
                booldim_left = len(best_un)
                lboolc += booldim_left
                un_left = best_un

                decomposition.append(best_vertex)
                right = right - (best_vertex & right)
                left = left | best_vertex

            #print(lboolc)
            #print(math.log(lboolc, 2))
            if lboolc < best_lboolc:
                best_lboolc = lboolc
                best_decomposition = decomposition
        lboolc_components.append(best_lboolc)
        decomposition_components.append(best_decomposition)

    total_lboolc = sum(lboolc_components)
    total_decomposition = [v for part in decomposition_components for v in part]

    return total_lboolc, total_decomposition


def greedy_cost_ties_step(G, left, right, un_left, booldim_left, depth, un_table):
    """
    Return the best vertex, along with its score and un.
    """
    if size(right) == 1:
        return right, {0}, 1

    assert size(right) > 1

    candidates = get_neighborhood_2(G.neighborhoods, left) & right

    best_vertices = []
    best_uns = []
    best_score = Infinity
    #print(left)


    for v in iterate(candidates):
        if left | v not in un_table:
            un_table[left | v] = next_un(G.neighborhoods, un_left, left, right, v)
        new_un = un_table[left | v]
        new_score = len(new_un)

        if new_score == best_score:
            best_vertices.append(v)
            best_uns.append(new_un)
        elif new_score < best_score:
            best_score = new_score
            best_vertices = [v]
            best_uns = [new_un]

    #print('Ties: {}'.format(len(best_vertices) - 1))

    if len(best_vertices) == 1 or len(best_vertices) > 10:
        return best_vertices[0], best_uns[0], best_score

    assert len(best_vertices) > 1


    if depth > 0:
        print('Recursing from depth {} to {} for {} vertices'.format(depth, depth - 1,
            len(best_vertices)))
        best_index = 0
        best_recursive_score = Infinity
        for i, v in enumerate(best_vertices):
            _, _, recursive_score = greedy_cost_ties_step(G, left | v, subtract(right, v),
                    best_uns[i], new_score, depth - 1, un_table)
            new_score = new_score + recursive_score
            if new_score < best_recursive_score:
                best_index = i
                best_recursive_score = new_score
        return best_vertices[best_index], best_uns[best_index], best_score

    return best_vertices[0], best_uns[0], best_score




#
# FIRST IMPROVEMENT
#


def first_improvement(G, depth=0):
    V = G.vertices

    best_lboolw = Infinity
    best_decomposition = None

    for i, start in enumerate(iterate(V)):
    #for i, start in enumerate(iterate(2)):
        print('{}th starting vertex'.format(i))
        right = subtract(V, start)
        left = start
        un_left = next_un(G.neighborhoods, {0L}, 0L, V, start)

        decomposition = [start]
        lboolw = len(un_left)

        for _ in range(size(V) - 1):
            best_vertex, best_un, _ = first_improvement_step(G, left, right, un_left, depth)
            lboolw = max(lboolw, len(best_un))
            un_left = best_un

            decomposition.append(best_vertex)
            right = subtract(right, best_vertex)
            left = left | best_vertex

        if lboolw < best_lboolw:
            best_lboolw = lboolw
            best_decomposition = decomposition

    return best_lboolw, best_decomposition


def first_improvement_step(G, left, right, un_left, depth=0):
    if size(right) == 1:
        return right, {0L}, 1
    assert size(right) > 1

    current_booldim = len(un_left)
    candidates = get_neighborhood_2(G, left) & right
    for v in iterate(candidates):
        new_un = next_un(G.neighborhoods, un_left, left, right, v)
        new_booldim = len(new_un)

        if depth > 0:
            _, _, recursive_booldim = first_improvement_step(G, left | v, subtract(right, v), new_un, depth - 1)
            new_booldim = max(new_booldim, recursive_booldim)

        if new_booldim < current_booldim:
            return v, new_un, new_booldim

    # Just return last vertex if no improvement found
    return v, new_un, new_booldim

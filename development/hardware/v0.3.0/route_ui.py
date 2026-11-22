"""Route the nine key nets on the two-layer UI placement study.

Grid routing is a geometry starting point. KiCad DRC remains the gate.
"""
from pathlib import Path
from heapq import heappush, heappop
import math
import pcbnew as p

ROOT = Path(__file__).resolve().parent
board = p.LoadBoard(str(ROOT / "CorePad_UI_v0.3.0.kicad_pcb"))
footprints = {f.GetReference(): f for f in board.GetFootprints()}
STEP, WIDTH, CLEARANCE = .25, .15, .20
VIA_DIAMETER, VIA_DRILL = .6, .3
EXTENTS = (50.5, 147.5, 50.5, 127.5)
LAYER_IDS = (p.B_Cu, p.F_Cu)


def mm(value):
    return p.ToMM(value)


def xy(value):
    return (mm(value.x), mm(value.y))


def vec(value):
    return p.VECTOR2I(p.FromMM(value[0]), p.FromMM(value[1]))


def pad(ref, number):
    return next(x for x in footprints[ref].Pads() if x.GetNumber() == str(number))


pads = []
for footprint in footprints.values():
    for item in footprint.Pads():
        box = item.GetBoundingBox()
        pads.append((item.m_Uuid.AsString(), (mm(box.GetX()), mm(box.GetX()+box.GetWidth()),
                      mm(box.GetY()), mm(box.GetY()+box.GetHeight())),
                     tuple(item.IsOnLayer(layer) for layer in LAYER_IDS), item.HasDrilledHole()))

routes = []  # (a, b, layer-index, net-name)
vias = []  # (x, y, net-name)
pad_buckets = {}
route_buckets = {}
via_buckets = {}


def bucket_cells(xmin, xmax, ymin, ymax):
    for ix in range(math.floor(xmin)-1, math.ceil(xmax)+2):
        for iy in range(math.floor(ymin)-1, math.ceil(ymax)+2):
            yield (ix, iy)


for entry in pads:
    bounds = entry[1]
    for cell in bucket_cells(bounds[0], bounds[1], bounds[2], bounds[3]):
        pad_buckets.setdefault(cell, []).append(entry)


def distance_to_segment(x, y, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    t = max(0, min(1, ((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-a[0]-t*dx, y-a[1]-t*dy)


def blocked(x, y, layer, net, endpoints, radius=WIDTH/2):
    if x < EXTENTS[0] or x > EXTENTS[1] or y < EXTENTS[2] or y > EXTENTS[3]:
        return True
    halo = radius + CLEARANCE
    bucket = (math.floor(x), math.floor(y))
    for identity, bounds, copper, drilled in pad_buckets.get(bucket, ()):
        if identity in endpoints:
            continue
        if (copper[layer] or drilled) and bounds[0]-halo <= x <= bounds[1]+halo and bounds[2]-halo <= y <= bounds[3]+halo:
            return True
    for a, b, track_layer, other in route_buckets.get(bucket, ()):
        if other != net and track_layer == layer and distance_to_segment(x, y, a, b) < radius+WIDTH/2+CLEARANCE:
            return True
    for vx, vy, other in via_buckets.get(bucket, ()):
        if other != net and math.hypot(x-vx, y-vy) < radius+VIA_DIAMETER/2+CLEARANCE:
            return True
    return False


def via_free(x, y, net, endpoints):
    return all(not blocked(x, y, layer, net, endpoints, VIA_DIAMETER/2) for layer in (0, 1))


def route(number):
    src, dst = pad(f"SW{number}", 1), pad("J_UI", number)
    net = f"KEY{number}"
    endpoints = {src.m_Uuid.AsString(), dst.m_Uuid.AsString()}
    start_xy, goal_xy = xy(src.GetPosition()), xy(dst.GetPosition())
    # The key's plated hole launches on F.Cu; the FFC pad is only B.Cu.
    start = (round(start_xy[0]/STEP), round(start_xy[1]/STEP), 1)
    goal = (round(goal_xy[0]/STEP), round(goal_xy[1]/STEP), 0)
    frontier = [(0, start)]
    score, previous, closed = {start: 0}, {start: None}, set()
    directions = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
    while frontier:
        _, here = heappop(frontier)
        if here in closed:
            continue
        closed.add(here)
        if here == goal:
            break
        if len(closed) > 450000:
            raise RuntimeError(f"Search exhausted on {net}")
        x, y, layer = here
        candidates = []
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if blocked(nx*STEP, ny*STEP, layer, net, endpoints):
                continue
            if blocked((x+dx/2)*STEP, (y+dy/2)*STEP, layer, net, endpoints):
                continue
            candidates.append(((nx, ny, layer), math.hypot(dx, dy)))
        if via_free(x*STEP, y*STEP, net, endpoints):
            candidates.append(((x, y, 1-layer), 10))
        for target, cost in candidates:
            new_score = score[here] + cost
            if new_score >= score.get(target, math.inf):
                continue
            score[target], previous[target] = new_score, here
            estimate = math.hypot(target[0]-goal[0], target[1]-goal[1]) + (8 if target[2] != goal[2] else 0)
            heappush(frontier, (new_score+estimate, target))
    if goal not in previous:
        raise RuntimeError(f"No legal grid path for {net}; explored {len(closed)} cells")
    cells = []
    here = goal
    while here is not None:
        cells.append(here)
        here = previous[here]
    cells.reverse()
    for a, b in zip(cells, cells[1:]):
        ax, ay, al = a; bx, by, bl = b
        if al != bl:
            item = p.PCB_VIA(board)
            item.SetPosition(vec((ax*STEP, ay*STEP)))
            item.SetWidth(p.F_Cu, p.FromMM(VIA_DIAMETER))
            item.SetWidth(p.B_Cu, p.FromMM(VIA_DIAMETER))
            item.SetDrill(p.FromMM(VIA_DRILL))
            item.SetLayerPair(p.F_Cu, p.B_Cu)
            item.SetNet(src.GetNet()); board.Add(item)
            entry = (ax*STEP, ay*STEP, net)
            vias.append(entry)
            for cell in bucket_cells(entry[0]-.7,entry[0]+.7,entry[1]-.7,entry[1]+.7):
                via_buckets.setdefault(cell, []).append(entry)
        else:
            axy, bxy = (ax*STEP, ay*STEP), (bx*STEP, by*STEP)
            item = p.PCB_TRACK(board)
            item.SetStart(vec(axy)); item.SetEnd(vec(bxy))
            item.SetLayer(LAYER_IDS[al]); item.SetWidth(p.FromMM(WIDTH))
            item.SetNet(src.GetNet()); board.Add(item)
            entry = (axy, bxy, al, net)
            routes.append(entry)
            for cell in bucket_cells(min(axy[0],bxy[0]),max(axy[0],bxy[0]),min(axy[1],bxy[1]),max(axy[1],bxy[1])):
                route_buckets.setdefault(cell, []).append(entry)
    for endpoint, cell in ((start_xy, cells[0]), (goal_xy, cells[-1])):
        grid_xy = (cell[0]*STEP, cell[1]*STEP)
        if math.dist(endpoint, grid_xy) > .001:
            item = p.PCB_TRACK(board)
            item.SetStart(vec(endpoint)); item.SetEnd(vec(grid_xy))
            item.SetLayer(LAYER_IDS[cell[2]]); item.SetWidth(p.FromMM(WIDTH))
            item.SetNet(src.GetNet()); board.Add(item)
            routes.append((endpoint, grid_xy, cell[2], net))
    print(net, "segments", len(cells)-1, "vias", sum(a[2]!=b[2] for a,b in zip(cells,cells[1:])))


failed = []
for key in (3,2,1,6,5,4,9,8,7):
    try:
        route(key)
    except RuntimeError as error:
        failed.append(key)
        print(error)
p.SaveBoard(str(ROOT / "CorePad_UI_v0.3.0.kicad_pcb"), board)
print("Saved partial key routes; open keys:", failed, "; GND and auxiliary circuits remain open")

# SETUP
# =====
from geospatial_ross import * # adjust later if necessary
import matplotlib.pyplot as plt
from matplotlib import use as mpl_use  # remove for Windows use
# import matplotlib.pyplot as plt # import for windows use

mpl_use('MacOSX') # remove for windows use


# sample data points for beginning
station1_points = [[0, 0], [0, 3], [3, 3], [3, 2.5], [4, 0.5], [1,0], [0,0]]

counter1_points = [[1, 5], [1, 7], [3, 8], [4, 6.5], [4, 5], [2.5,4.5], [1,5]]
counter2_points = [[1, 1], [1, 3], [3, 4], [4, 2.5], [4, 1], [2.5,0.5], [1,1]]
counter3_points = [[0,4], [0.5,4], [1.5,3.75], [1.5,3], [1,2.25], [0.5,2], [0,3], [0,4]]
counter4_points = [[0,7], [0.5,7], [1.5,6.75], [1.5,6], [1,5.25], [0.5,5], [0,6], [0,7]]

# sample polygons from sample data points (via Polygon class in geospatial)
station1 = Polygon(station1_points, xcol=0, ycol=1)

counter1 = Polygon(counter1_points, xcol=0, ycol=1)
counter2 = Polygon(counter2_points, xcol=0, ycol=1)
counter3 = Polygon(counter3_points, xcol=0, ycol=1)
counter4 = Polygon(counter4_points, xcol=0, ycol=1)

# sample list of polygons => later: resulting voronoi as input
counters = [counter1, counter2, counter3, counter4 ]

stations = [station1]

# CONTINUATION
# ============

# Find potentially intersecting polygons via bounding box
def findIntersPoly(station, counters):
    intersects = [] 
    bboxStation = Bbox(station) # bounding box around station voronoi
    for counter in counters:
        bboxCounter = Bbox(counter) # bounding box around counter voronoi (simplest approach)
        if bboxStation.intersects(bboxCounter): # check for bbox intersection
            intersects.append(counter) # store counters that "intersect" with station voronoi
    return intersects

print(findIntersPoly(station1, counters))

# Find points in polygon
def findPointinPoly(station, counter):
    containing = []
    # find counter points in station polygon
    for point in counter.points:
        if station.containsPoint(point):
            containing.append([point.x, point.y])
    # find station points in counter polygon
    for point in station.points:
        if counter.containsPoint(point):
            containing.append([point.x, point.y])
    # Use list comprehension to filter out duplicates (chatgpt)        
    seen = set()
    containing = [x for x in containing if tuple(x) not in seen and not seen.add(tuple(x))]
    return containing

print(findPointinPoly(station1, counter2))

# Find intersecting segments and intersection points of two polygons
def findIntersections(station, counter):
    # identify segments
    seg_station = []
    seg_counter = []
    seg_intersect_points = [] # prepare for final output
    for i in range(len(station.points)-1):
        seg = Segment(station.points[i], station.points[i+1])
        seg_station.append(seg)
    for i in range(len(counter.points)-1):
        seg = Segment(counter.points[i], counter.points[i+1])
        seg_counter.append(seg)
    # determine if segments intersect
    for stationseg in seg_station:
        for counterseg in seg_counter:
            if stationseg.intersects(counterseg): 
                # determine intersection point
                x1_stat = stationseg.start.x
                x2_stat = stationseg.end.x
                y1_stat = stationseg.start.y
                y2_stat = stationseg.end.y
                x1_coun = counterseg.start.x
                x2_coun = counterseg.end.x
                y1_coun = counterseg.start.y
                y2_coun = counterseg.end.y
                # calculate slopes and y-intercepts, avoid division by zero
                if x2_stat - x1_stat == 0:
                    m_stat = float('inf')
                else:
                    m_stat = (y2_stat - y1_stat) / (x2_stat - x1_stat)
                q_stat = y1_stat - m_stat * x1_stat
                if x2_coun - x1_coun == 0:
                   m_coun = float('inf')
                else:
                    m_coun = (y2_coun - y1_coun) / (x2_coun - x1_coun)
                q_coun = y1_coun - m_coun * x1_coun
                # calculate & add intersection points
                if m_coun != m_stat: # !! assumption: if intersect and parallel => identical!
                # if identical, no storage needed because point is already included by PiP check
                    x_inters = (q_coun - q_stat) / (m_stat - m_coun)
                    y_inters = m_stat * x_inters + q_stat
                    p = Point(x_inters, y_inters)
                    seg_intersect_points.append(p)
    return seg_intersect_points                   

# only adding them to other PiP results is missing

    
print(findIntersections(station1, counter2))


#box = Bbox(station1)
#box.plot_bbox()
station1.plot_polygon()
#counter1.plot_polygon()
counter2.plot_polygon()
#counter3.plot_polygon()
#counter4.plot_polygon()
plt.show()















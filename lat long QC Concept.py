import csv
import ast
from matplotlib import pyplot as plt
from shapely.geometry import Polygon, Point

data = []
with open("AndersonCounty.csv") as f:
    reader = csv.reader(f)
    next(reader) # skip header
    #data = []
    for r in reader:


        r = tuple(r)[3]

        #Correct the data to right format
        r = ast.literal_eval(r)

        data.append(r)

#print(data)



poly = Polygon(data)

x,y = poly.exterior.xy




fig = plt.figure(1, figsize=(5,5), dpi=90)
ax = fig.add_subplot(111)
#ax.legend(('label1', 'label2', 'label3'))

#Plot the Polygon

ax.plot(x, y)
ax.set_title('Anderson County')
#legend()



#Plot the first point and determine if it is within the polygon
point1x = -95.633481
point1y = 31.812007

point1 = Point(point1x, point1y)

plt.plot(point1x, point1y, 'ro')

print("Is Point 1(Red) within the county? " + str(point1.within(poly)))

#Plot the Second point and determine if it is within the polygon
point2x = -96
point2y = 31.782

point2 = Point(point2x, point2y)

plt.plot(point2x, point2y, 'go')




print("Is Point 2(Green) within the county? " + str(point2.within(poly)))

#NEED THIS FOR PYCHARM TO SHOW THE PLOT
plt.show()
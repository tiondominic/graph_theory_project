import math
import random
import visual


def calculate_distance(point1, point2):
  return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def divide_points(points):
  if random.choice([True, False]):
    points.sort(key=lambda point: point[0])
  else:
    points.sort(key=lambda point: point[1])
  mid = len(points) // 2
  return points[:mid], points[mid:]

def find_shortest(subset1, subset2):
  min_distance = float('inf')
  bridge = None

  for point1 in subset1:
    for point2 in subset2:
      distance = calculate_distance(point1, point2)
      if distance < min_distance:
        min_distance = distance
        bridge = (point1, point2)

  return bridge

def dac(points):
  if len(points) == 1:
    return points, 0
  if len(points) == 2:
    distance = calculate_distance(points[0], points[1])
    return points + [points[0]], 2 * distance

  subset1, subset2 = divide_points(points)
  tour1, distance1 = dac(subset1)
  tour2, distance2 = dac(subset2)

  bridge = find_shortest(subset1, subset2)
  tour1 = tour1[:-1]
  merged_tour = tour1 + [bridge[0], bridge[1]] + tour2

  merged_distance = distance1 + distance2 + calculate_distance(bridge[0], bridge[1])

  return merged_tour, merged_distance

if __name__ == "__main__":

  # Kani siya is for generate random points of houses
  houses = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(20)]
  print(houses)

  tour, total_distance = dac(houses)
  print("Tour (coordinates):", tour)
  print("Total Distance: ", total_distance)

  nodes = {}
  for i, house in enumerate(houses):
    nodes[house] = f"House {i}"


  visual.visualize_tour(nodes, tour)
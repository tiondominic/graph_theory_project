import math
import random
import visual


def build_distances(edges, houses):
  dist = {(a, b): (0 if a == b else float('inf')) for a in houses for b in houses}
  for weight, source, destination in edges:
    if weight < dist[(source, destination)]:
      dist[(source, destination)] = weight
      dist[(destination, source)] = weight

  for k in houses:
    for i in houses:
      for j in houses:
        if dist[(i, k)] + dist[(k, j)] < dist[(i, j)]:
          dist[(i, j)] = dist[(i, k)] + dist[(k, j)]

  return dist

def calculate_distance(point1, point2):
  return distances[(point1, point2)]

def divide_points(points):
  first = points[0]
  points.sort(key=lambda point: calculate_distance(first, point))
  mid = len(points) // 2
  return points[:mid], points[mid:]

def tour_distance(tour):
  return sum(calculate_distance(tour[i], tour[(i + 1) % len(tour)]) for i in range(len(tour)))

def find_shortest(tour1, tour2):
  min_distance = float('inf')
  best = None

  for i in range(len(tour1)):
    rotated1 = tour1[i:] + tour1[:i]
    for j in range(len(tour2)):
      rotated2 = tour2[j:] + tour2[:j]
      for candidate in (rotated2, rotated2[::-1]):
        merged = rotated1 + candidate
        distance = tour_distance(merged)
        if distance < min_distance:
          min_distance = distance
          best = merged

  return best

def dac(points):
  if len(points) == 1:
    return points, 0
  if len(points) == 2:
    return points, 2 * calculate_distance(points[0], points[1])

  subset1, subset2 = divide_points(points)
  tour1, distance1 = dac(subset1)
  tour2, distance2 = dac(subset2)

  merged_tour = find_shortest(tour1, tour2)
  merged_distance = tour_distance(merged_tour)

  return merged_tour, merged_distance

if __name__ == "__main__":

  houses = ["W", "A", "B", "C", "D", "E", "F"]

  edges = [
    (4, "W", "A"),
    (5, "W", "D"),
    (2, "A", "B"),
    (3, "A", "C"),
    (2, "B", "C"),
    (2, "D", "E"),
    (4, "D", "F"),
    (3, "E", "F"),
    (8, "A", "D"),
    (6, "B", "D"),
    (7, "B", "E"),
    (5, "C", "E"),
  ]
  print(edges)

  distances = build_distances(edges, houses)

  tour, total_distance = dac(houses)
  start = tour.index("W")
  tour = tour[start:] + tour[:start] + ["W"]
  print("Tour:", tour)
  print("Total Distance: ", total_distance)

  nodes = {}
  for i, house in enumerate(houses):
    nodes[house] = f"House {i}"

  visual.visualize_tour(nodes, tour, edges=edges)

import math
import random
import visual


def build_distances(distance_matrix, buildings):
  dist = {}

  for i, source in enumerate(buildings):
    for j, destination in enumerate(buildings):
      dist[(source, destination)] = distance_matrix[source][j]

  return dist


def calculate_distance(point1, point2):
  return distances[(point1, point2)]


def divide_points(points):
  first = points[0]
  points.sort(key=lambda point: calculate_distance(first, point))
  mid = len(points) // 2
  return points[:mid], points[mid:]


def tour_distance(tour):
  return round(sum(calculate_distance(tour[i], tour[(i + 1) % len(tour)]) for i in range(len(tour))), 9)

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
  destination_names = {
    "A": "Centrio",
    "B": "KetKai",
    "C": "SM Downtown",
    "D": "Xavier University",
    "E": "City Hall",
    "F": "Gaston Park"
  }

  distance_matrix = {
    "A": [0, 1.2, 0.6, 1.5, 2.2, 2.4],
    "B": [1.2, 0, 1.0, 1.7, 2.8, 3.0],
    "C": [0.6, 1.0, 0, 1.8, 2.6, 2.8],
    "D": [1.5, 1.7, 1.8, 0, 1.5, 1.3],
    "E": [2.2, 2.8, 2.6, 1.5, 0, 0.4],
    "F": [2.4, 3.0, 2.8, 1.3, 0.4, 0]
  }

  buildings = ["A", "B", "C", "D", "E", "F"]

  distances = build_distances(distance_matrix, buildings)

  tour, total_distance = dac(buildings.copy())
  tour = tour + [tour[0]]

  print("Tour:", tour)
  print("Route:", " -> ".join(destination_names[b] for b in tour))
  print("Total Distance:", total_distance)

  visual.visualize_tour(destination_names, tour)

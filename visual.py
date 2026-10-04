import math
import random
import itertools
import pygame


def visualize_tour(nodes, tour, window_size=800, node_radius=16, step_delay_ms=300, edges=None):
    if not nodes or len(nodes) < 2:
        print("Need at least 2 nodes to visualize.")
        return

    edges = edges or []
    node_keys = list(nodes.keys())

    pos_layout = {node: [random.uniform(-1, 1), random.uniform(-1, 1)] for node in node_keys}

    edge_weights = {}
    graph_edges = set()
    for item in edges:
        if len(item) == 3:
            weight, u, v = item
        else:
            u, v = item[0], item[1]
            weight = None
        if u in pos_layout and v in pos_layout:
            edge_key = (u, v) if u < v else (v, u)
            graph_edges.add(edge_key)
            if weight is not None:
                edge_weights[edge_key] = weight

    iterations = 200
    k = math.sqrt(1.0 / len(node_keys))
    t = 0.1

    for _ in range(iterations):
        disp = {node: [0.0, 0.0] for node in node_keys}

        for u, v in itertools.combinations(node_keys, 2):
            dx = pos_layout[u][0] - pos_layout[v][0]
            dy = pos_layout[u][1] - pos_layout[v][1]
            dist = math.hypot(dx, dy) or 0.01
            force = (k * k) / dist
            disp[u][0] += (dx / dist) * force
            disp[u][1] += (dy / dist) * force
            disp[v][0] -= (dx / dist) * force
            disp[v][1] -= (dy / dist) * force

        for u, v in graph_edges:
            dx = pos_layout[u][0] - pos_layout[v][0]
            dy = pos_layout[u][1] - pos_layout[v][1]
            dist = math.hypot(dx, dy) or 0.01
            force = (dist * dist) / k
            disp[u][0] -= (dx / dist) * force
            disp[u][1] -= (dy / dist) * force
            disp[v][0] += (dx / dist) * force
            disp[v][1] += (dy / dist) * force

        for node in node_keys:
            d_len = math.hypot(disp[node][0], disp[node][1]) or 0.01
            pos_layout[node][0] += (disp[node][0] / d_len) * min(d_len, t)
            pos_layout[node][1] += (disp[node][1] / d_len) * min(d_len, t)

    all_x = [pos[0] for pos in pos_layout.values()]
    all_y = [pos[1] for pos in pos_layout.values()]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    range_x = (max_x - min_x) if max_x != min_x else 1
    range_y = (max_y - min_y) if max_y != min_y else 1

    padding = 80
    usable_space = window_size - (2 * padding)

    def to_screen_pos(node):
        x, y = pos_layout[node]
        screen_x = padding + ((x - min_x) / range_x) * usable_space
        screen_y = window_size - (padding + ((y - min_y) / range_y) * usable_space)
        return (int(screen_x), int(screen_y))

    pixel_positions = {node: to_screen_pos(node) for node in node_keys}

    pygame.init()
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Animated Graph & Tour Visualizer")
    node_font = pygame.font.SysFont("Arial", max(10, int(node_radius * 0.8)), bold=True)
    weight_font = pygame.font.SysFont("Arial", 14, bold=True)
    clock = pygame.time.Clock()

    COLOR_BG = (255, 255, 255)
    COLOR_DEFAULT_EDGE = (210, 215, 225)
    COLOR_TOUR_EDGE = (235, 60, 60)
    COLOR_NODE = (40, 115, 220)
    COLOR_NODE_TEXT = (255, 255, 255)
    COLOR_WEIGHT_TEXT = (50, 50, 50)
    COLOR_WEIGHT_BG = (240, 240, 240)

    STEP_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(STEP_EVENT, step_delay_ms)

    tour_index = 0
    animated_edges = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == STEP_EVENT:
                if tour_index < len(tour) - 1:
                    u = tour[tour_index]
                    v = tour[tour_index + 1]
                    if u != v:
                        animated_edges.append((u, v))
                    tour_index += 1

        screen.fill(COLOR_BG)

        for u, v in graph_edges:
            p1 = pixel_positions[u]
            p2 = pixel_positions[v]
            pygame.draw.line(screen, COLOR_DEFAULT_EDGE, p1, p2, width=2)

        for u, v in animated_edges:
            if u in pixel_positions and v in pixel_positions:
                p1 = pixel_positions[u]
                p2 = pixel_positions[v]
                pygame.draw.line(screen, COLOR_TOUR_EDGE, p1, p2, width=5)

        for (u, v), weight in edge_weights.items():
            p1 = pixel_positions[u]
            p2 = pixel_positions[v]
            mid_x = (p1[0] + p2[0]) // 2
            mid_y = (p1[1] + p2[1]) // 2

            text_surface = weight_font.render(str(weight), True, COLOR_WEIGHT_TEXT)
            text_rect = text_surface.get_rect(center=(mid_x, mid_y))

            bg_rect = text_rect.inflate(6, 4)
            pygame.draw.rect(screen, COLOR_WEIGHT_BG, bg_rect, border_radius=3)
            pygame.draw.rect(screen, COLOR_DEFAULT_EDGE, bg_rect, width=1, border_radius=3)
            screen.blit(text_surface, text_rect)

        for node, label in nodes.items():
            pos = pixel_positions[node]

            pygame.draw.circle(screen, COLOR_NODE, pos, node_radius)

            text_surface = node_font.render(str(node), True, COLOR_NODE_TEXT)
            text_rect = text_surface.get_rect(center=pos)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
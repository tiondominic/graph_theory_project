import pygame
import itertools


def visualize_tour(nodes, tour, window_size=800, node_radius=16, step_delay_ms=300):
    if not nodes or len(nodes) < 2:
        print("Need at least 2 nodes to visualize.")
        return

    node_keys = list(nodes.keys())
    all_edges = set()
    for u, v in itertools.combinations(node_keys, 2):
        edge = (u, v) if u < v else (v, u)
        all_edges.add(edge)

    all_x = [pos[0] for pos in node_keys]
    all_y = [pos[1] for pos in node_keys]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    range_x = (max_x - min_x) if max_x != min_x else 1
    range_y = (max_y - min_y) if max_y != min_y else 1

    padding = 80
    usable_space = window_size - (2 * padding)

    def to_screen_pos(coord):
        x, y = coord
        screen_x = padding + ((x - min_x) / range_x) * usable_space
        screen_y = window_size - (padding + ((y - min_y) / range_y) * usable_space)
        return (int(screen_x), int(screen_y))

    pixel_positions = {coord: to_screen_pos(coord) for coord in node_keys}

    pygame.init()
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Animated Graph & Tour Visualizer")
    font = pygame.font.SysFont("Arial", max(10, int(node_radius * 0.7)), bold=True)
    clock = pygame.time.Clock()

    COLOR_BG = (255, 255, 255)
    COLOR_DEFAULT_EDGE = (210, 215, 225)
    COLOR_TOUR_EDGE = (235, 60, 60)
    COLOR_NODE = (40, 115, 220)
    COLOR_TEXT = (0, 0, 0)

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

        for u, v in all_edges:
            p1 = pixel_positions[u]
            p2 = pixel_positions[v]
            pygame.draw.line(screen, COLOR_DEFAULT_EDGE, p1, p2, width=1)

        for u, v in animated_edges:
            if u in pixel_positions and v in pixel_positions:
                p1 = pixel_positions[u]
                p2 = pixel_positions[v]
                pygame.draw.line(screen, COLOR_TOUR_EDGE, p1, p2, width=4)

        for node_tuple, label in nodes.items():
            pos = pixel_positions[node_tuple]

            pygame.draw.circle(screen, COLOR_NODE, pos, node_radius)

            text_surface = font.render(str(label), True, COLOR_TEXT)
            text_rect = text_surface.get_rect(center=pos)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

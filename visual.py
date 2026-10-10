import os
import math
import pygame

DEFAULT_POSITIONS = {
    "A": (494, 71),
    "B": (669, 210),
    "C": (627, 107),
    "D": (302, 394),
    "E": (116, 394),
    "F": (151, 440),
}


def draw_arrow(screen, color, start, end, width, node_radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    tip = (end[0] - ux * node_radius, end[1] - uy * node_radius)
    base = (start[0] + ux * node_radius, start[1] + uy * node_radius)
    pygame.draw.line(screen, color, base, tip, width)
    head = 14
    left = (tip[0] - ux * head + uy * head * 0.5, tip[1] - uy * head - ux * head * 0.5)
    right = (tip[0] - ux * head - uy * head * 0.5, tip[1] - uy * head + ux * head * 0.5)
    pygame.draw.polygon(screen, color, [tip, left, right])


def visualize_tour(nodes, tour, map_path="map.PNG", positions=None, node_radius=16, step_delay_ms=900, bar_height=60):
    if not nodes or len(nodes) < 2:
        print("Need at least 2 nodes to visualize.")
        return

    positions = positions or DEFAULT_POSITIONS

    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [map_path, os.path.join(base_dir, map_path), os.path.join(base_dir, "map.png")]
    resolved = next((p for p in candidates if os.path.exists(p)), None)
    if resolved is None:
        print("Map image not found:", map_path)
        return

    pygame.init()
    map_surface = pygame.image.load(resolved)
    map_w, map_h = map_surface.get_size()
    screen = pygame.display.set_mode((map_w, map_h + bar_height))
    pygame.display.set_caption("Animated Tour Visualizer")
    map_surface = map_surface.convert()

    node_font = pygame.font.SysFont("Arial", 15, bold=True)
    label_font = pygame.font.SysFont("Arial", 13, bold=True)
    button_font = pygame.font.SysFont("Arial", 17, bold=True)
    info_font = pygame.font.SysFont("Arial", 15)
    clock = pygame.time.Clock()

    COLOR_BAR = (28, 30, 42)
    COLOR_TOUR_EDGE = (255, 90, 90)
    COLOR_NODE = (40, 115, 220)
    COLOR_NODE_ACTIVE = (255, 190, 40)
    COLOR_NODE_TEXT = (255, 255, 255)
    COLOR_LABEL_BG = (20, 22, 32)
    COLOR_LABEL_TEXT = (255, 255, 255)
    COLOR_BUTTON = (60, 130, 230)
    COLOR_BUTTON_HOVER = (85, 155, 250)
    COLOR_BUTTON_TEXT = (255, 255, 255)
    COLOR_INFO = (220, 225, 235)

    play_button = pygame.Rect(15, map_h + 12, 110, 36)
    reset_button = pygame.Rect(140, map_h + 12, 110, 36)

    total_steps = len(tour) - 1
    step = 0
    playing = False
    last_tick = pygame.time.get_ticks()

    def reset():
        nonlocal step, playing, last_tick
        step = 0
        playing = False
        last_tick = pygame.time.get_ticks()

    def toggle_play():
        nonlocal step, playing, last_tick
        if step >= total_steps:
            step = 0
        playing = not playing
        last_tick = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    toggle_play()
                elif reset_button.collidepoint(event.pos):
                    reset()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    toggle_play()
                elif event.key == pygame.K_r:
                    reset()

        now = pygame.time.get_ticks()
        if playing and now - last_tick >= step_delay_ms:
            last_tick = now
            if step < total_steps:
                step += 1
            if step >= total_steps:
                playing = False

        screen.blit(map_surface, (0, 0))

        for i in range(step):
            u, v = tour[i], tour[i + 1]
            if u != v and u in positions and v in positions:
                draw_arrow(screen, COLOR_TOUR_EDGE, positions[u], positions[v], 5, node_radius)

        current = tour[step] if step < len(tour) else None

        for node, label in nodes.items():
            pos = positions[node]
            color = COLOR_NODE_ACTIVE if node == current else COLOR_NODE
            pygame.draw.circle(screen, (255, 255, 255), pos, node_radius + 2)
            pygame.draw.circle(screen, color, pos, node_radius)
            text = node_font.render(str(node), True, COLOR_NODE_TEXT)
            screen.blit(text, text.get_rect(center=pos))

            label_surface = label_font.render(label, True, COLOR_LABEL_TEXT)
            label_rect = label_surface.get_rect(midtop=(pos[0], pos[1] + node_radius + 4))
            label_rect.clamp_ip(pygame.Rect(0, 0, map_w, map_h))
            pygame.draw.rect(screen, COLOR_LABEL_BG, label_rect.inflate(8, 4), border_radius=4)
            screen.blit(label_surface, label_rect)

        pygame.draw.rect(screen, COLOR_BAR, (0, map_h, map_w, bar_height))
        mouse = pygame.mouse.get_pos()

        play_text = "Pause" if playing else ("Replay" if step >= total_steps else "Play")
        for rect, text in ((play_button, play_text), (reset_button, "Reset")):
            color = COLOR_BUTTON_HOVER if rect.collidepoint(mouse) else COLOR_BUTTON
            pygame.draw.rect(screen, color, rect, border_radius=6)
            surface = button_font.render(text, True, COLOR_BUTTON_TEXT)
            screen.blit(surface, surface.get_rect(center=rect.center))

        route = " -> ".join(tour[: step + 1])
        info = info_font.render(f"Step {step}/{total_steps}   {route}", True, COLOR_INFO)
        screen.blit(info, (270, map_h + 21))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
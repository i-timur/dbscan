import pygame
import random
import numpy as np

MAX_DISTANCE = 50
NEIGHBOUR_GREEN = 3
NEIGHBOUR_YELLOW = 1


class DataPoint:
    x = 0
    y = 0
    is_green = False
    is_yellow = False
    is_red = False

    def __init__(self, x, y):
        self.x = x
        self.y = y


def calculate_distance(first_point, second_point):
    return np.sqrt((first_point.x - second_point.x) ** 2 + (first_point.y - second_point.y) ** 2)


def generate_nearby_points(point):
    points = [(point[0] + random.randint(-20, 20), point[1] + random.randint(-20, 20)) for _ in
              range(random.randint(2, 5))]
    return points


def assign_flags(points):
    for current_point in points:
        current_point.is_red = False
        current_point.is_green = False
        current_point.is_yellow = False

        neighbours = 0
        green_neighbours = 0
        for near_point in points:
            if current_point == near_point:
                continue

            if calculate_distance(current_point, near_point) <= MAX_DISTANCE:
                neighbours += 1
                if near_point.is_green:
                    green_neighbours += 1

        if neighbours >= NEIGHBOUR_GREEN:
            current_point.is_green = True
        elif green_neighbours == NEIGHBOUR_YELLOW:
            current_point.is_yellow = True
        elif green_neighbours == 0:
            current_point.is_red = True

    screen.fill(color='#FFFFFF')

    color_map = {
        True: {
            "is_green": 'green',
            "is_yellow": 'yellow',
            "is_red": 'red'
        },
        False: '#FFFFFF'
    }

    for point in points:
        color = next(
            (color_map[True][attr] for attr in vars(point) if attr in color_map[True] and getattr(point, attr)),
            color_map[False])
        pygame.draw.circle(screen, color, center=(point.x, point.y), radius=5)

    pygame.display.update()

    return points


def cluster_data_points(points):
    red_points = [p for p in points if p.is_red]
    other_points = [p for p in points if not p.is_red]
    visited = set(red_points)
    clusters = []

    while len(visited) < len(points):
        point = random.choice([p for p in other_points if p not in visited and not p.is_yellow])
        visited.add(point)
        cluster = [point]
        neighbors = []

        for p in other_points:
            if p in visited or p.is_red:
                continue
            if calculate_distance(point, p) <= MAX_DISTANCE:
                if p.is_yellow:
                    cluster.append(p)
                else:
                    neighbors.append(p)
                visited.add(p)

        while neighbors:
            neighbor = random.choice(neighbors)
            neighbors.remove(neighbor)
            cluster.append(neighbor)

            for p in other_points:
                if p in visited or p.is_red:
                    continue
                if calculate_distance(neighbor, p) <= MAX_DISTANCE:
                    if p.is_yellow:
                        cluster.append(p)
                    else:
                        neighbors.append(p)
                    visited.add(p)

        clusters.append(cluster)

    screen.fill(color='#FFFFFF')
    colors = ['black', 'gray', 'brown', 'orange', 'lime', 'cyan', 'blue', 'navy',
              'magenta', 'purple', 'violet', 'pink']

    for cluster in clusters:
        color = random.choice(colors)
        colors.remove(color)
        for point in cluster:
            pygame.draw.circle(screen, color=color, center=(point.x, point.y), radius=5)

    for red_point in red_points:
        pygame.draw.circle(screen, color='red', center=(red_point.x, red_point.y), radius=5)

    pygame.display.update()

    return points


def process_event(event, points, screen, is_mousebuttondown):
    center_coordinates = None
    if event.type == pygame.QUIT:
        return False, is_mousebuttondown, points

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        is_mousebuttondown = True
        center_coordinates = event.pos
        points.append(create_data_point(center_coordinates))
        draw_circle(screen, center_coordinates)

    elif event.type == pygame.MOUSEBUTTONUP:
        is_mousebuttondown = False

    elif event.type == pygame.MOUSEMOTION and is_mousebuttondown:
        new_point = create_data_point(event.pos)
        if calculate_distance(new_point, points[-1]) > 20:
            center_coordinates = event.pos
            draw_circle(screen, center_coordinates)
            points.append(create_data_point(center_coordinates))
            draw_nearby_points(points, screen, center_coordinates)

    elif event.type == pygame.KEYUP:
        if event.key == 114:
            points = []
            screen.fill(color='#FFFFFF')
        elif event.key == 115:
            points = assign_flags(points)
        elif event.key == 99:
            points = cluster_data_points(points)

    pygame.display.update()
    return True, is_mousebuttondown, points


def draw_circle(screen, center):
    pygame.draw.circle(screen, color='black', center=center, radius=5)


def draw_nearby_points(points, screen, center_coordinates):
    random_points = generate_nearby_points(center_coordinates)
    for coords in random_points:
        pygame.draw.circle(screen, color='black', center=coords, radius=5)
        point_to_append = create_data_point(coords)
        points.append(point_to_append)


def create_data_point(center_coordinates):
    return DataPoint(center_coordinates[0], center_coordinates[1])


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1024, 720), pygame.RESIZABLE)
    screen.fill(color='#FFFFFF')
    pygame.display.update()

    is_active = True
    is_mousebuttondown = False
    points = []
    while is_active:
        for event in pygame.event.get():
            is_active, is_mousebuttondown, points = process_event(event, points, screen, is_mousebuttondown)

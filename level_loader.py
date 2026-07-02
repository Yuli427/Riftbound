import csv
import pygame
import Constants as cons
from World import World


def create_empty_grid():
    return [[-1] * cons.COLUMN for _ in range(cons.ROWS)]


def read_csv(path):
    data = create_empty_grid()

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for y, row in enumerate(reader):
            for x, tile in enumerate(row):
                data[y][x] = int(tile)

    return data


def load_tile_images(level):
    tile_list = []

    if level == '1':
        for x in range(cons.TILE_TYPES):
            tile_image = pygame.image.load(
                f'assets/level1_background_tile/Tile_{x + 1:02d}.png'
            ).convert_alpha()
            tile_list.append(tile_image)

    elif level == '2':
        for x in range(cons.TILE_TYPES):
            tile_image = pygame.image.load(
                f'assets/level2_background_tile/Tiles_{x + 1:02d}.png'
            ).convert_alpha()
            tile_list.append(tile_image)

    else:
        for x in range(cons.TILE_TYPES):
            tile_image = pygame.image.load(
                f'assets/level3_background_tile/Tile_{x + 1:02d}.png'
            ).convert_alpha()
            tile_list.append(tile_image)

    return tile_list


def load_object_tile_images(level):
    obj_tile_list = []

    if level == '1':
        for x in range(26):
            tile_image = pygame.image.load(
                f'assets/level1_obj_tile/{x + 1}.png'
            ).convert_alpha()
            obj_tile_list.append(tile_image)

    elif level == '2':
        for x in range(26):
            tile_image = pygame.image.load(
                f'assets/level2_obj_tile/{x}.png'
            ).convert_alpha()
            obj_tile_list.append(tile_image)

    else:
        for x in range(41):
            tile_image = pygame.image.load(
                f'assets/level3_obj_tile/{x + 1}.png'
            ).convert_alpha()
            obj_tile_list.append(tile_image)

    return obj_tile_list


def load_level_data(level):
    if level == '1':
        world_data = read_csv('levels/l1/level1_background.csv')
        platform_data = read_csv('levels/l1/level1_Platform.csv')
        object_data = read_csv('levels/l1/level1_Objects.csv')
        layer_data = create_empty_grid()

    elif level == '2':
        world_data = read_csv('levels/l2/level2_background.csv')
        platform_data = read_csv('levels/l2/level2_Platform.csv')
        object_data = read_csv('levels/l2/level2_Objects.csv')
        layer_data = read_csv('levels/l2/level2_layer.csv')

    else:
        world_data = read_csv('levels/l3/level3_background.csv')
        platform_data = read_csv('levels/l3/level3_Platform.csv')
        object_data = read_csv('levels/l3/level3_Objects.csv')
        layer_data = create_empty_grid()

    return world_data, layer_data, object_data, platform_data


def build_spawn_tiles(world):
    spawn_tile = []

    tile_set = {(tile.centerx, tile.top) for tile in world.obstacle_tiles}

    for tile in world.obstacle_tiles:
        cx = tile.centerx
        top = tile.top

        left1 = (cx - cons.TILE_SIZE, top) in tile_set
        right1 = (cx + cons.TILE_SIZE, top) in tile_set

        if left1 and right1:
            spawn_tile.append((tile.centerx, tile.top - cons.ENEMY_HEIGHT))

    return spawn_tile


def build_tornado_spawn_tiles(world):
    tornado_spawn_tile = []

    tile_set = {(tile.centerx, tile.top) for tile in world.obstacle_tiles}

    for tile in world.obstacle_tiles:
        cx = tile.centerx
        top = tile.top

        left1 = (cx - cons.TILE_SIZE, top) in tile_set
        left2 = (cx - cons.TILE_SIZE * 2, top) in tile_set
        left3 = (cx - cons.TILE_SIZE * 3, top) in tile_set

        right1 = (cx + cons.TILE_SIZE, top) in tile_set
        right2 = (cx + cons.TILE_SIZE * 2, top) in tile_set
        right3 = (cx + cons.TILE_SIZE * 3, top) in tile_set

        right_ok = right1 and right2 and right3
        left_ok = left1 and left2 and left3

        if right_ok and left_ok:
            tornado_spawn_tile.append((tile.centerx, tile.top))

    return tornado_spawn_tile


def load_level_world(level):
    tile_list = load_tile_images(level)
    obj_tile_list = load_object_tile_images(level)

    world_data, layer_data, object_data, platform_data = load_level_data(level)

    world = World()
    world.process_data(
        world_data,
        layer_data,
        object_data,
        platform_data,
        tile_list,
        obj_tile_list,
        level == '2',
        level == '1'
    )

    spawn_tile = build_spawn_tiles(world)
    tornado_spawn_tile = build_tornado_spawn_tiles(world)

    return {
        "world": world,
        "world_data": world_data,
        "layer_data": layer_data,
        "object_data": object_data,
        "platform_data": platform_data,
        "tile_list": tile_list,
        "obj_tile_list": obj_tile_list,
        "spawn_tile": spawn_tile,
        "tornado_spawn_tile": tornado_spawn_tile,
    }
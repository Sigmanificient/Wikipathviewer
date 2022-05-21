import asyncio
from typing import Dict, Tuple, List, Any

from db import db


class Point:

    def __init__(self, id_: int, url: str):
        self.id_ = id_
        self.url = url
        self.relations = []

    def __repr__(self):
        return self.url


async def find_paths(
        start: Point, end: Point,
        points: List[Point],
        depth: int = 0,
        path: List[Point] = None,
        paths: List[List[Point]] = None
) -> List[List[Point]]:
    if depth > 2:
        return []

    if path is None:
        path = [start]

    if paths is None:
        paths = []

    possible_paths = []
    for point_id in start.relations:
        point = points[point_id - 1]

        if point.id_ == end.id_:
            possible_paths.extend([path + [end]])
            continue

        await find_paths(
            point, end, points, depth + 1, path + [point], paths
        )

    if possible_paths:
        paths.extend(possible_paths)

    return paths


async def main():
    if not await db.init():
        print('db init failed')
        return

    links = dict(await db.fetchall("SELECT id, url FROM Point"))
    links_relations = await db.fetchall("SELECT link_from, link_to FROM LinkRelation")

    print(links_relations)

    points = [Point(id_, url) for id_, url in links.items()]
    for point_form, point_to in links_relations:
        points[point_form - 1].relations.append(point_to)

    paths = await find_paths(points[0], points[-1], points)
    print('paths =>', ', '.join(''.join(map(str, path)) for path in paths))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

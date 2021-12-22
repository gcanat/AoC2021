import numpy as np


def one_step(probe):
    probe['x_pos'] += probe['x_vel']
    probe['y_pos'] += probe['y_vel']
    if probe['x_vel'] > 0:
        probe['x_vel'] -= 1
    elif probe['x_vel'] < 0:
        probe['x_vel'] += 1
    probe['y_vel'] -= 1
    return probe


def check_pos(probe, target):
    # check if we are inside target area
    if (probe['x_pos'] >= target['x_min']) and (probe['x_pos'] <= target['x_max']) and (
            probe['y_pos'] >= target['y_min']) and (probe['y_pos'] <= target['y_max']):
        return "Inside target"
    elif (probe['x_pos'] > target['x_max']) or (probe['y_pos'] < target['y_min']):
        # print(f"Missed target: position {probe['pos']}, velocity {probe['vel']}")
        return "Missed target"
    else:
        return "Still on course"


def shoot_probe(probe, target):
    # result = check_pos(probe, target)
    result = "Still on course"
    trajectory = []
    while result == "Still on course":
        probe = one_step(probe)
        trajectory.append((probe['x_pos'], probe['y_pos']))
        result = check_pos(probe, target)
    if result == "Inside target":
        return "Success", trajectory
    else:
        return "Failure", trajectory


if __name__ == "__main__":
    # input = "target area: x=169..206, y=-108..-68"
    success_probes = []
    target = {}
    target['x_min'] = 169
    target['x_max'] = 206
    target['y_min'] = -108
    target['y_max'] = -68
    for x_vel in range(1, 210):
        for y_vel in range(-200, 200):
            probe = {}
            probe['x_pos'] = 0
            probe['y_pos'] = 0
            probe['x_vel'] = x_vel
            probe['y_vel'] = y_vel
            probe_result, trajectory = shoot_probe(probe, target)
            if probe_result == "Success":
                success_probes.append(trajectory)
    max_y = 0
    for traject in success_probes:
        for pos in traject:
            if pos[1] > max_y:
                max_y = pos[1]
    print("Part 1 answer:", max_y)
    print("Part 2 answer:", len(success_probes))

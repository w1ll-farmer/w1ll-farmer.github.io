def build_cost_matrix(preferences, riggedPerson="annabel", rigged=True):
    allocation = {}

    if rigged:
        allocation[riggedPerson] = preferences[riggedPerson][0]
        rigged_room = allocation[riggedPerson]

        del preferences[riggedPerson]

        for key in preferences:
            preferences[key] = [room for room in preferences[key] if room != rigged_room]
    else:
        rigged_room = None

    people = list(preferences.keys())

    # Gather all rooms from remaining preferences
    all_rooms = set()
    for prefs in preferences.values():
        all_rooms.update(prefs)
    if rigged_room:
        all_rooms.discard(rigged_room)

    all_rooms = sorted(all_rooms)  # consistent room order
    room_indices = {room: i for i, room in enumerate(all_rooms)}

    # Build base cost matrix
    cost_matrix = []
    for person in people:
        row = [100] * len(all_rooms)
        for rank, room in enumerate(preferences[person]):
            if room in room_indices:
                col = room_indices[room]
                row[col] = rank + 1
        cost_matrix.append(row)

    # If fewer people than rooms, pad with dummy people (high cost)
    n = len(all_rooms)
    while len(cost_matrix) < n:
        cost_matrix.append([100] * n)

    return cost_matrix, people, all_rooms, allocation

from scipy.optimize import linear_sum_assignment

prefs = {
    'annabel': ['room1', 'room2', 'room3', 'room4'],
    'bob': ['room1', 'room3', 'room2'],
    'claire': ['room1', 'room3', 'room4']
}

matrix, people, rooms, allocation = build_cost_matrix(prefs.copy(), "annabel", rigged=True)
row_ind, col_ind = linear_sum_assignment(matrix)

for i, j in zip(row_ind, col_ind):
    if i < len(people):  # skip dummy rows
        allocation[people[i]] = rooms[j]

print("Final Allocation:", allocation)

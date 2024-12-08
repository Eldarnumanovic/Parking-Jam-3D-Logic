examples = [
    # Winning Examples
    {
        "size": 10,
        "car_list": [
            (1, 0, 0, 'EW'),
            (2, 9, 9, 'NS'),
            (3, 4, 5, 'NS'),
            (4, 7, 2, 'EW'),
            (5, 1, 8, 'EW')
        ],
        "barrier_list": [
            (0, 1), (1, 1), (2, 2), (8, 8), (6, 6), (3, 4), (9, 0), (5, 9)
        ]
    },
    {
        "size": 12,
        "car_list": [
            (1, 1, 1, 'EW'),
            (2, 2, 3, 'NS'),
            (3, 5, 5, 'EW'),
            (4, 9, 10, 'NS'),
            (5, 10, 8, 'EW'),
            (6, 7, 3, 'NS'),
            (7, 11, 11, 'EW')
        ],
        "barrier_list": [
            (0, 0), (3, 3), (4, 4), (6, 6), (8, 8), (9, 9), (5, 1), (1, 8), (10, 10), (2, 6)
        ]
    },
    {
        "size": 15,
        "car_list": [
            (1, 0, 0, 'EW'),
            (2, 0, 14, 'EW'),
            (3, 14, 0, 'NS'),
            (4, 14, 14, 'NS'),
            (5, 7, 7, 'EW'),
            (6, 5, 5, 'NS'),
            (7, 9, 9, 'EW')
        ],
        "barrier_list": [
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (10, 10), (11, 11), (12, 12), (13, 13), (8, 8)
        ]
    },
    {
        "size": 20,
        "car_list": [
            (1, 10, 0, 'NS'),
            (2, 5, 2, 'NS'),
            (3, 14, 7, 'NS'),
            (4, 3, 15, 'NS'),
            (5, 8, 10, 'NS'),
            (6, 1, 12, 'NS'),
            (7, 6, 18, 'NS'),
            (8, 11, 5, 'NS')
        ],
        "barrier_list": [
            (0, 0), (1, 1), (5, 5), (10, 10), (15, 15), (19, 19), (8, 8), (3, 3), (7, 7), (13, 13)
        ]
    },
    {
        "size": 25,
        "car_list": [
            (1, 0, 0, 'EW'),
            (2, 24, 24, 'NS'),
            (3, 12, 12, 'NS'),
            (4, 6, 10, 'EW'),
            (5, 18, 5, 'NS'),
            (6, 20, 18, 'EW'),
            (7, 3, 22, 'NS')
        ],
        "barrier_list": [
            (1, 1), (2, 2), (4, 4), (5, 5), (6, 6), (9, 9), (11, 11), (13, 13), (16, 16), (20, 20),
            (21, 21), (22, 22), (23, 23), (24, 24)
        ]
    },
    # Losing Examples
    {
        "size": 5,
        "car_list": [
            (1, 2, 2, 'EW')  # Car 1 is completely blocked
        ],
        "barrier_list": [
            (1, 2),  # Barrier to the left of the car
            (3, 2),  # Barrier to the right of the car
            (2, 1),  # Barrier above the car
            (2, 3)   # Barrier below the car
        ]
    },
    {
        "size": 6,
        "car_list": [
            (1, 3, 3, 'NS'),  # Car 1 is vertically blocked
            (2, 4, 2, 'EW')   # Car 2 is horizontally blocked
        ],
        "barrier_list": [
            (3, 2), (3, 4),  # Barriers blocking Car 1 vertically
            (2, 2), (5, 2)   # Barriers blocking Car 2 horizontally
        ]
    },
    {
        "size": 10,
        "car_list": [
            (1, 4, 4, 'NS'),  # Car 1 cannot move up or down
            (2, 6, 6, 'EW')   # Car 2 cannot move left or right
        ],
        "barrier_list": [
            (4, 3), (4, 5),  # Barriers blocking Car 1 vertically
            (5, 6), (7, 6)   # Barriers blocking Car 2 horizontally
        ]
    },
    {
        "size": 8,
        "car_list": [
            (1, 0, 0, 'EW'),  # Car 1 is trapped in the corner
            (2, 7, 7, 'NS')   # Car 2 is trapped in the opposite corner
        ],
        "barrier_list": [
            (1, 0), (0, 1),  # Barriers around Car 1
            (6, 7), (7, 6)   # Barriers around Car 2
        ]
    },
    {
        "size": 12,
        "car_list": [
            (1, 6, 6, 'EW'),  # Car 1 is surrounded by barriers
            (2, 5, 5, 'NS')   # Car 2 is surrounded by barriers
        ],
        "barrier_list": [
            (5, 6), (7, 6),  # Barriers on either side of Car 1
            (6, 5), (6, 7),  # Barriers on either side of Car 2
            (5, 5), (5, 7), (7, 5), (7, 7)  # Extra barriers around the cluster
        ]
    }
]

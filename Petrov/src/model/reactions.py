from .state import State

def get_reactions(N, qx, qy, Zx, Zy):
    return [
        {
            'name': 'cix',
            'guard': lambda s: s.x > 0 and s.y > 0 and s.u < N,
            'rate': lambda s: qx * s.x * s.y,
            'delta': lambda s: State(s.x, s.y - 1, s.u + 1)
        },
        {
            'name': 'ciy',
            'guard': lambda s: s.x > 0 and s.x < N and s.u > 0,
            'rate': lambda s: qy * s.x * s.y,
            'delta': lambda s: State(s.x - 1, s.y, s.u + 1)
        },
        {
            'name': 'rx',
            'guard': lambda s: s.x > 0 and s.x < N and s.u > 0,
            'rate': lambda s: qy * s.x * s.y,
            'delta': lambda s: State(s.x + 1, s.y, s.u - 1)
        },
        {
            'name': 'ry',
            'guard': lambda s: s.y > 0 and s.y < N and s.u > 0,
            'rate': lambda s: qy * s.x * s.y,
            'delta': lambda s: State(s.x, s.y + 1, s.u - 1)
        },
        {
            'name': 'zeaxa',
            'guard': lambda s: s.y > 0 and s.u < N and Zx > 0,
            'rate': lambda s: qx * s.y * Zx,
            'delta': lambda s: State(s.x, s.y - 1, s.u + 1)
        },
        {
            'name': 'zeaxb',
            'guard': lambda s: s.u > 0 and s.x < N and Zx > 0,
            'rate': lambda s: qx * s.u * Zx,
            'delta': lambda s: State(s.x + 1, s.y, s.u - 1)
        },
        {
            'name': 'zeaya',
            'guard': lambda s: s.x > 0 and s.u < N and Zy > 0,
            'rate': lambda s: qy * s.y * Zy,
            'delta': lambda s: State(s.x - 1, s.y, s.u + 1)
        },
        {
            'name': 'zeayb',
            'guard': lambda s: s.u > 0 and s.y < N and Zy > 0,
            'rate': lambda s: qy * s.u * Zy,
            'delta': lambda s: State(s.x, s.y + 1, s.u - 1)
        }
    ]


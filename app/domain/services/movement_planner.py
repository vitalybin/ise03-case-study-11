from app.domain.entities.vehicle import Direction, MovementStep


class MovementPlanner:
    """
    Übersetzt grobe Schritt-Kommandos in konkrete API-Aktionen.
    Da die Fremd-API keine direkte 'move one step'-Funktion anbietet,
    approximieren wir Schritte über Throttle/Steer + Zeit.
    """

    def plan(self, direction: Direction, step_percent: int = 18, duration_ms: int = 450) -> list[MovementStep]:
        step_percent = max(1, min(100, step_percent))
        duration_ms = max(100, min(5000, duration_ms))

        if direction == Direction.FORWARD:
            return [
                MovementStep(throttle=step_percent, steer=0, duration_ms=duration_ms),
                MovementStep(throttle=0, steer=0, duration_ms=0),
            ]
        if direction == Direction.BACKWARD:
            return [
                MovementStep(throttle=-step_percent, steer=0, duration_ms=duration_ms),
                MovementStep(throttle=0, steer=0, duration_ms=0),
            ]
        if direction == Direction.LEFT:
            return [
                MovementStep(throttle=max(8, step_percent // 2), steer=-35, duration_ms=duration_ms),
                MovementStep(throttle=0, steer=0, duration_ms=0),
            ]
        if direction == Direction.RIGHT:
            return [
                MovementStep(throttle=max(8, step_percent // 2), steer=35, duration_ms=duration_ms),
                MovementStep(throttle=0, steer=0, duration_ms=0),
            ]

        raise ValueError(f'Unsupported direction: {direction}')

class Servo:
    def __init__(self, pin, freq=50, min_us=500, max_us=2500, angle_range=180):
        self.pin = pin
        self.freq = freq
        self.min_us = min_us
        self.max_us = max_us
        self.angle_range = angle_range
        self._angle = 0  # current angle
        self._pulse_us = self._angle_to_us(0)
        print(f"[INIT] Servo(pin={pin}, freq={freq}Hz) initialized.")

    def _angle_to_us(self, angle):
        return self.min_us + (angle / self.angle_range) * (self.max_us - self.min_us)

    def write_angle(self, angle):
        angle = max(0, min(self.angle_range, angle))
        self._angle = angle
        self._pulse_us = self._angle_to_us(angle)
        print(f"[WRITE] Angle set to {angle}° → pulse {self._pulse_us:.1f}μs")

    def write_us(self, us):
        us = max(self.min_us, min(self.max_us, us))
        self._pulse_us = us
        self._angle = ((us - self.min_us) * self.angle_range) / (self.max_us - self.min_us)
        print(f"[WRITE] Pulse width set to {us}μs → angle {self._angle:.1f}°")

    def get_state(self):
        return {
            "pin": self.pin,
            "angle": self._angle,
            "pulse_us": self._pulse_us,
        }

    def deinit(self):
        print(f"[DEINIT] Servo(pin={self.pin}) deinitialized.")

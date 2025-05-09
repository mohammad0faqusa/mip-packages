import time

class MethodWrapper:
    def __init__(self, func):
        self.func = func

    def __getitem__(self, args):
        if isinstance(args, (list, tuple)):
            return self.func(*args)  # Unpack!
        else:
            return self.func(args)


class PushButton:
    def __init__(self, pin, simulate=True, debounce_ms=50):
        self.pin = pin
        self.simulate = simulate
        self.debounce_ms = debounce_ms
        self._last_state = False
        self._last_time = time.ticks_ms()
        self._simulated_state = False  # Controlled manually by the user
        self.was_pressed = False

        if not self.simulate:
            from machine import Pin
            self._btn = Pin(pin, Pin.IN, Pin.PULL_UP)

        print(f"[INIT] PushButton on pin {pin} (simulate={simulate}, debounce={debounce_ms}ms)")

    def __getitem__(self, key):
        method = getattr(self, key)
        return MethodWrapper(method)

    def set_simulated_state(self, pressed: bool):
        """Only used in simulate=True mode to mock button press."""
        if self.simulate:
            self._simulated_state = pressed
            print(f"[SIM SET] PushButton state set to: {'PRESSED' if pressed else 'RELEASED'}")

    def is_pressed(self):
        current_time = time.ticks_ms()

        if self.simulate:
            current_state = self._simulated_state
        else:
            current_state = not self._btn.value()  # Active LOW logic

        # Debounce logic
        if current_state != self._last_state:
            if time.ticks_diff(current_time, self._last_time) > self.debounce_ms:
                self._last_time = current_time
                self._last_state = current_state
                self.was_pressed = True
                print(f"[DETECTED] Button {'PRESSED' if current_state else 'RELEASED'}")

        return self._last_state
    
    def push(self):
        self.set_simulated_state(True)
        self.is_pressed()
        self.set_simulated_state(False)
        self.is_pressed()
    
    def get_event(self):
        """Returns and clears the was_pressed flag."""
        if self.was_pressed: 
            self.was_pressed = False
            return True
        return False


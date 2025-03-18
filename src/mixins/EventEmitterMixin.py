from typing import Callable, Dict

class EventEmitterMixin:
    def __init__(self):
        self._event_listeners: Dict[str, list] = {}

    def on(self, event_name: str) -> Callable:
        """Decorator for registering an event listener."""
        def decorator(func: Callable) -> Callable:
            if event_name not in self._event_listeners:
                self._event_listeners[event_name] = []
            self._event_listeners[event_name].append(func)
            return func
        return decorator

    def _emit_event(self, event_name: str, data: dict) -> None:
        """Emit an event to the registered listeners."""
        if event_name in self._event_listeners:
            for listener in self._event_listeners[event_name]:
                listener(data)
        else:
            print(f"Warning: No listeners for event '{event_name}'.")

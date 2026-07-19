import math
import time


class EventTracker:
    """
    Tracks active survivor/fire events and avoids creating duplicate events
    for nearby detections.
    """

    def __init__(self):
        # Stores all active events
        self.active_events = {}

        # Counter for generating unique event IDs
        self.next_event_id = 1

        # Maximum distance (meters/units) before considering it a new event
        self.distance_threshold = 5.0

        # Remove events not updated for this many seconds
        self.timeout = 30

    def calculate_distance(self, coords1, coords2):
        """
        Calculate Euclidean distance between two 3D coordinates.
        """

        return math.sqrt(
            (coords1[0] - coords2[0]) ** 2 +
            (coords1[1] - coords2[1]) ** 2 +
            (coords1[2] - coords2[2]) ** 2
        )

    def find_existing_event(self, event_type, coords):
        """
        Search for an existing nearby event of the same type.
        Returns event_id if found, otherwise None.
        """

        for event_id, event in self.active_events.items():

            if event["event_type"] != event_type:
                continue

            distance = self.calculate_distance(coords, event["coords"])

            if distance <= self.distance_threshold:
                return event_id

        return None

    def cleanup_old_events(self):
        """
        Remove events that have not been updated recently.
        """

        current_time = time.time()

        expired = []

        for event_id, event in self.active_events.items():

            if current_time - event["last_seen"] > self.timeout:
                expired.append(event_id)

        for event_id in expired:
            del self.active_events[event_id]

    def update(self, payload):
        """
        Process a telemetry payload.

        Input:
        {
            "drone_id":1,
            "timestamp":...,
            "coords":[x,y,z],
            "human_detected":True,
            "fire_detected":False
        }

        Returns the same payload with event information attached.
        """

        self.cleanup_old_events()

        # Decide which event type this detection represents
        if payload["human_detected"]:
            event_type = "human"

        elif payload["fire_detected"]:
            event_type = "fire"

        else:
            payload["event_id"] = None
            payload["event_type"] = None
            return payload

        coords = payload["coords"]

        existing_event = self.find_existing_event(event_type, coords)

        # Existing event found
        if existing_event is not None:

            self.active_events[existing_event]["coords"] = coords
            self.active_events[existing_event]["last_seen"] = time.time()
            self.active_events[existing_event]["drone_id"] = payload["drone_id"]

            payload["event_id"] = existing_event
            payload["event_type"] = event_type

            return payload

        # Create new event
        event = {
            "event_id": self.next_event_id,
            "event_type": event_type,
            "coords": coords,
            "drone_id": payload["drone_id"],
            "created_at": time.time(),
            "last_seen": time.time()
        }

        self.active_events[self.next_event_id] = event

        payload["event_id"] = self.next_event_id
        payload["event_type"] = event_type

        self.next_event_id += 1

        return payload

    def get_active_events(self):
        """
        Return all active tracked events.
        """

        self.cleanup_old_events()

        return list(self.active_events.values())

    def print_active_events(self):
        """
        Print active events for debugging.
        """

        print("\n========== ACTIVE EVENTS ==========")

        if not self.active_events:
            print("No active events.")

        for event in self.active_events.values():
            print(event)

        print("===================================\n")
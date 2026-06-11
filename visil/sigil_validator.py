from datetime import datetime


class SigilValidator:

    # -------------------------
    # ENTRY POINT
    # -------------------------
    def validate(self, event):

        self._validate_base(event)
        self._validate_timestamp(event)
        self._validate_type(event)

        if event["type"] == "add":
            self._validate_node(event.get("node"))

        if event["type"] == "update":
            self._validate_node(event.get("node"))

        if event["type"] == "connect":
            self._validate_edge(event.get("edge"))

        return True

    # -------------------------
    # BASE STRUCTURE
    # -------------------------
    def _validate_base(self, event):
        required = ["id", "timestamp", "type"]

        for r in required:
            if r not in event:
                raise ValueError(f"Missing field: {r}")

    # -------------------------
    # TIMESTAMP RULE
    # -------------------------
    def _validate_timestamp(self, event):
        try:
            datetime.fromisoformat(event["timestamp"].replace("Z", ""))
        except:
            raise ValueError("Invalid timestamp format")

    # -------------------------
    # EVENT TYPE RULE
    # -------------------------
    def _validate_type(self, event):

        valid_types = ["add", "update", "connect"]

        if event["type"] not in valid_types:
            raise ValueError(f"Invalid event type: {event['type']}")

    # -------------------------
    # NODE RULES
    # -------------------------
    def _validate_node(self, node):

        if not node:
            raise ValueError("Missing node payload")

        if "id" not in node:
            raise ValueError("Node missing id")

        if "timestamp" not in node:
            raise ValueError("Node missing timestamp")

        if "concepts" not in node:
            raise ValueError("Node missing concepts")

        if not isinstance(node["concepts"], list):
            raise ValueError("Node concepts must be list")

    # -------------------------
    # EDGE RULES
    # -------------------------
    def _validate_edge(self, edge):

        if not edge:
            raise ValueError("Missing edge payload")

        if "from" not in edge or "to" not in edge:
            raise ValueError("Edge must have from/to")

        if edge["from"] == edge["to"]:
            raise ValueError("Self-referencing edges not allowed")

    # -------------------------
    # SAFE WRAP
    # -------------------------
    def safe_validate(self, event):

        try:
            return self.validate(event)
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "event_id": event.get("id")
            }

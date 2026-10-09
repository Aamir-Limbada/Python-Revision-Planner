from datetime import datetime


class Topic:
    def __init__(self, name, category, confidence=3):
        self.name = name
        self.category = category
        self.confidence = confidence
        self.sessions = []
        self.created = datetime.now()

    def update_confidence(self, new_confidence):
        if not 1 <= new_confidence <= 5:
            raise ValueError("Confidence must be between 1 and 5.")

        self.confidence = new_confidence

    def record_session(self, attempted, correct, confidence):
        if attempted < 1:
            raise ValueError("You must attempt at least one question.")

        if not 0 <= correct <= attempted:
            raise ValueError(
                "Correct answers must be between zero and attempted."
            )

        if not 1 <= confidence <= 5:
            raise ValueError("Confidence must be between 1 and 5.")

        session = {
            "date": datetime.now(),
            "attempted": attempted,
            "correct": correct,
            "confidence": confidence,
        }

        self.sessions.append(session)
        self.confidence = confidence

    def get_accuracy(self):
        total_attempted = sum(
            session["attempted"] for session in self.sessions
        )

        total_correct = sum(
            session["correct"] for session in self.sessions
        )

        if total_attempted == 0:
            return 0.0

        return (total_correct / total_attempted) * 100

    def get_session_count(self):
        return len(self.sessions)
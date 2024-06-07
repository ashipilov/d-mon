class Cancellation:
    is_requested = False

    def request_cancellation(self):
        self.is_requested = True

cancellation = Cancellation()
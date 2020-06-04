import logging


class ReaderTracker:
    max_depth = None
    current_depth = 0
    logger = None

    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        self.logger = logging.getLogger("PocketFurnace")

    def protect_depth(self, execute):
        self.current_depth += 1
        if 0 < self.max_depth < self.current_depth:
            logging.error(f"Nesting level too deep: reached max depth of {self.max_depth} tags")
            raise ValueError

        try:
            execute()
        finally:
            self.current_depth -= 1

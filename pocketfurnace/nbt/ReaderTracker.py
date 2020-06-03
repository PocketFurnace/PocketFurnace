class ReaderTracker:
    maxDepth = None
    currentDepth = 0

    def __init__(self, maxDepth: int):
        self.maxDepth = maxDepth

    def protectDepth(self, execute):
        self.currentDepth += 1
        if 0 < self.maxDepth < self.currentDepth:
            print("[PocketFurnace]: Nesting level too deep: reached max depth of "+str(self.maxDepth)+" tags")

        try:
            execute()
        finally:
            self.currentDepth -= 1


from concurrent.futures import ThreadPoolExecutor

class InferenceScheduler(ThreadPoolExecutor):
    def __init__(self, max_worker=None):
        super().__init__(max_workers=max_worker)
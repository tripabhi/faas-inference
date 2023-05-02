from concurrent.futures import ProcessPoolExecutor

class InferenceScheduler(ProcessPoolExecutor):
    def __init__(self, max_worker=None):
        # Only supported in Python 3.11
        # super().__init__(max_workers=max_worker, max_tasks_per_child=None)
        super().__init__(max_workers=max_worker)
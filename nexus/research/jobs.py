from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from threading import Lock
from uuid import uuid4


@dataclass
class ResearchJob:
    job_id: str
    status: str
    error: str = ""
    result: dict | None = None


class ResearchJobManager:
    """Small in-process async job manager; replaceable by a distributed queue later."""

    def __init__(self, max_workers: int = 2):
        self.executor = ThreadPoolExecutor(max_workers=max(1, min(max_workers, 4)))
        self.jobs: dict[str, ResearchJob] = {}
        self._lock = Lock()

    def submit(self, fn, *args, **kwargs) -> ResearchJob:
        job = ResearchJob(uuid4().hex, "running")
        with self._lock:
            self.jobs[job.job_id] = job
        try:
            future = self.executor.submit(fn, *args, **kwargs)
        except Exception as exc:
            with self._lock:
                job.status = "failed"
                job.error = str(exc)
            return job
        future.add_done_callback(lambda f: self._finish(job.job_id, f))
        return job

    def _finish(self, job_id: str, future: Future):
        with self._lock:
            job = self.jobs[job_id]
            try:
                job.result = future.result()
                job.status = "completed"
            except Exception as exc:
                job.error = str(exc)
                job.status = "failed"

    def get(self, job_id: str) -> ResearchJob | None:
        with self._lock:
            return self.jobs.get(job_id)

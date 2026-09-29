import time

from nexus.research.jobs import ResearchJobManager


def test_job_manager_completes():
    manager = ResearchJobManager(max_workers=1)
    job = manager.submit(lambda: {"ok": True})
    for _ in range(50):
        current = manager.get(job.job_id)
        if current.status == "completed":
            assert current.result == {"ok": True}
            return
        time.sleep(0.01)
    raise AssertionError("job did not complete")

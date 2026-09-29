from nexus.research.acquisition import AcquisitionManager
from nexus.research.providers import StaticURLProvider


class ResearchAcquisitionController:
    """Runs bounded external acquisition before the normal research engine."""

    def __init__(self, engine, acquisition_manager: AcquisitionManager):
        self.engine = engine
        self.acquisition_manager = acquisition_manager

    def run(self, question: str, source_urls: list[str] | None = None, max_sources: int = 5, **options):
        acquisition = None
        if source_urls:
            provider = StaticURLProvider(source_urls)
            candidates = provider.search(question, limit=max_sources)
            acquisition = self.acquisition_manager.acquire(candidates, max_sources=max_sources)
        context = self.engine.run(question, **options)
        context.state["acquisition"] = {
            "requested": acquisition.requested if acquisition else 0,
            "acquired": acquisition.acquired if acquisition else 0,
            "skipped": acquisition.skipped if acquisition else 0,
            "failed": acquisition.failed if acquisition else 0,
            "sources": [source.__dict__ for source in acquisition.sources] if acquisition else [],
            "errors": list(acquisition.errors) if acquisition else [],
        }
        return context

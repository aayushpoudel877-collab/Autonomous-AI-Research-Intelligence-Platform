from nexus.research.acquisition import AcquisitionManager
from nexus.research.evidence import EvidenceController
from nexus.research.providers import StaticURLProvider


class ResearchAcquisitionController:
    """Runs bounded acquisition and an auditable evidence stopping policy."""

    def __init__(self, engine, acquisition_manager: AcquisitionManager):
        self.engine = engine
        self.acquisition_manager = acquisition_manager
        self.evidence_controller = EvidenceController()

    def run(
        self,
        question: str,
        source_urls: list[str] | None = None,
        max_sources: int = 5,
        target_evidence: int = 5,
        target_sources: int = 2,
        min_average_score: float = 0.15,
        max_age_days: float = 1.0,
        force_refresh: bool = False,
        **options,
    ):
        acquisition = None
        if source_urls:
            provider = StaticURLProvider(source_urls)
            candidates = provider.search(question, limit=max_sources)
            acquisition = self.acquisition_manager.acquire(
                candidates,
                max_sources=max_sources,
                max_age_days=max_age_days,
                force_refresh=force_refresh,
            )

        context = self.engine.run(question, **options)
        assessment = self.evidence_controller.assess(
            context.evidence,
            target_evidence=target_evidence,
            target_sources=target_sources,
            min_average_score=min_average_score,
        )
        context.state["evidence_assessment"] = assessment.__dict__
        context.state["acquisition"] = {
            "requested": acquisition.requested if acquisition else 0,
            "acquired": acquisition.acquired if acquisition else 0,
            "skipped": acquisition.skipped if acquisition else 0,
            "cached": acquisition.cached if acquisition else 0,
            "failed": acquisition.failed if acquisition else 0,
            "sources": [source.__dict__ for source in acquisition.sources] if acquisition else [],
            "errors": list(acquisition.errors) if acquisition else [],
        }
        return context

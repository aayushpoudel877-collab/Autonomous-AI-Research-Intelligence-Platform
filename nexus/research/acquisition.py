from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime

from nexus.ingestion.registry import get_ingestor
from nexus.research.dedup import SourceDeduplicator, content_hash
from nexus.research.quality import SourceQualityScorer
from nexus.research.registry import SourceRegistry
from nexus.research.sources import AcquiredSource, SourceCandidate, canonicalize_url


@dataclass(frozen=True)
class AcquisitionResult:
    requested: int
    acquired: int
    skipped: int
    cached: int
    failed: int
    sources: tuple[AcquiredSource, ...]
    errors: tuple[dict[str, str], ...]


class AcquisitionManager:
    def __init__(self, index_pipeline, storage=None, max_workers: int = 4):
        self.index_pipeline = index_pipeline
        self.storage = storage
        self.max_workers = max(1, min(max_workers, 8))
        self.quality = SourceQualityScorer()
        self.deduplicator = SourceDeduplicator()
        self.registry = SourceRegistry(storage) if storage else None

    def _fetch(self, candidate: SourceCandidate):
        canonical = canonicalize_url(candidate.url)
        document = get_ingestor("url").ingest(canonical)
        fetched_at = datetime.now(UTC).isoformat()
        return candidate, canonical, document, fetched_at

    def acquire(
        self,
        candidates: list[SourceCandidate],
        max_sources: int = 5,
        max_age_days: float = 1.0,
        force_refresh: bool = False,
    ) -> AcquisitionResult:
        bounded = candidates[: max(1, min(max_sources, 20))]
        fresh_candidates = []
        cached = 0
        for candidate in bounded:
            canonical = canonicalize_url(candidate.url)
            if self.registry and not force_refresh and self.registry.is_fresh(canonical, max_age_days):
                cached += 1
            else:
                fresh_candidates.append(candidate)

        fetched = []
        errors = []
        skipped = 0
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._fetch, candidate): candidate
                for candidate in fresh_candidates
            }
            for future in as_completed(futures):
                candidate = futures[future]
                try:
                    candidate, canonical, document, fetched_at = future.result()
                    if not document.text.strip():
                        skipped += 1
                        continue
                    if not self.deduplicator.accept(canonical, document.text):
                        skipped += 1
                        continue
                    fetched.append((candidate, canonical, document, fetched_at))
                except Exception as exc:
                    errors.append({"url": candidate.url, "error": str(exc)})

        sources = []
        for candidate, canonical, document, fetched_at in fetched:
            quality = self.quality.score(canonical, document.text, candidate.score)
            acquired = AcquiredSource(
                canonical,
                document.title,
                document.text,
                candidate.provider,
                quality,
                content_hash(document.text),
                fetched_at,
                0.0,
            )
            self.index_pipeline.index([document])
            if self.storage:
                self.storage.save_acquired_source(acquired)
            sources.append(acquired)

        sources.sort(key=lambda source: source.quality, reverse=True)
        return AcquisitionResult(
            len(bounded),
            len(sources),
            skipped,
            cached,
            len(errors),
            tuple(sources),
            tuple(errors),
        )

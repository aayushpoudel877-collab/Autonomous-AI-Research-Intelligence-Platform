from nexus.research.acquisition import AcquisitionResult


def test_acquisition_result_tracks_cached_sources():
    result = AcquisitionResult(3, 1, 0, 2, 0, (), ())
    assert result.requested == 3
    assert result.acquired == 1
    assert result.cached == 2

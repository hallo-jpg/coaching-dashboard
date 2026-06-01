import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from generate_pacing import parse_gpx, group_segments

FIXTURE = "tests/fixtures/mini.gpx"

def test_parse_gpx_returns_points():
    pts = parse_gpx(FIXTURE)
    assert len(pts) >= 2
    assert "dist" in pts[0]
    assert "ele" in pts[0]

def test_group_segments_returns_segments():
    pts = parse_gpx(FIXTURE)
    segs = group_segments(pts)
    assert len(segs) >= 1
    assert "dist_m" in segs[0]
    assert "gradient_pct" in segs[0]
    assert "elev_start" in segs[0]
    assert "elev_end" in segs[0]

def test_total_distance_plausible():
    pts = parse_gpx(FIXTURE)
    total = pts[-1]["dist"]
    assert 500 < total < 2000  # mini.gpx ist ~1km

def test_gradient_direction():
    pts = parse_gpx(FIXTURE)
    segs = group_segments(pts)
    # mini.gpx steigt → alle Gradienten positiv
    for s in segs:
        assert s["gradient_pct"] > 0

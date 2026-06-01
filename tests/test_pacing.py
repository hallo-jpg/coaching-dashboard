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

from generate_pacing import velocity_from_power, assign_power, compute_w_prime_balance

def test_velocity_increases_with_power():
    v1 = velocity_from_power(200, 5.0, "climb")
    v2 = velocity_from_power(300, 5.0, "climb")
    assert v2 > v1

def test_velocity_decreases_with_gradient():
    v_flat = velocity_from_power(250, 1.0, "climb")
    v_steep = velocity_from_power(250, 8.0, "climb")
    assert v_flat > v_steep

def test_velocity_reasonable_range():
    # 300W auf 5% Anstieg → ca. 12-18 km/h = 3.3-5.0 m/s
    v = velocity_from_power(300, 5.0, "climb")
    assert 3.0 < v < 6.0  # m/s

def test_assign_power_increases_with_gradient():
    p_flat = assign_power(2.0, "climb", 300)
    p_steep = assign_power(7.0, "climb", 300)
    assert p_steep > p_flat

def test_assign_power_tt_higher_than_climb():
    p_climb = assign_power(5.0, "climb", 300)
    p_tt = assign_power(5.0, "tt", 300)
    assert p_tt > p_climb

def test_w_prime_depletes_on_hard_segments():
    segs = [
        {"target_w": 350, "time_s": 300},  # above CP=300 → depletes
        {"target_w": 200, "time_s": 300},  # below CP → recovers
    ]
    result = compute_w_prime_balance(segs, cp_w=300, w_prime_total_j=20000)
    assert result[0]["w_prime_balance_j"] < 20000
    assert result[1]["w_prime_balance_j"] > result[0]["w_prime_balance_j"]

def test_w_prime_never_exceeds_total():
    segs = [{"target_w": 100, "time_s": 600}]  # far below CP → recovery
    result = compute_w_prime_balance(segs, cp_w=300, w_prime_total_j=20000)
    assert result[0]["w_prime_balance_j"] <= 20000

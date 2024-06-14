from src.reach_efficiency_by_zipcode import get_efficiency_stats, get_reach_efficiency

import pandas


def test_get_efficiency_stats():
    raw_df = pandas.DataFrame(
        {
            "ZIP_AUDIENCE_PEOPLE": [100, 200, 300, 400],
            "ZIP_TOTAL_PEOPLE": [1000, 2000, 3000, 4000],
        }
    )
    processed_df = get_efficiency_stats(raw_df)
    assert processed_df["TARGET_DENSITY"].tolist() == [0.1, 0.1, 0.1, 0.1]
    assert processed_df["CUMULATIVE_AUD_REACH"].tolist() == [100, 300, 600, 1000]
    assert processed_df["CUMULATIVE_TOTAL_REACH"].tolist() == [1000, 3000, 6000, 10000]
    assert processed_df["CUMULATIVE_PCT_REACH"].tolist() == [0.1, 0.3, 0.6, 1.0]
    assert processed_df["CUMULATIVE_TARGET_DENSITY"].tolist() == [0.1, 0.1, 0.1, 0.1]


def test_get_reach_efficiency():
    data = pandas.DataFrame(
        {
            "ZIP_AUDIENCE_PEOPLE": [100, 200, 300, 400],
            "ZIP_TOTAL_PEOPLE": [1000, 2000, 3000, 4000],
            "CUMULATIVE_PCT_REACH": [0.1, 0.3, 0.6, 1.0],
            "CUMULATIVE_TARGET_DENSITY": [0.1, 0.1, 0.1, 0.1],
            "CUMULATIVE_AUD_REACH": [100, 300, 600, 1000],
            "CUMULATIVE_TOTAL_REACH": [1000, 3000, 6000, 10000],
        }
    )
    output = get_reach_efficiency(data, 0.5)
    assert output == {
        "zipcode_number": 2,
        "audience_reach": 300,
        "total_reach": 3000,
        "pct_reach": 0.3,
        "target_density": 0.1,
    }

import pandas as pd


# Process data to add reach and efficiency stats
def get_efficiency_stats(raw_df):
    # Target density = in this zipcode, what % of people are targets?
    raw_df["TARGET_DENSITY"] = (
        raw_df["ZIP_AUDIENCE_PEOPLE"] / raw_df["ZIP_TOTAL_PEOPLE"]
    )
    raw_df = raw_df.sort_values(by="TARGET_DENSITY", ascending=False)
    # Cumulative audience reach = if we target up to this zip, how many audience people have we reached?
    raw_df["CUMULATIVE_AUD_REACH"] = raw_df["ZIP_AUDIENCE_PEOPLE"].cumsum()
    # Cumulative total reach = if we target up to this zip, how many total people have we reached (even if they aren't in audience)?
    raw_df["CUMULATIVE_TOTAL_REACH"] = raw_df["ZIP_TOTAL_PEOPLE"].cumsum()
    # Cumulative % reach = if we target up to this zip, what % of the audience have we reached?
    raw_df["CUMULATIVE_PCT_REACH"] = (
        raw_df["CUMULATIVE_AUD_REACH"] / raw_df["ZIP_AUDIENCE_PEOPLE"].sum()
    )
    # Cumulative target density = if we target up to this zip, what % of the people are targets?
    raw_df["CUMULATIVE_TARGET_DENSITY"] = (
        raw_df["CUMULATIVE_AUD_REACH"] / raw_df["CUMULATIVE_TOTAL_REACH"]
    )
    return raw_df


def get_reach_efficiency(data, reach_level):
    targeted = data[data["CUMULATIVE_PCT_REACH"] <= reach_level]
    targeted = targeted.sort_values(by="CUMULATIVE_TARGET_DENSITY", ascending=False)
    output = {
        "zipcode_number": len(targeted),
        "audience_reach": targeted["CUMULATIVE_AUD_REACH"].max(),
        "total_reach": targeted["CUMULATIVE_TOTAL_REACH"].max(),
        "pct_reach": targeted["CUMULATIVE_PCT_REACH"].max(),
        "target_density": targeted.iloc[[-1]]["CUMULATIVE_TARGET_DENSITY"].values[0],
    }
    return output

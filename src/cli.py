import pandas as pd
import sys

from src.reach_efficiency_by_zipcode import get_efficiency_stats, get_reach_efficiency

pd.options.display.float_format = "{:,.2f}".format


def cli(file_name):
    raw_df = pd.read_csv(file_name)

    processed_df = get_efficiency_stats(raw_df)
    output = get_reach_efficiency(processed_df, 0.5)

    print(pd.DataFrame(output, index=[0]).T)


if __name__ == "__main__":
    file_name = sys.argv[1:][0]
    cli(file_name)
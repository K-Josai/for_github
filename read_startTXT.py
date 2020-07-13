import pandas as pd


def main():
    df = pd.read_csv(
        "start.txt", delim_whitespace=True, header=None, skiprows=1)
    print("pandas data frame")
    print(df)

    data_ndarray = df.values
    print("numpy array")
    print(data_ndarray.shape)
    print(data_ndarray)


if __name__ == "__main__":
    main()

import pandas as pd
import math
import numpy as np

INPUT_FILE = 'raw.xlsm'
INPUT_SHEET = 'IntRes1'

OUTPUT_FILE = 'automation.xlsx'
OUTPUT_SHEET = 'IntRes1'


def my_round(x):
    # x = 18.372
    try:
        x_re = x * 10
        # x_return = 18.3
        return math.floor(x_re) / 10.0
    except ValueError:
        return x


def get_columns(data):
    time_col = []
    measurements = []
    shape = data.shape

    # iterate over data set and get new column structure
    for measurement in range(0, shape[0], 2):
        # save number of measurements
        measurements.append(data.iloc[measurement,0])
        measurements.append(None)

        for col in range(2, shape[1]):
            match_val = False
            rounded_val = my_round(data.iloc[measurement, col])
            for ref in time_col:
                if (ref - rounded_val) == 0.0:
                    match_val = True

            # if a new column value has been found, save it
            if not match_val:
                if not math.isnan(rounded_val):
                    time_col.append(rounded_val)

    time_col = sorted(time_col)
    return measurements, time_col


def get_new_col_nr(value, cols):
    # search for best matching column
    matching_col_nr = None
    smallest_diff = 99999

    for i in range(len(cols)):
        diff = abs(value-cols[i])
        if diff < smallest_diff:
            smallest_diff = diff
            matching_col_nr = i
    return matching_col_nr


def create_new_data_frame(columns, index, data):
    # create new matrix
    new_shape = (len(columns), len(index))
    vals = np.zeros(new_shape, dtype=float)

    # iterate over old values and position them in new matrix
    old_shape = data.shape
    for measurement in range(0, old_shape[0], 2):
        for col in range(2, old_shape[1]):
            new_col = get_new_col_nr(data.iloc[measurement, col], columns)
            if new_col is not None:
                vals[new_col, measurement] = data.iloc[measurement, col]
                vals[new_col, measurement+1] = data.iloc[measurement+1, col]
    return vals.transpose()


def main():
    # read in data
    data = pd.read_excel(INPUT_FILE, sheet_name=INPUT_SHEET, header=None)

    # get columns for new data structure
    measure_nr, new_cols = get_columns(data)

    # parse data to new structure
    new_matrix = create_new_data_frame(new_cols, measure_nr, data)

    # convert numpy array to panda dataframe
    new_frame = pd.DataFrame(new_matrix, index=measure_nr, columns=new_cols)

    # save as excel
    new_frame.to_excel(OUTPUT_FILE, sheet_name=OUTPUT_SHEET)


if __name__ == '__main__':
    main()


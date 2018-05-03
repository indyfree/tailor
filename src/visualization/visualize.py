from pathlib import Path
import matplotlib.pyplot as plt
import src.data.load_dataframe as load
import src.features.build_features as build


PROJECT_DIR = str(Path(__file__).resolve().parents[2])
OUTPUTPATH = PROJECT_DIR + '/reports/figures/'


def plot_line_chart(x_axis, y_axis, filename, x_axis_label='', y_axis_label=''):
    fig = plt.figure()
    ax = plt.axes()
    ax.set_ylabel(y_axis_label, fontsize=12)
    ax.set_xlabel(x_axis_label, fontsize=12)
    plt.plot(x_axis, y_axis)
    plt.savefig(OUTPUTPATH + filename)


def main():
    raw_dataframe = load.load_raw_dataframe()
    grouped_dataframe = build.group_dataframe_by_attribute(raw_dataframe, 'time_on_sale')

    plot_line_chart(grouped_dataframe['time_on_sale'],
                    grouped_dataframe['revenue'],
                    'line_chart_revenue.png')


if __name__ == '__main__':
    main()
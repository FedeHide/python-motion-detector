from bokeh.plotting import figure, show, output_file
import pandas


def visualize_motion_intervals(motion_intervals_df) -> None:
    """
    Plot motion intervals.

    Args:
        motion_intervals_df (pandas.DataFrame): DataFrame containing motion intervals.
    """

    motion_intervals_df = pandas.read_csv(motion_intervals_df)
    motion_intervals_df["Start"] = pandas.to_datetime(
        motion_intervals_df["Start"], format="mixed"
    )
    motion_intervals_df["End"] = pandas.to_datetime(
        motion_intervals_df["End"], format="mixed"
    )

    p = figure(
        title="Motion Intervals",
        x_axis_label="Time",
        y_axis_label="Motion",
        x_axis_type="datetime",
        width=800,
        height=400,
    )

    p.quad(
        left=motion_intervals_df["Start"],
        right=motion_intervals_df["End"],
        top=1,
        bottom=0,
        color="green",
    )

    output_file("motion_intervals.html")

    show(p)

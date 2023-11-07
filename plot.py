from picozk import *
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from madlibs import madlibs
from phonebook import phonebook


def generate_data(DEBUG, scale, num_hc, csv):
    data = []
    if csv == "output_madlibs.csv":
        prod_weight, prod_size, reprod_weight, reprod_size = madlibs.run(
            DEBUG=DEBUG, scale=scale, num_blanks=num_hc
        )
    else:
        prod_weight, prod_size, reprod_weight, reprod_size = phonebook.run(
            DEBUG=DEBUG, scale=scale, num_honeys=num_hc
        )
    data.append(
        {
            "prod/reprod": "producer",
            "scale": scale,
            "blank ratio": num_hc / scale,
            "weight": prod_weight,
            "size": prod_size,
        }
    )
    data.append(
        {
            "prod/reprod": "reproducer",
            "scale": scale,
            "blank ratio": num_hc / scale,
            "weight": reprod_weight,
            "size": reprod_size,
        }
    )
    return data


def generate_dataframe(csv):
    data = []
    DEBUG = False
    for scale in range(10, 50, 10):
        for denom in [0.1, 0.5, 1]:
            num_hc = int(scale * denom)
            data.extend(generate_data(DEBUG, scale, num_hc, csv))
    df = pd.DataFrame(data)
    df.to_csv(csv, index=False)


def main(csv, obj):
    # Load the data from the CSV file
    df = pd.read_csv(csv)

    # Filter data for producer and reproducer
    producer_data = df[df["prod/reprod"] == "producer"]
    reproducer_data = df[df["prod/reprod"] == "reproducer"]
    if producer_data.empty:
        print("No producer data available.")
        return
    if reproducer_data.empty:
        print("No reproducer data available.")
        return

    # Define a grid of x and y values
    xi = np.linspace(df["scale"].min(), df["scale"].max(), 100)
    yi = np.linspace(df["blank ratio"].min(), df["blank ratio"].max(), 100)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate z values for the grid using griddata
    prod_zi = griddata(
        (producer_data["scale"], producer_data["blank ratio"]),
        producer_data[obj],
        (xi, yi),
        method="cubic",
    )
    reprod_zi = griddata(
        (reproducer_data["scale"], reproducer_data["blank ratio"]),
        reproducer_data[obj],
        (xi, yi),
        method="cubic",
    )

    # Create the plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Plot the surfaces
    surf1 = ax.plot_surface(xi, yi, prod_zi, alpha=0.6, color="r")
    surf2 = ax.plot_surface(xi, yi, reprod_zi, alpha=0.6, color="b")
    obj = obj[0].upper() + obj[1:]

    # Create proxy artists for the legend
    legend_elements = [
        Line2D([0], [0], color="r", lw=4, label="Producer " + obj),
        Line2D([0], [0], color="b", lw=4, label="Reproducer " + obj),
    ]

    # Add the legend using the proxy artists
    ax.legend(handles=legend_elements, loc="upper right")

    ax.set_xlabel("Scale")
    ax.set_ylabel("Blank Ratio")
    ax.set_zlabel(obj)
    ax.set_title("3D Surface Plot of " + obj)

    plt.show()


if __name__ == "__main__":
    p = (
        pow(2, 256)
        - pow(2, 32)
        - pow(2, 9)
        - pow(2, 8)
        - pow(2, 7)
        - pow(2, 6)
        - pow(2, 4)
        - 1
    )

    with PicoZKCompiler("irs/picozk_test", field=[p], options=["ram"]):
        csv = "output_phonebook.csv"

        generate_dataframe(csv)

        obj = "size"
        main(csv, obj)

        obj = "weight"
        main(csv, obj)

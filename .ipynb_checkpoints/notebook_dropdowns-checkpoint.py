"""
Notebook dropbown functions.

This notebook contains variables and functions that allow users to select areas using a combination of dropdowns and interactive maps.
It was developed as part of the Living Wales project.

Authors: Abigail Sanders, Dan Clewley.

"""

import glob
import os
import pandas as pd
import geopandas as gpd
import ipywidgets as widgets
import ipyleaflet
from IPython.display import display
import matplotlib.pyplot as plt
from ipywidgets import Layout

WELSH_AREAS_FOLDER = "/home/jovyan/shared_space/welsh_areas"
USER_UPLOADS_FOLDER = "/home/jovyan/shared_space/uploads"

vector_types_list = glob.glob(f"{WELSH_AREAS_FOLDER}/*")
vector_types_dict = {}

# Add in user uploads directory
vector_types_dict["1. User uploads"] = USER_UPLOADS_FOLDER

vector_types_dict = vector_types_dict | {
    os.path.basename(vector_type).replace("_", " "): vector_type
    for vector_type in vector_types_list
    if os.path.isdir(vector_type)
}


global gpd_df
global col_name_var
global AREA_SELECTION
global selected_polygon
global RESULTS


RESULTS = {}
RESULTS["global_selected_polygon"] = None
RESULTS["global_selected_polygon_type"] = None  # options are All: if all is selected and Selected: if a single one is selected


AREA_SELECTION = None
selected_polygon = None


def set_global_result(key, value):
    """ This sets value to globally defined RESULTS dictionary """
    RESULTS[key] = value
    
    
def get_global_result(key):
    """ This reads value from globally defined RESULTS dictionary """
    # return RESULTS.get(key, "Nothing selected")
    return RESULTS.get(key, None)


    
def polygon_selected():
    """ This function fetches and returns value of selected polygon if it exists """
    selected_global_polygon =  get_global_result("global_selected_polygon")
    selected_global_polygon_type =  get_global_result("global_selected_polygon_type")
    
    
    if selected_global_polygon_type and selected_global_polygon_type == "All":
         # return whole thing if all is selected
        return gpd_df
        
    elif selected_global_polygon and selected_global_polygon_type == "Selected":
        try:
            identifer_key = list(selected_global_polygon.keys())[0]
            if identifer_key:
                gpd_df_sub = gpd_df[gpd_df[identifer_key] == selected_global_polygon[identifer_key]]
                # find and return selected polygon 
                return gpd_df_sub
        except Exception as e:
            # return all of it  or return None (if something goes wrong)?
            return selected_global_polygon
    
    # returns None if cant find setr selected polygon values
    return None



def convert_timestamps_to_strings(df):
    """
    Converts all Timestamp columns in the DataFrame to strings.
    """
    for col in df.columns:
        # Comment out print to debug
        # print(f"{col} {df[col].dtype}")
        if (
            isinstance(df[col].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype)
            or df[col].dtype == "datetime64[ns]"
            or df[col].dtype == "datetime64[ms]"
        ):
            df[col] = df[col].astype(str)
    return df


def area_selection():
    # Path to Welsh Dataset repository
    shapefiles_dict = {}

    def update_shapefiles(*args):
        # List all shapefiles in the selected directory
        shapefiles_list = glob.glob(
            os.path.join(vector_types_dict[get_type.value], "*.shp")
        )
        shapefiles_dict.clear()
        shapefiles_dict.update(
            {
                os.path.basename(shapefile)
                .replace(".shp", "")
                .replace("_", " ")
                .lower(): shapefile
                for shapefile in shapefiles_list
            }
        )

        # Update shapefile dropdown options
        get_shapefile.options = list(shapefiles_dict.keys())
        get_shapefile.value = (
            list(shapefiles_dict.keys())[0] if shapefiles_dict else None
        )
        update_polygons()

    # Function to update the polygon options
    def update_polygons(*args):
        selected_shapefile_path = shapefiles_dict.get(get_shapefile.value, None)

        if selected_shapefile_path:
            global gpd_df, col_name_var  # Define as global variables
            gpd_df = gpd.read_file(selected_shapefile_path)

            # Try to find a suitable column name for site names
            col_name_var = None
            if "name" in gpd_df.columns:
                col_name_var = "name"
            else:
                for col in gpd_df.columns:
                    if "name" in col.lower():
                        col_name_var = col
                        break

            if col_name_var is not None:
                site_names = gpd_df[col_name_var].drop_duplicates().tolist()
                get_polygon.options = site_names
                get_polygon.value = None
            else:
                get_polygon.options = []
                get_polygon.value = None
        else:
            get_polygon.options = []
            get_polygon.value = None

    style = {'description_width': 'initial'}
    
    # Dropdown for selecting vector type
    get_type = widgets.Dropdown(
        options=list(vector_types_dict.keys()),
        value=list(vector_types_dict.keys())[0],
        default="User uploads",
        description="Select Type",
        disabled=False,
        layout=Layout(width='40%'),
        style=style
    )

    # Dropdown for selecting shapefile
    get_shapefile = widgets.Dropdown(
        options=[],
        description="Choose Vector",
        disabled=False,
        layout=Layout(width='40%'),
        style=style
    )

    # Dropdown for selecting polygon
    global get_polygon
    get_polygon = widgets.Dropdown(
        options=[],
        description="Select a polygon",
        disabled=False,
        default="",
        layout=Layout(width='40%'),
        style=style
    )

    # Observe changes and update accordingly
    get_type.observe(update_shapefiles, "value")
    get_shapefile.observe(update_polygons, "value")

    # Function to reset the dropdowns and clear outputs
    def reset_dropdowns(*args):
        get_type.value = list(vector_types_dict.keys())[0]
        update_shapefiles()
        clear_output(wait=True)
        display(get_type)
        display(get_shapefile)
        display(get_polygon)
        display(reset_button)

    # Button for resetting the dropdowns
    reset_button = widgets.Button(description="Reset")
    reset_button.on_click(reset_dropdowns)

    # Initial update of shapefiles and polygons
    update_shapefiles()

    # Display the dropdowns and reset button
    display(get_type)
    display(get_shapefile)
    display(get_polygon)
    display(reset_button)
    # return get_type, get_shapefile, get_polygon, reset_button
    
    return get_polygon


def static_polygon_plot(get_polygon):
    """
    Produces a static plot of a given polygon
    """
    if get_polygon.value is not None:
        gpd_df_sub = gpd_df[gpd_df[col_name_var] == get_polygon.value]
        polygon_name = get_polygon.value
    else:
        gpd_df_sub = gpd_df
        polygon_name = "All"

    # Ensure the GeoDataFrame is in a projected CRS for accurate area calculation
    gpd_df_sub = gpd_df_sub.to_crs(epsg=3857)

    # Calculate the area in square meters
    gpd_df_sub["area"] = gpd_df_sub.geometry.area

    # Sum the areas to get the total area in hectares (1 hectare = 10,000 square meters)
    total_area = gpd_df_sub["area"].sum() / 10000

    # Set the GeoDataFrame back to geographic CRS for plotting
    gpd_df_sub = gpd_df_sub.to_crs(epsg=4326)

    # Set the figure size for standardization
    fig, ax = plt.subplots(figsize=(10, 10))

    # Visualize the polygon with standardized size
    gpd_df_sub.plot(ax=ax, color="blue", edgecolor="black")
    ax.set_title(f"Site Visualization ({polygon_name})")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Add north arrow
    x, y = -0.2, 1  # Adjust these values based on your plot
    arrow_length = 0.1
    ax.annotate(
        "N",
        xy=(x, y),
        xytext=(x, y - arrow_length),
        arrowprops=dict(facecolor="black", width=5, headwidth=15),
        ha="center",
        va="center",
        fontsize=20,
        xycoords="axes fraction",
    )

    plt.show()

    # Display total area
    print(f"Total area: {total_area:.2f} ha")

    return gpd_df_sub





def interactive_polygon_plot(gpd_df_sub):
    """
    Produces an interactive plot of a given polygon
    """
    global AREA_SELECTION
    global selected_polygon

    # Style function for polygons
    def style_function(feature):
        if selected_polygon and all(
            feature["properties"][k] == selected_polygon[k] for k in selected_polygon
        ):
            return {
                "color": "black",
                "fillColor": "yellow",  # Color for the selected polygon
                "opacity": 0.05,
                "weight": 1.9,
                "dashArray": "2",
                "fillOpacity": 0.6,
            }
        else:
            return {
                "color": "black",
                "fillColor": "#3366cc",  # Default color
                "opacity": 0.05,
                "weight": 1.9,
                "dashArray": "2",
                "fillOpacity": 0.6,
            }

    # Function to update the style of the selected polygon
    def update_polygon_style(feature):
        geo_data.style_callback = style_function
        #geo_data.clear_layers()
        #geo_data.update()

    # Function to handle click events and store the selected polygon
    def handle_click(event, feature, **kwargs):
        html.value = f"<b style='color:black'> Identifying selected area please wait .... </b> <br>"
        selected_polygon = feature["properties"]
        # Update the style of the selected polygon
        update_polygon_style(feature)
        html.value = f"<b style='color:orange'>Selected Polygon: </b> <br> {selected_polygon}"
        set_global_result("global_selected_polygon", selected_polygon)
        set_global_result("global_selected_polygon_type", "Selected")


    # Function to confirm and rename the output to AREA_selection
    def confirm_selection(button):
        AREA_SELECTION = AREA_SELECTION
        print("The selected area has been confirmed as 'AREA_SELECTION'")
        
    
    # Function to select all polyons 
    def confirm_select_all(button):
        html.value = "<b style='color:orange'>  All polygons currently selected <b>"
        set_global_result("global_selected_polygon", gpd_df_sub)
        set_global_result("global_selected_polygon_type", "All")
        print("All polygon selected")

    # Calculate the bounding box
    bounds = gpd_df_sub.total_bounds  # returns (minx, miny, maxx, maxy)
    sw = [bounds[1], bounds[0]]  # southwest corner (miny, maxx)
    ne = [bounds[3], bounds[2]]  # northeast corner (maxy, minx)

    # Calculate the center of the bounding box
    center = [(sw[0] + ne[0]) / 2, (sw[1] + ne[1]) / 2]

    # Convert any Timestamps to strings
    AREA_SELECTION = convert_timestamps_to_strings(gpd_df_sub)

    # Initialize selected_polygon variable
    selected_polygon = None

    # Create a button for confirming the selection
    confirm_button = widgets.Button(description="CONFIRM")
    confirm_button.on_click(confirm_selection)
    
    
    #use all polygon button
    select_all_poly_button = widgets.Button(description="USE ALL POLYGONS")
    select_all_poly_button.on_click(confirm_select_all)

    # Display the instructions, button, and map
    # instructions = widgets.HTML("<b>If you are happy with the entire areas shown please click 'Confirm'.<br>If you want to select a specific polygon please click on the map.</b>")
    # display(widgets.VBox([instructions, confirm_button]))
    # HTML widget to display selected shapefile information
    html = widgets.HTML()
    html.value = "<b style='color:orange'> All polygons currently selected <b>"

    # Create GeoData layer
    geo_data = ipyleaflet.GeoData(
        geo_dataframe=AREA_SELECTION,
        style={
            "color": "black",
            "fillColor": "#3366cc",
            "opacity": 0.05,
            "weight": 1.9,
            "dashArray": "2",
            "fillOpacity": 0.6,
        },
        hover_style={"fillColor": "red", "fillOpacity": 0.2},
        name="Boundary",
    )

    geo_data.on_click(handle_click)

    # Create a map centered on the GeoDataFrame
    m = ipyleaflet.Map(
        center=center,
        zoom=50,
        basemap=ipyleaflet.basemaps.Esri.WorldImagery,
        layout=widgets.Layout(height="600px"),
    )

    # Add GeoData layer to the map
    m.add_layer(geo_data)

    # Fit map to bounds
    m.fit_bounds([sw, ne])

    # Add controls to the map
    m.add_control(ipyleaflet.LayersControl(position="topright"))
    m.add_control(ipyleaflet.FullScreenControl())

    # Display the map
    # display(m)
    display(
        widgets.VBox(
            [
                widgets.HTML(
                    "<b>If you are happy with the entire areas shown please click <span style='color:orange'>'USE ALL POLYGONS' </span>.<br>If you want to select a specific polygon please click on the map, to select area and <span style='color:orange'> wait for <span style='color:#5a5c5a'> 'Selected Polygon' </span> confirmation below.<span>  </b>"
                ),
                html,
                # confirm_button,
                select_all_poly_button,
                m,
            ]
        )
    )





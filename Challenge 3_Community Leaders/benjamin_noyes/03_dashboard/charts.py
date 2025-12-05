from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests
import json


from data import tab1_data, tab2_data, tab3_data, tab4_data, intersections
from color import segment_colors_dct

############################################## tab 1 ##############################################

vc_country = pd.Series(tab1_data)

geojson_url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
geojson = requests.get(geojson_url).json()

tab1_geo_fig = px.choropleth_mapbox(
  vc_country,
  geojson = geojson,
  featureidkey="properties.ISO_A2",
  locations=vc_country.index,
  color=vc_country.values,
  color_continuous_scale="Mint",
  mapbox_style="carto-positron",
  zoom=4,
  center={"lat":0, "lon": 35},
  opacity=0.5,
  range_color=[0, vc_country.values.max()]
).update_traces(
  hovertemplate=(
    "<b>%{location}</b><br>" +
    "Number of users: %{z:,}<br>" +
    "<extra></extra>"    
  )
).update_layout({
  "title": {"text": "Number of users in geographic region", "x": 0.5},
  "coloraxis": {
    "colorbar": {
      "title": "n users"
    }
  }
})

############################################## tab 2 ##############################################
def tab2_hist_fig(country_codes, segmentation_name):

  df = tab2_data[segmentation_name]
  df_country =  df[df["question_user_country_code"].isin(country_codes)]
  df_summed = df_country.groupby(segmentation_name, as_index=False)["n"].sum()

  fig = px.bar(
    df_summed,
    x=segmentation_name, 
    y="n",
    color=segmentation_name,
    color_discrete_map=segment_colors_dct
  )

  return fig.update_traces(
    marker_line_width=0
  ).update_layout({
    "title": {"text": f"{", ".join(country_codes)}, {segmentation_name}", "x": 0.5},
    "xaxis": {"title": "segments"},
  })

def tab2_pie_fig(country_codes, segmentation_name):

  df = tab2_data[segmentation_name]
  df_country =  df[df["question_user_country_code"].isin(country_codes)]
  df_summed = df_country.groupby(segmentation_name, as_index=False)["n"].sum()

  fig = px.pie(
    df_summed, 
    names=segmentation_name, 
    values="n",
    color=segmentation_name,
    color_discrete_map=segment_colors_dct
  )
  fig.update_traces(
    hovertemplate="segment %{label}"
  )

  return fig.update_layout({
    "title": {"text": f"{", ".join(country_codes)}, {segmentation_name}", "x": 0.5},
    "showlegend": False,
  })

############################################## tab 5 (2.5, between 2 and 3) ##############################################

def tab5_funnel_fig(country_codes, segment_values_dct):
    
    labels = []
    values = []
    
    current_combo = {
      "Count": ["1", "2", "3", "4", "5"],
      "Speed": ["1", "2", "3", "4", "5"],
      "Reach": ["1", "2", "3", "4", "5"],
      "Tenure": ["1", "2", "3", "4", "5"]
    }
    
    key = json.dumps(current_combo, sort_keys=True)
    labels.append("all users in region(s)")
    values.append(sum(intersections["counts"][key]["by_country"][c] for c in country_codes))
  
    for segment_name, segment_value in segment_values_dct.items():
      if segment_value and segment_value != "None":
        current_combo[segment_name] = [segment_value]
        key = json.dumps(current_combo, sort_keys=True)
        
        labels.append(f"{segment_name}: {segment_value}")
        values.append(sum(intersections["counts"][key]["by_country"][c] for c in country_codes))
    
    fig = go.Figure(
      go.Funnel(
        y=labels,
        x=values,
        textposition="outside",
        textinfo="value+percent initial",
        marker={"color": ["#9F90E8", "#9F90E8", "#9F90E8", "#9F90E8", "#9F90E8"]}
      )
    )
    
    fig.update_layout({
      "title": {"text": "Custom segment, funnel", "x": 0.5},
      "showlegend": False
      }
    )
    
    return fig


############################################## tab 3 ##############################################

def tab3_bar_bigfig(
    country_codes, 
    segmentation_name, 
    individual_segment_lst,
    broad_category_lst,
    switch_cs1,
    cs1_key_json,
    switch_cs2,
    cs2_key_json
  ):

  df_b = tab3_data["broad"][segmentation_name]
  df_n = tab3_data["niche"][segmentation_name]

  df_cs1_b = intersections["broad"][cs1_key_json]
  df_cs1_n = intersections["niche"][cs1_key_json]

  df_cs2_b = intersections["broad"][cs2_key_json]
  df_cs2_n = intersections["niche"][cs2_key_json]


  bigfig = make_subplots(
    2, len(country_codes),
    subplot_titles=[
      f"{country} {topic}" for topic in ["broad topics", "niche topics"] 
      for country in country_codes
    ],
    vertical_spacing=0.3
  )

  for idx, country in enumerate(country_codes):
    df_norm_broad = df_b[df_b["question_user_country_code"]==country]

    niche_mk = (df_n["question_user_country_code"]==country)
    if broad_category_lst:
      niche_mk &= (df_n["broad_type"].isin(broad_category_lst))
    df_norm_niche = df_n[niche_mk]

    segment_order_lst = ["1", "2", "3", "4", "5"]
    segment_final_lst = [j for j in segment_order_lst if j in individual_segment_lst]

    for segment in segment_final_lst:
      df_trace_broad = df_norm_broad[df_norm_broad[segmentation_name]==segment]
      df_trace_niche = df_norm_niche[df_norm_niche[segmentation_name]==segment]
      bigfig.add_trace(
        go.Bar(
          x=df_trace_broad["category"],
          y=df_trace_broad["pct"],
          customdata=df_trace_broad["count"],
          hovertemplate=(
            "<b>%{x}</b><br>" +
            "Percentage: %{y:.1%}<br>" +
            "Sample size: %{customdata:,}<br>" +
            "<extra></extra>"
          ),
          error_y={
            "type": "data",
            "array": df_trace_broad["se"],
            "width": 0,
            "thickness": 2,
            "visible": True
          },
          showlegend=(idx==0),
          marker={
            "color": df_trace_broad["segment_color"],
          },
          name=segment
        ),
        row=1, col=idx+1
      ).add_trace(
        go.Bar(
          x=df_trace_niche["category"],
          y=df_trace_niche["pct"],
          customdata=df_trace_niche["count"],
          hovertemplate=(
            "<b>%{x}</b><br>" +
            "Percentage: %{y:.1%}<br>" +
            "Sample size: %{customdata:,}<br>" +
            "<extra></extra>"
          ),
          error_y={
            "type": "data",
            "array": df_trace_niche["se"],
            "width": 0,
            "thickness": 2,
            "visible": True
          },
          showlegend=False,
          marker={
            "color": df_trace_niche["segment_color"],
          },
          name=segment
        ),
        row=2, col=idx+1
      )

    custom_segments_df_lst = []
    if switch_cs1:
      custom_segments_df_lst.append((df_cs1_b, df_cs1_n, "#9F90E8", "Custom 1"))
    if switch_cs2:
      custom_segments_df_lst.append((df_cs2_b, df_cs2_n, "black", "Custom 2"))

    for idx_color, (df_cs_b, df_cs_n, color, name) in enumerate(custom_segments_df_lst):

      df_cs_b_country = df_cs_b[df_cs_b["question_user_country_code"]==country]
      df_cs_n_country = df_cs_n[df_cs_n["question_user_country_code"]==country]

      niche_mk = pd.Series(True, index=df_cs_n_country.index)
      if broad_category_lst:
        niche_mk &= (df_cs_n_country["broad_type"].isin(broad_category_lst))
      df_cs_n_country = df_cs_n_country[niche_mk]

      bigfig.add_trace(
        go.Bar(
          x=df_cs_b_country["category"],
          y=df_cs_b_country["pct"],
          error_y={
            "type": "data",
            "array": df_cs_b_country["se"],
            "thickness": 2,
            "width": 0,
            "visible": True,
          },
          customdata=df_cs_b_country["count"],
          hovertemplate=(
            "<b>%{x}</b><br>" +
            "Percentage: %{y:.1%}<br>" +
            "Sample size: %{customdata:,}<br>" +
            "<extra></extra>"
          ),
          showlegend=(idx==0),
          marker={
            "color": color
          },
          name=name
        ),
        row=1, col=idx+1
      ).add_trace(
        go.Bar(
          x=df_cs_n_country["category"],
          y=df_cs_n_country["pct"],
          error_y={
            "type": "data",
            "array": df_cs_n_country["se"],
            "thickness": 2,
            "width": 0,
            "visible": True,
          },
          customdata=df_cs_n_country["count"],
          hovertemplate=(
            "<b>%{x}</b><br>" +
            "Percentage: %{y:.1%}<br>" +
            "Sample size: %{customdata:,}<br>" +
            "<extra></extra>"
          ),
          showlegend=False,
          marker={
            "color": color
          },
        ),
        row=2, col=idx+1
      )

  return bigfig

############################################## tab 4 ##############################################
def set_consistent_yaxes(fig, all_y_values, niche=False):

  if not niche:
    padding=0.05
  else:
    padding=0.01

  y_min = min(all_y_values)
  y_max = max(all_y_values)

  new_y_min = y_min - padding
  new_y_max = y_max + padding

  new_y_min = max(0, new_y_min)

  return fig.update_yaxes({"range": [new_y_min, new_y_max]})

def tab4_broad_bigfig(
    country_codes, 
    segmentation_name,
    individual_segment_lst,
    broad_category_lst,
    time_slice,
    switch_cs1,
    cs1_key_json,
    switch_cs2,
    cs2_key_json
  ):


  df = tab4_data["broad"][segmentation_name][time_slice]
  df_cs1 = intersections["time_broad"][cs1_key_json][time_slice]
  df_cs2 = intersections["time_broad"][cs2_key_json][time_slice]

  bigfig = make_subplots(
    len(broad_category_lst), len(country_codes),
    subplot_titles=[
      f"{cat}: {country}"
      for cat in broad_category_lst
      for country in country_codes
    ],
    vertical_spacing=0.1,
    row_heights=[300] * len(broad_category_lst)
  )

  all_y_lst = []

  for idx_col, country in enumerate(country_codes):
    df_country = df[df["question_user_country_code"]==country]
    for idx_row, cat in enumerate(broad_category_lst):
      df_cat = df_country[df_country["category"]==cat]

      segment_order_lst = ["1", "2", "3", "4", "5"]
      segment_final_lst = [j for j in segment_order_lst if j in individual_segment_lst]

      for segment in segment_final_lst:

        df_segment = df_cat[df_cat[segmentation_name]==segment]
        all_y_lst.extend(df_segment["pct"].tolist())

        bigfig.add_trace(
          go.Scatter(
            x=df_segment[time_slice],
            y=df_segment["pct"],
            customdata=df_segment["count"],
            hovertemplate=(
              "<b>%{x}</b><br>" +
              "Percentage: %{y:.1%}<br>" +
              "Sample size: %{customdata:,}<br>" +
              "<extra></extra>"
            ),
            error_y={
              "type": "data",
              "array": df_segment["se"],
              "thickness": 2,
              "width": 0
            },
            mode="lines+markers",
            marker={"color": df_segment["segment_color"].values},
            line={"color": df_segment["segment_color"].iloc[0]},
            showlegend=(idx_row==0 and idx_col==0),
            name=segment
          ),
          row=idx_row+1, col=idx_col+1
        )

      custom_segments_df_lst = []
      if switch_cs1:
        custom_segments_df_lst.append((df_cs1, "#9F90E8", "Custom 1"))
      if switch_cs2:
        custom_segments_df_lst.append((df_cs2, "black", "Custom 2"))

      for idx_color, (df_cs_b, color, name) in enumerate(custom_segments_df_lst):
        df_cs_country = df_cs_b[df_cs_b["question_user_country_code"]==country]
        df_cs_cat = df_cs_country[df_cs_country["category"]==cat]
        all_y_lst.extend(df_cs_cat["pct"].tolist())

        bigfig.add_trace(
          go.Scatter(
            x=df_cs_cat[time_slice],
            y=df_cs_cat["pct"],
            customdata=df_segment["count"],
            hovertemplate=(
              "<b>%{x}</b><br>" +
              "Percentage: %{y:.1%}<br>" +
              "Sample size: %{customdata:,}<br>" +
              "<extra></extra>"
            ),
            error_y={
              "type": "data",
              "array": df_cs_cat["se"],
              "thickness": 2,
              "width": 0
            },            
            mode="lines+markers",
            marker={"color": color},
            showlegend=(idx_row==0 and idx_col==0),
            name=name 
          ),
          row=idx_row+1, col=idx_col+1
        )

  return bigfig.update_layout({
    "height": 300 * len(broad_category_lst)
  })
    
def tab4_niche_bigfig(
    country_codes, 
    segmentation_name, 
    individual_segment_lst, 
    broad_category_lst, 
    niche_category_lst, 
    time_slice,
    switch_cs1,
    cs1_key_json,
    switch_cs2,
    cs2_key_json
  ):

  df = tab4_data["niche"][segmentation_name][time_slice]

  if not niche_category_lst:
    niche_category_lst=["maize"]

  niche_mk = pd.Series(True, index=df.index)
  if niche_category_lst:
    niche_mk &= (df["niche"].isin(niche_category_lst))
  df_sub_niche = df[niche_mk]

  df_cs1 = intersections["time_niche"][cs1_key_json][time_slice]
  df_cs2 = intersections["time_niche"][cs2_key_json][time_slice]

  bigfig = make_subplots(
    len(niche_category_lst), len(country_codes),
    subplot_titles=[
      f"{cat}: {country}"
      for cat in niche_category_lst
      for country in country_codes
    ],
    vertical_spacing=0.1,
    row_heights=[300] * len(niche_category_lst)
  )

  all_y_lst = []

  for idx_col, country in enumerate(country_codes):
    df_country = df_sub_niche[df_sub_niche["question_user_country_code"]==country]
    for idx_row, cat in enumerate(niche_category_lst):
      df_cat = df_country[df_country["niche"]==cat]

      segment_order_lst = ["1", "2", "3", "4", "5"]
      segment_final_lst = [j for j in segment_order_lst if j in individual_segment_lst]
      for segment in segment_final_lst:
        df_segment = df_cat[df_cat[segmentation_name]==segment]

        all_y_lst.extend(df_segment["pct"].tolist())

        bigfig.add_trace(
          go.Scatter(
            x=df_segment[time_slice],
            y=df_segment["pct"],
            customdata=df_segment["count"],
            hovertemplate=(
              "<b>%{x}</b><br>" +
              "Percentage: %{y:.1%}<br>" +
              "Sample size: %{customdata:,}<br>" +
              "<extra></extra>"
            ),
            error_y={
              "type": "data",
              "array": df_segment["se"],
              "thickness": 2,
              "width": 0
            },
            mode="lines+markers",            
            marker={"color": df_segment["segment_color"].values},
            line={"color": df_segment["segment_color"].iloc[0]},
            showlegend=(idx_row==0 and idx_col==0),
            name=segment
          ),
          row=idx_row+1, col=idx_col+1
        )

      custom_segments_df_lst = []
      if switch_cs1:
        custom_segments_df_lst.append((df_cs1, "#9F90E8", "Custom 1"))
      if switch_cs2:
        custom_segments_df_lst.append((df_cs2, "black", "Custom 2"))

      for idx_color, (df_cs_n, color, name) in enumerate(custom_segments_df_lst):
        df_cs_country = df_cs_n[df_cs_n["question_user_country_code"]==country]
        df_cs_cat = df_cs_country[df_cs_country["niche"]==cat]
        all_y_lst.extend(df_cs_cat["pct"].tolist())

        bigfig.add_trace(
          go.Scatter(
            x=df_cs_cat[time_slice],
            y=df_cs_cat["pct"],
            customdata=df_cs_cat["count"],
            hovertemplate=(
              "<b>%{x}</b><br>" +
              "Percentage: %{y:.1%}<br>" +
              "Sample size: %{customdata:,}<br>" +
              "<extra></extra>"
            ),
            error_y={
              "type": "data",
              "array": df_cs_cat["se"],
              "thickness": 2,
              "width": 0
            },
            mode="lines+markers",
            marker={"color": color},
            showlegend=(idx_row==0 and idx_col==0),
            name=name
          ),
          row=idx_row+1, col=idx_col+1
        )

  return bigfig.update_layout({
    "height": 300 * len(niche_category_lst)
  })

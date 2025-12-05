from dash import Input, Output, State, exceptions
import dash_mantine_components as dmc
import plotly.graph_objects as go
import numpy as np
import json

from charts import tab2_hist_fig, tab2_pie_fig, tab3_bar_bigfig, tab4_broad_bigfig, tab4_niche_bigfig, tab5_funnel_fig
from data import tab2_data, tab3_data, intersections
from color import basic_layout, segment_colors_dct

def none_to_list(lst):
    return ["1", "2", "3", "4", "5"] if lst=="None" else [lst]

def none_to_string(input):
    return "None"


def callbacks_master(app):
############################################## tab 2 ##############################################

    @app.callback(
        Output("comp5_hist_fig_tab2_OUT", "figure"),
        Output("comp6_pie_fig_tab2_OUT", "figure"),
        Output("comp3_s1_text_tab2_OUT", "children"),
        Output("comp3_s2_text_tab2_OUT", "children"),
        Output("comp3_s3_text_tab2_OUT", "children"),
        Output("comp3_s4_text_tab2_OUT", "children"),
        Output("comp3_s5_text_tab2_OUT", "children"),
        Input("comp4_dropdown_country_tab2_IN", "value"),
        Input("comp4_dropdown_segmentation_tab2_IN", "value")
    )
    def callback_tab2_out(country, segmentation):

        if not country:
            country = tab2_data["Count"]["question_user_country_code"].unique()            

        df_segmentation = tab2_data[segmentation]
        df_country = df_segmentation[df_segmentation["question_user_country_code"].isin(country)]
        df_country_summed = df_country.groupby(segmentation, as_index=False)["n"].sum()

        df_segment_lst = [
            str(df_country_summed[df_country_summed[segmentation]==segment]["n"].values[0]) 
            for segment in df_segmentation[segmentation].unique()
        ]

        return (
            basic_layout(
                tab2_hist_fig(
                    country, 
                    segmentation
                )
            ), basic_layout(
                tab2_pie_fig(
                    country, 
                    segmentation
                )
            ),
            *df_segment_lst
        )

############################################## tab 5 (2.5, between 2 and 3) ##############################################

    @app.callback(
        Output("comp20_funnel_fig_tab5_OUT", "figure"),
        Output("comp19_cs_text_tab5_OUT", "children"),
        Input("comp19_dropdown_country_cs_tab5_IN", "value"),
        Input("comp19_dropdown_ua_cs_tab5_IN", "value"),
        Input("comp19_dropdown_spr_cs_tab5_IN", "value"),
        Input("comp19_dropdown_cs_cs_tab5_IN", "value"),
        Input("comp19_dropdown_ten_cs_tab5_IN", "value")
        )
    def callback_tab5_out(country, ua_cs, spr_cs, cs_cs, ten_cs):
        if not country:
            country = tab2_data["Count"]["question_user_country_code"].unique()
        if not ua_cs:
            ua_cs = none_to_string(ua_cs)
        if not spr_cs:
            spr_cs = none_to_string(spr_cs)
        if not cs_cs:
            cs_cs = none_to_string(cs_cs)
        if not ten_cs:
            ten_cs = none_to_string(ten_cs)

        cs_combo_dct = {
            "Reach": none_to_list(cs_cs),
            "Speed": none_to_list(spr_cs),
            "Tenure": none_to_list(ten_cs),
            "Count": none_to_list(ua_cs)
        }

        cs_key_json = json.dumps(cs_combo_dct, sort_keys=True)
        intersections_sub_dct = intersections["counts"][cs_key_json]
        cs_count = sum(intersections_sub_dct["by_country"][c] for c in country)

        segment_values_dct = {
            "Count": ua_cs,
            "Speed": spr_cs,
            "Reach": cs_cs,
            "Tenure": ten_cs
        }

        return (
            basic_layout(
                tab5_funnel_fig(
                    country,
                    segment_values_dct
                )
            ),
            cs_count
        )


############################################## tab 3 ##############################################

    @app.callback(
        Output("comp8_bigfig_tab3_OUT", "figure"),
        Output("comp7_basicsegments_pills_tab3", "children"),
        Output("comp12_cs1_text_tab3_OUT", "children"),
        Output("comp17_cs2_text_tab3_OUT", "children"),
        Input("comp7_dropdown_country_tab3_IN", "value"),
        Input("comp7_dropdown_segmentation_tab3_IN", "value"),
        Input("comp7_dropdown_individual_segment_tab3_IN", "value"),
        Input("comp7_dropdown_b_topic_tab3_IN", "value"),
        Input("comp12_dropdown_switch_cs1_tab3_IN", "checked"),
        Input("comp12_dropdown_ua_cs1_tab3_IN", "value"),
        Input("comp12_dropdown_spr_cs1_tab3_IN", "value"),
        Input("comp12_dropdown_cs_cs1_tab3_IN", "value"),
        Input("comp12_dropdown_ten_cs1_tab3_IN", "value"),
        Input("comp17_dropdown_switch_cs2_tab3_IN", "checked"),
        Input("comp17_dropdown_ua_cs2_tab3_IN", "value"),
        Input("comp17_dropdown_spr_cs2_tab3_IN", "value"),
        Input("comp17_dropdown_cs_cs2_tab3_IN", "value"),
        Input("comp17_dropdown_ten_cs2_tab3_IN", "value")
    )
    def callback_tab3_out(
        country, 
        segmentation, 
        individual_segment_lst, 
        broad_topic_lst,
        switch_cs1,
        ua_cs1,
        spr_cs1,
        cs_cs1,
        ten_cs1,
        switch_cs2,
        ua_cs2,
        spr_cs2,
        cs_cs2,
        ten_cs2

    ):

        if not individual_segment_lst:
            individual_segment_lst = ["1", "2", "3", "4", "5"]
        if not country:
            country = tab2_data["Count"]["question_user_country_code"].unique()
        if not ua_cs1:
            ua_cs1 = none_to_string(ua_cs1)
        if not spr_cs1:
            spr_cs1 = none_to_string(spr_cs1)
        if not cs_cs1:
            cs_cs1 = none_to_string(cs_cs1)
        if not ten_cs1:
            ten_cs1 = none_to_string(ten_cs1)
        if not ua_cs2:
            ua_cs2 = none_to_string(ua_cs2)
        if not spr_cs2:
            spr_cs2 = none_to_string(spr_cs2)
        if not cs_cs2:
            cs_cs2 = none_to_string(cs_cs2)
        if not ten_cs2:
            ten_cs2 = none_to_string(ten_cs2)

        df_segmentation = tab2_data[segmentation]
        df_country = df_segmentation[df_segmentation["question_user_country_code"].isin(country)]

        df_segment_count_dct_lst = {
            segment: df_country[df_country[segmentation]==segment]["n"].sum()
            for segment in individual_segment_lst
        }

        pills_lst = []
        for segment, count in df_segment_count_dct_lst.items():
            pills_lst.append(
                dmc.Badge(
                    f"{count}",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color=segment_colors_dct[segment],
                    style={"color": "white"}
                )
            )

        cs1_combo_dct = {
            "Reach": none_to_list(cs_cs1),
            "Speed": none_to_list(spr_cs1),
            "Tenure": none_to_list(ten_cs1),
            "Count": none_to_list(ua_cs1)
        }

        cs1_key_json = json.dumps(cs1_combo_dct, sort_keys=True)
        cs1_count = intersections["counts"][cs1_key_json]["total"]

        cs2_combo_dct = {
            "Reach": none_to_list(cs_cs2),
            "Speed": none_to_list(spr_cs2),
            "Tenure": none_to_list(ten_cs2),
            "Count": none_to_list(ua_cs2)
        }

        cs2_key_json = json.dumps(cs2_combo_dct, sort_keys=True)
        cs2_count = intersections["counts"][cs2_key_json]["total"]

        return (
            basic_layout(
                tab3_bar_bigfig(
                    country, 
                    segmentation, 
                    individual_segment_lst, 
                    broad_topic_lst,
                    switch_cs1,
                    cs1_key_json,
                    switch_cs2,
                    cs2_key_json,
                )
            ).update_layout({
                "margin": {"t": 25}
            }),
            pills_lst,
            cs1_count,
            cs2_count
        )

    @app.callback(
        Output('comp12_dropdown_ua_cs1_tab3_IN', 'value'),
        Input('comp7_dropdown_segmentation_tab3_IN', 'value'),
        State('comp12_dropdown_ua_cs1_tab3_IN', 'value'),
        prevent_initial_call=True
    )
    def preserve_custom_segment(segmentation, current_value):
        # Don't change the value, just return what it already was
        return current_value if current_value else 'None'


############################################## tab 4 ##############################################

    @app.callback(
        Output("comp9_dropdown_n_topic_tab4_IN", "data"),
        Output("comp9_dropdown_n_topic_tab4_IN", "value"),
        Input("comp9_dropdown_b_topic_tab4_IN", "value"),
        State("comp9_dropdown_segmentation_tab4_IN", "value"),
        State("comp9_dropdown_n_topic_tab4_IN", "value")
    )
    def filter_niche_by_broad(broad_topics, segmentation, current_niches):
        df = tab3_data["niche"][segmentation]
        
        if not broad_topics:
            niche_options = df["niche"].unique().tolist()
        else:
            niche_mk = df["broad_type"].isin(broad_topics)
            niche_options = df[niche_mk]["niche"].unique().tolist()
        
        if current_niches:
            new_value = [n for n in current_niches if n in niche_options]
        else:
            new_value = []
        
        if not new_value and niche_options:
            new_value = [niche_options[0]]

        return niche_options, new_value

    @app.callback(
        Output("comp10_bigfig_tab4_OUT", "figure"),
        Output("comp9_basicsegments_pills_tab4", "children"),
        Output("comp13_cs1_text_tab4_OUT", "children"),
        Output("comp18_cs2_text_tab4_OUT", "children"),  
        Input("comp9_dropdown_sc_tab4_IN", "value"),
        Input("comp9_dropdown_country_tab4_IN", "value"),
        Input("comp9_dropdown_segmentation_tab4_IN", "value"),
        Input("comp9_dropdown_individual_segments_tab4_IN", "value"),
        Input("comp9_dropdown_b_topic_tab4_IN", "value"),
        Input("comp9_dropdown_n_topic_tab4_IN", "value"),
        Input("comp9_dropdown_time_tab4_IN", "value"),
        Input("comp13_dropdown_switch_cs1_tab4_IN", "checked"),        
        Input("comp13_dropdown_ua_cs1_tab4_IN", "value"),
        Input("comp13_dropdown_spr_cs1_tab4_IN", "value"),
        Input("comp13_dropdown_cs_cs1_tab4_IN", "value"),
        Input("comp13_dropdown_ten_cs1_tab4_IN", "value"),
        Input("comp18_dropdown_switch_cs2_tab4_IN", "checked"),
        Input("comp18_dropdown_ua_cs2_tab4_IN", "value"),
        Input("comp18_dropdown_spr_cs2_tab4_IN", "value"),
        Input("comp18_dropdown_cs_cs2_tab4_IN", "value"),
        Input("comp18_dropdown_ten_cs2_tab4_IN", "value")        

    )
    def callback_tab4_out(
        specificity,
        country, 
        segmentation, 
        individual_segment_lst, 
        broad_topic_lst,
        niche_topic_lst,
        time_slice,
        switch_cs1,
        ua_cs1,
        spr_cs1,
        cs_cs1,
        ten_cs1,
        switch_cs2,
        ua_cs2,
        spr_cs2,
        cs_cs2,
        ten_cs2
    ):
        if not broad_topic_lst:
            broad_topic_lst = ["crop"]
        if not broad_topic_lst:
            broad_topic_lst = ["maize"]
        if not individual_segment_lst:
            individual_segment_lst = ["1", "2", "3", "4", "5"]
        if not country:
            country = tab2_data["Count"]["question_user_country_code"].unique()
        if not ua_cs1:
            ua_cs1 = none_to_string(ua_cs1)
        if not spr_cs1:
            spr_cs1 = none_to_string(spr_cs1)
        if not cs_cs1:
            cs_cs1 = none_to_string(cs_cs1)
        if not ten_cs1:
            ten_cs1 = none_to_string(ten_cs1)
        if not ua_cs2:
            ua_cs2 = none_to_string(ua_cs2)
        if not spr_cs2:
            spr_cs2 = none_to_string(spr_cs2)
        if not cs_cs2:
            cs_cs2 = none_to_string(cs_cs2)
        if not ten_cs2:
            ten_cs2 = none_to_string(ten_cs2)

        df_segmentation = tab2_data[segmentation]
        df_country = df_segmentation[df_segmentation["question_user_country_code"].isin(country)]

        df_segment_count_dct_lst = {
            segment: df_country[df_country[segmentation]==segment]["n"].sum()
            for segment in individual_segment_lst
        }

        pills_lst = []
        for segment, count in df_segment_count_dct_lst.items():
            pills_lst.append(
                dmc.Badge(
                    f"{count}",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color=segment_colors_dct[segment],
                    style={"color": "white"}
                )
            )

        cs1_combo_dct = {
            "Reach": none_to_list(cs_cs1),
            "Speed": none_to_list(spr_cs1),
            "Tenure": none_to_list(ten_cs1),
            "Count": none_to_list(ua_cs1)
        }

        cs1_key_json = json.dumps(cs1_combo_dct, sort_keys=True)
        cs1_count = intersections["counts"][cs1_key_json]["total"]


        cs2_combo_dct = {
            "Reach": none_to_list(cs_cs2),
            "Speed": none_to_list(spr_cs2),
            "Tenure": none_to_list(ten_cs2),
            "Count": none_to_list(ua_cs2)
        }

        cs2_key_json = json.dumps(cs2_combo_dct, sort_keys=True)
        cs2_count = intersections["counts"][cs2_key_json]["total"]


        if specificity=="Broad":
            return (
                basic_layout(
                    tab4_broad_bigfig(
                        country, 
                        segmentation, 
                        individual_segment_lst, 
                        broad_topic_lst,
                        time_slice,
                        switch_cs1,
                        cs1_key_json,
                        switch_cs2,
                        cs2_key_json
                    )
                ).update_layout({
                    "margin": {"t": 25}
                }),
                pills_lst,
                cs1_count,
                cs2_count
            )
        else:
            return (
                basic_layout(
                    tab4_niche_bigfig(
                        country, 
                        segmentation, 
                        individual_segment_lst, 
                        broad_topic_lst,
                        niche_topic_lst,
                        time_slice,
                        switch_cs1,
                        cs1_key_json,
                        switch_cs2,
                        cs2_key_json
                    )
                ).update_layout({
                    "margin": {"t": 25}
                }),
                pills_lst,
                cs1_count,
                cs2_count
            )
    @app.callback(
        Output("comp12_dropdown_checked_show_cs1_tab3_OUT", "style"),
        Output("comp17_dropdown_checked_show_cs2_tab3_OUT", "style"),
        Output("comp13_dropdown_checked_show_cs1_tab4_OUT", "style"),
        Output("comp18_dropdown_checked_show_cs2_tab4_OUT", "style"),
        Input("comp12_dropdown_switch_cs1_tab3_IN", "checked"),
        Input("comp17_dropdown_switch_cs2_tab3_IN", "checked"),
        Input("comp13_dropdown_switch_cs1_tab4_IN", "checked"),
        Input("comp18_dropdown_switch_cs2_tab4_IN", "checked")
    )
    def pills_tab3_tab4_checked(
        cs1_tab3,
        cs2_tab3,
        cs1_tab4,
        cs2_tab4
    ):
        cs1_tab3_style = {"display": "flex"} if cs1_tab3 else {"display": "none"}
        cs2_tab3_style = {"display": "flex"} if cs2_tab3 else {"display": "none"}
        cs1_tab4_style = {"display": "flex"} if cs1_tab4 else {"display": "none"}
        cs2_tab4_style = {"display": "flex"} if cs2_tab4 else {"display": "none"}

        return (cs1_tab3_style, cs2_tab3_style, cs1_tab4_style, cs2_tab4_style)

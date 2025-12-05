import pandas as pd
import numpy as np

from dash import html, dcc, _dash_renderer
from dash_iconify import DashIconify
import dash_mantine_components as dmc
_dash_renderer._set_react_version('18.2.0')

from data import tab1_data, tab2_data, tab3_data, tab4_data
from charts import tab1_geo_fig
from color import basic_layout, segment_colors_dct

# # # # # # # # # # # # # # basic layout # # # # # # # # # # # # # # 

############################################## tab 1 ##############################################

comp1_geo_fig_tab1 = dmc.Card(
    [
        dcc.Graph(
            figure=basic_layout(tab1_geo_fig), 
            id="comp1_geo_fig_tab1", 
        )
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp1_geo_card"
)

comp3_text = dmc.Card(
    [
        dmc.Text(
            [
                "DataKind DataKit: Smallholder Farmers"
            ],
            fw=500,
            size="l",
            className="text_header"
        ),
        dmc.Text(
            "Smallholder farmers are individuals or families who manage relatively small plots of land, often relying on family labor and traditional farming methods. Despite their small scale, they play a central role in global food systems, producing up to one-third of the world’s food supply and forming the backbone of rural economies across Africa, Asia, and Latin America. Their livelihoods are closely tied to the land and weather, making them both essential contributors to food security, and highly vulnerable to environmental and market changes.",
            c="gray",
            size="xs",
            className="text_standard_intro"
        ),
        dmc.Text(
            "Understanding smallholder farmers and the challenges they face is key for building resilient agricultural systems and sustainable rural development. By studying their behaviors and needs organizations can design better tools, information services, and policies that directly improve productivity, income, and climate resilience. Data-driven insights into their practices not only empower farmers themselves, but also strengthen local economies and contribute to broader goals such as poverty reduction and food sustainability.",
            c="gray",
            size="xs",
            className="text_standard_intro text_nomargin"
        ),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp3_text_card"
)

inline_comp_3_0 = html.Div(
    [
        comp3_text,
    ],
    className="in inline_comp_3_0"
)

tab1 = html.Div(
    [
        inline_comp_3_0,
        comp1_geo_fig_tab1
    ],
    className="d d1"
)


############################################## tab 2 ##############################################
comp4_dropdown_tab2 = dmc.Card(
    [
        dmc.Text(
            [
                "Basic segments"
            ],
            fw=500,
            size="md",
            className="text_header"
        ),
        dmc.MultiSelect(
                label="Country",
                placeholder="select...",
                value=tab2_data["Count"]["question_user_country_code"].unique(),
                data=tab2_data["Count"]["question_user_country_code"].unique(),
                clearable=False,
                id="comp4_dropdown_country_tab2_IN"
            ),
        dmc.Select(
                label="Segmentation",
                placeholder="select...",
                value="Count",
                data=list(tab2_data.keys()),
                clearable=False,
                id="comp4_dropdown_segmentation_tab2_IN"
            ),
        html.Div(
            [
                dmc.Badge(
                    id="comp3_s1_text_tab2_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color=segment_colors_dct["1"],
                    style={"color": "white"}
                ),
                dmc.Badge(
                    id="comp3_s2_text_tab2_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color=segment_colors_dct["2"],
                    style={"color": "white"}
                ),
                dmc.Badge(
                    id="comp3_s3_text_tab2_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color=segment_colors_dct["3"],
                    style={"color": "white"}
                ),
                dmc.Badge(
                    id="comp3_s4_text_tab2_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color=segment_colors_dct["4"],
                    style={"color": "white"}
                ),
                dmc.Badge(
                    id="comp3_s5_text_tab2_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color=segment_colors_dct["5"],
                    style={"color": "white"}
                )

            ],
            className="flex-parent basic-segments"
        )
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t f-child comp3_dropdown_tab2_card"
)


comp4_center_filter_tab2 = html.Div(
    [
        comp4_dropdown_tab2
    ],
    className="f f-parent"
)


comp5_hist_fig_tab2 = dmc.Card(
    [
        dcc.Graph(figure={}, id="comp5_hist_fig_tab2_OUT")
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp5_hist_fig_tab2_card"   
)

comp6_pie_fig_tab2 = dmc.Card(
    [
        dcc.Graph(figure={}, id="comp6_pie_fig_tab2_OUT")
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp6_pie_fig_tab2_card"   
)

comp14_description_text_tab2 = dmc.Card(
    [
        dmc.Text(
            [
                "Segmentation description"
            ],
            fw=500,
            size="md",
            className="text_header"
        ),
        dmc.Text(
            [
                "Each segmentation is created on an ordinal scale of 1 to 5, with 1 being low, and being high. Buckets were created manually from analyzing the distribution of the variable."
            ],
            size="xs",
            c="gray",
            className="text_standard_intro"
        ),
        dmc.Text(
            [
                """For example, in the "Speed" segmentation, which examined how fast a user responded to a question, segment 5 is comprised of users who responded within thirty seconds, segement 4 is users who responded between thirty seconds and two minutes, segment 3 is users who responded between three minutes and twelve minutes, segment 2 is users who responded between twelve minutes and three days, and segment 1 is users who responded after three days."""
            ],
            size="xs",
            c="gray",
            className="text_standard_intro"
        ),
        dmc.Text(
            [
                dcc.Markdown(
                    """Each segment comprises at least 5% of the data. The notebook that defines the segment bins can be found [here] (https://github.com/datakind/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%203_Community%20Leaders/benjamin_noyes/05_groupby_segmentation/DataKit_Challenge_3_identifying_community_leaders_leader_analysis_groupbys%20(3).ipynb).""",
                    link_target="_blank",
                ),
            ],
            size="xs",
            c="gray",
            className="text_standard_intro text_nomargin"
        )
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp14_description_tab2_card",
)
comp14_description_text_inline_tab2 = html.Div(
    [
        comp6_pie_fig_tab2,
        comp14_description_text_tab2
    ],
    className="in comp14_description_text_inline_tab2"
)

grid_tab2 = html.Div(
    [
        comp5_hist_fig_tab2,
        comp14_description_text_inline_tab2,
    ],
    className="d d2"

)

tab2 = html.Div(
    [
        comp4_center_filter_tab2,
        grid_tab2
    ],
    className="a tab2_all"
)


############################################## tab 5 (2.5, between 2 and 3) ##############################################

comp19_dropdown_cs_tab5 = dmc.Card(
 [
        dmc.Text(
            [
                "Custom segment"
            ],
            fw=500,
            size="md",
            className="text_header"
        ),
        dmc.MultiSelect(
            label="Country",
            placeholder="select multiple...",
            value=tab2_data["Count"]["question_user_country_code"].unique(),
            data=tab2_data["Count"]["question_user_country_code"].unique(),
            maxValues=2,
            clearable=False,
            id="comp19_dropdown_country_cs_tab5_IN"
        ),        
        dmc.Select(
            label="Count",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp19_dropdown_ua_cs_tab5_IN"
        ),
        dmc.Select(
            label="Speed",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp19_dropdown_spr_cs_tab5_IN"
        ),
        dmc.Select(
            label="Reach",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp19_dropdown_cs_cs_tab5_IN"
        ),
        dmc.Select(
            label="Tenure",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp19_dropdown_ten_cs_tab5_IN"
        ),
        html.Div(
            [
                dmc.Badge(
                    id="comp19_cs_text_tab5_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color="#9F90E8",
                    style={"color": "white"}
                )
            ],
            className="flex-parent"
        )
        
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t f-child comp19_cs_dropdown_tab5_card"
)

comp20_funnel_fig_tab5 = dmc.Card(
    [   
        dcc.Graph(
            figure={},
            id="comp20_funnel_fig_tab5_OUT"
        )
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp20_funnel_fig_tab5"
)


comp21_center_filter_tab5 = html.Div(
    [
        comp19_dropdown_cs_tab5
    ],
    className="f f-parent"
)

tab5 = html.Div(
    [
        comp21_center_filter_tab5,
        comp20_funnel_fig_tab5
    ],
    className="a tab5_all"
)

############################################## tab 3 ##############################################
comp22_dropdown_country_tab3 = dmc.Card(
    [
        dmc.MultiSelect(
            label="Country",
            placeholder="select multiple...",
            value=tab2_data["Count"]["question_user_country_code"].unique(),
            data=tab2_data["Count"]["question_user_country_code"].unique(),
            maxValues=2,
            clearable=False,
            id="comp7_dropdown_country_tab3_IN"
        ),     
    ],
    withBorder=True,
    shadow="xs",
    radius="md",
    className="t f-top-child bottomcomp22_dropdown_country_tab3"
)

comp7_dropdown_tab3 = dmc.Card(
    [
        dmc.Text(
            [
                "Basic segments"
            ],
            fw=500,
            size="md",
            className="text_header"
        ),
        dmc.Select(
                label="Segmentation",
                placeholder="...",
                value="Count",
                data=list(tab2_data.keys()),
                clearable=False,
                id="comp7_dropdown_segmentation_tab3_IN"
            ),
        dmc.MultiSelect(
            label="Individual segments",
            placeholder="select multiple...",
            value=["1", "5"],
            data=["1", "2", "3", "4", "5"],
            clearable=False,
            id="comp7_dropdown_individual_segment_tab3_IN"
        ),
        html.Div(
            id="comp7_basicsegments_pills_tab3",
            className="flex-parent basic-segments"
        )

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t f-child comp7_dropdown_tab3_card"
)

comp15_topic_dropdown_tab3 = dmc.Card(
    [
        dmc.Text(
            [
                "Topic"
            ],
            fw=500,
            size="md",
            className="text_header"
        ), 
        dmc.MultiSelect(
            label="Broad topic",
            placeholder="select multiple...",
            value=["livestock"],
            data=tab3_data["niche"]["Count"]["broad_type"].unique(),
            clearable=True,
            maxValues=4,
            id="comp7_dropdown_b_topic_tab3_IN"
        )        
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp15_topic_dropdown_tab3_card"    
)


comp12_customsegment1_dropdown_tab3 = dmc.Card(
    [
        dmc.Switch(
            labelPosition="left",
            label="Custom segment 1",
            size="md",
            radius="lg",
            color="#9F90E8",
            checked=False,
            disabled=False,
            withThumbIndicator=False,
            id="comp12_dropdown_switch_cs1_tab3_IN",
            className="text_header",
        ),
        dmc.Select(
            label="Count",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp12_dropdown_ua_cs1_tab3_IN"
        ),
        dmc.Select(
            label="Speed",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp12_dropdown_spr_cs1_tab3_IN"
        ),
        dmc.Select(
            label="Reach",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp12_dropdown_cs_cs1_tab3_IN"
        ),
        dmc.Select(
            label="Tenure",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp12_dropdown_ten_cs1_tab3_IN"
        ),
        html.Div(
            [
                dmc.Badge(
                    id="comp12_cs1_text_tab3_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color="#9F90E8",
                    style={"color": "white"}
                )
            ],
            className="flex-parent",
            id="comp12_dropdown_checked_show_cs1_tab3_OUT"
        )
        
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp12_cs1_dropdown_tab3_card"
)

comp17_customsegment2_dropdown_tab3 = dmc.Card(
    [
        dmc.Switch(
            labelPosition="left",
            label="Custom segment 2",
            size="md",
            radius="lg",
            color="black",
            checked=False,
            disabled=False,
            withThumbIndicator=False,
            id="comp17_dropdown_switch_cs2_tab3_IN",
            className="text_header",
        ),
        dmc.Select(
            label="Count",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp17_dropdown_ua_cs2_tab3_IN"
        ),
        dmc.Select(
            label="Speed",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp17_dropdown_spr_cs2_tab3_IN"
        ),
        dmc.Select(
            label="Reach",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp17_dropdown_cs_cs2_tab3_IN"
        ),
        dmc.Select(
            label="Tenure",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp17_dropdown_ten_cs2_tab3_IN"
        ),
        html.Div(
            [
                dmc.Badge(
                    id="comp17_cs2_text_tab3_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color="black",
                    style={"color": "white"}
                ) 
            ],
            className="flex-parent",
            id="comp17_dropdown_checked_show_cs2_tab3_OUT"
        )
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp17_cs2_dropdown_tab3_card"
)

comp23_bottom_filter_tab3 = html.Div(
    [
        comp7_dropdown_tab3,
        comp12_customsegment1_dropdown_tab3,
        comp17_customsegment2_dropdown_tab3,
        comp15_topic_dropdown_tab3
    ],
    className="f f-bottom-child"
)
comp7_center_filter_tab3 = html.Div(
    [
        comp22_dropdown_country_tab3,
        comp23_bottom_filter_tab3
    ],
    className="f f-all"
)
comp24_all_filters_tab3 = html.Div(
    [
        comp7_center_filter_tab3
    ],
    className="f f-all-outer"
)

comp8_bigfig_tab3 = dmc.Card(
    [
        dcc.Graph(figure={}, id="comp8_bigfig_tab3_OUT", style={"height": "100%"})
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp8_bigfig_tab3_card",
    style={"height": "100%"}

)

tab3 = html.Div(
    [
        comp24_all_filters_tab3,
        comp8_bigfig_tab3
    ],
    className="a tab3_all"
)

############################################## tab 4 ##############################################
comp35_dropdown_country_tab4 = dmc.Card(
    [
        dmc.MultiSelect(
            label="Country",
            placeholder="select multiple...",
            value=tab2_data["Count"]["question_user_country_code"].unique(),
            data=tab2_data["Count"]["question_user_country_code"].unique(),
            maxValues=2,
            clearable=False,
            id="comp9_dropdown_country_tab4_IN"
        ),     
    ],
    withBorder=True,
    shadow="xs",
    radius="md",
    className="t f-top-child bottomcomp25_dropdown_country_tab4"
)


comp9_dropdown_tab4 = dmc.Card(
    [
       dmc.Text(
            [
                "Basic segments"
            ],
            fw=500,
            size="md",
            className="text_header"
        ),
        dmc.Select(
                label="Segmentation",
                placeholder="select...",
                value="Count",
                data=list(tab2_data.keys()),
                clearable=False,
                id="comp9_dropdown_segmentation_tab4_IN"
            ),
        dmc.MultiSelect(
            label="Individual segments",
            placeholder="select multiple...",
            value=["1", "5"],
            data=["1", "2", "3", "4", "5"],
            clearable=False,
            id="comp9_dropdown_individual_segments_tab4_IN"
        ),
        html.Div(
            id="comp9_basicsegments_pills_tab4",
            className="flex-parent basic-segments"
        )        

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t f-child comp9_dropdown_tab4_card"
)

comp16_topic_dropdown_tab4 = dmc.Card(
    [
       dmc.Text(
            [
                "Topic over time"
            ],
            fw=500,
            size="md",
            className="text_header"
        ),
        dmc.SegmentedControl(
            orientation="horizontal",
            id="comp9_dropdown_sc_tab4_IN",
            value="Broad",
            style={"width": "100%"},
            data=[
                {"value": "Broad", "label": "Broad"},
                {"value": "Niche", "label": "Niche"},
            ],
        ),
       dmc.MultiSelect(
            label="Broad topic",
            placeholder="select multiple...",
            value=["livestock"],
            data=tab3_data["niche"]["Count"]["broad_type"].unique(),
            maxValues=4,
            clearable=True,
            id="comp9_dropdown_b_topic_tab4_IN"
        ),
        dmc.MultiSelect(
            label="Niche topic",
            placeholder="select multiple...",
            value=["animals"],
            data=tab3_data["niche"]["Count"]["niche"].unique(),
            maxValues=4,
            clearable=True,
            id="comp9_dropdown_n_topic_tab4_IN"
        ),
        dmc.Select(
            label="Time slice",
            placeholder="select...",
            value=list(tab4_data["broad"]["Count"].keys())[0],
            data=list(tab4_data["broad"]["Count"].keys()),
            clearable=True,
            id="comp9_dropdown_time_tab4_IN"
        ) 
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp16_topic_dropdown_tab4_card"
)

comp13_customsegment1_dropdown_tab4 = dmc.Card(
    [
        dmc.Switch(
            labelPosition="left",
            label="Custom segment 1",
            size="md",
            radius="lg",
            color="#9F90E8",
            checked=False,
            disabled=False,
            withThumbIndicator=False,
            id="comp13_dropdown_switch_cs1_tab4_IN",
            className="text_header",
        ),
        dmc.Select(
            label="Count",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp13_dropdown_ua_cs1_tab4_IN"
        ),
        dmc.Select(
            label="Speed",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp13_dropdown_spr_cs1_tab4_IN"
        ),
        dmc.Select(
            label="Reach",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp13_dropdown_cs_cs1_tab4_IN"
        ),
        dmc.Select(
            label="Tenure",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp13_dropdown_ten_cs1_tab4_IN"
        ),
        html.Div(
            [
                dmc.Badge(
                    id="comp13_cs1_text_tab4_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color="#9F90E8",
                    style={"color": "white"}
                ) 
            ],
            className="flex-parent",
            id="comp13_dropdown_checked_show_cs1_tab4_OUT"
        )

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp13_cs1_dropdown_tab4_card"
)


comp18_customsegment2_dropdown_tab4 = dmc.Card(
    [
        dmc.Switch(
            labelPosition="left",
            label="Custom segment 2",
            size="md",
            radius="lg",
            color="black",
            checked=False,
            disabled=False,
            withThumbIndicator=False,
            id="comp18_dropdown_switch_cs2_tab4_IN",
            className="text_header",
        ),
        dmc.Select(
            label="Count",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp18_dropdown_ua_cs2_tab4_IN"
        ),
        dmc.Select(
            label="Speed",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp18_dropdown_spr_cs2_tab4_IN"
        ),
        dmc.Select(
            label="Reach",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp18_dropdown_cs_cs2_tab4_IN"
        ),
        dmc.Select(
            label="Tenure",
            placeholder="intersection...",
            value="None",
            data=["None", "1", "2", "3", "4", "5"],
            clearable=False,
            id="comp18_dropdown_ten_cs2_tab4_IN"
        ),
        html.Div(
            [
                dmc.Badge(
                    id="comp18_cs2_text_tab4_OUT",
                    size="lg",
                    variant="filled",
                    radius="xl",
                    color="black",
                    style={"color": "white"}
                ) 
            ],
            className="flex-parent",
            id="comp18_dropdown_checked_show_cs2_tab4_OUT"
        )
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp18_cs2_dropdown_tab4_card"
)

comp26_bottom_filter_tab4 = html.Div(
    [
        comp9_dropdown_tab4,
        comp13_customsegment1_dropdown_tab4,
        comp18_customsegment2_dropdown_tab4,        
        comp16_topic_dropdown_tab4
    ],
    className="f f-bottom-child"
)
comp36_center_filter_tab4 = html.Div(
    [
        comp35_dropdown_country_tab4,
        comp26_bottom_filter_tab4
    ],
    className="f f-all"
)
comp37_all_filters_tab4 = html.Div(
    [
        comp36_center_filter_tab4
    ],
    className="f f-all-outer"
)

comp10_bigfig_tab4 = dmc.Card(
    [
        dcc.Graph(figure={}, id="comp10_bigfig_tab4_OUT")
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t comp10_bigfig_tab4_card"
)

tab4 = html.Div(
    [
        comp37_all_filters_tab4,
        comp10_bigfig_tab4,
    ],
    className="a tab4_all"
)


# # # # # # # # # # # # # # tabs # # # # # # # # # # # # # # 

Tabs = html.Div(
    [
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.TabsTab(
                            "Geography",
                            leftSection=DashIconify(icon="material-symbols:travel-explore-rounded", width=20, color="black", className="icons-2"),
                            value="Geography"
                        ),
                        dmc.TabsTab(
                            "Basic segments",
                            leftSection=DashIconify(icon="material-symbols:modeling-outline-rounded", width=20, color="black", className="icons-2"),
                            value="Segments"),
                        dmc.TabsTab(
                            "Custom segments",
                            leftSection=DashIconify(icon="ph:funnel-bold", width=20, color="black", className="icons-2"),
                            value="Custom"),
                        dmc.TabsTab(
                            "Topics",
                            leftSection=DashIconify(icon="material-symbols:explore-outline-rounded", width=20, color="black", className="icons-2"),
                            value="Topics"
                        ),
                        dmc.TabsTab(
                            "Time",
                            leftSection=DashIconify(icon="ph:line-segments", width=20, color="black", className="icons-2"),
                            value="Time"
                        )
                    ]
                ),
                dmc.TabsPanel(
                    tab1,
                    value="Geography"
                ),
                dmc.TabsPanel(
                    tab2,
                    value="Segments"
                ),
                dmc.TabsPanel(
                    tab5,
                    value="Custom"
                ),
                dmc.TabsPanel(
                    tab3,
                    value="Topics"
                ),        
                dmc.TabsPanel(
                    tab4,
                    value="Time"
                ),
            ],
            color="blue",
            value="Geography",
            variant="outline"
        )
    ],
    className="tabs_main nm"
)


# # # # # # # # # # # # # # title # # # # # # # # # # # # # #


title = dmc.Card(
    [
        dmc.Text(
            "Smallholder Farmers in East Africa",
            size="xl",
            fw=600
            ),
        dmc.Text(
            """WeFarm SMS service: What questions were leaders asking?""",
            size="sm",
            fw=600
            )        
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t tit nm",
)

# # # # # # # # # # # # # # footer # # # # # # # # # # # # # #

color = "white"

icon_datakind = html.Img(src="/assets/DK_LOGO_R_ORG-2.png", style={"width": "100px"})
link_datakind = "https://www.datakind.org/"

icon_producers_direct = html.Img(src="/assets/Producers-Direct_Logo_500x500.png", style={"width": "100px"})
link_producers_direct = "https://producersdirect.org/"


comp32_datakind = dmc.Anchor(
    icon_datakind, href=link_datakind, target="_blank",
    size="xl",
    className="footnt-child"
)

comp33_producers_direct = dmc.Anchor(
    icon_producers_direct, href=link_producers_direct, target="_blank",
    size="xl",
    className="footnt-child"
)

comp25_copyrightfooter = html.P(
    "© Benjamin Noyes 2025 all rights reserved",
    className="footertinytext"
)

comp34_datakind_parent = html.Div(
    [
        comp32_datakind
    ],
    className="footnt-parent"
)

comp35_datakind_parent = html.Div(
    [
        comp33_producers_direct
    ],
    className="footnt-parent"
)


comp26_icons = html.Div(
    [
        comp34_datakind_parent,
        comp35_datakind_parent
    ],
    className="footie-middle"
)


footer = dmc.Card(
    [
        comp26_icons,
        comp25_copyrightfooter
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="t footie-all nm",
)

# # # # # # # # # # # # # # mobile # # # # # # # # # # # # # #

mobile_error = html.Div(
    [
        dmc.Card(
            [
                dmc.Text(
                    "This dashboard is not optimized for mobile. Please access from a desktop.",
                    size="xs",
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            className="mn-1"
        )
    ],
    className="mn-2"
)
############################### composition ##################################

lyt = dmc.MantineProvider(
    [
        title,
        Tabs,
        footer,
        mobile_error
    ]
)
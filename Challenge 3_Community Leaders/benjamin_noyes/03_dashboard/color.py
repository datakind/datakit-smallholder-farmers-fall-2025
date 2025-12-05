segment1_color = "#A1A1A1"
segment2_color = "#F9C926"
segment3_color = "#DC7326"
segment4_color = "#4897CD"
segment5_color = "#2E9999"

segment_colors_dct = {
  "1": segment1_color,
  "2": segment2_color,
  "3": segment3_color,
  "4": segment4_color,
  "5": segment5_color
}

def basic_layout(fig):
    return fig.update_layout({
        "clickmode": "select",
        "margin": {"r":0,"l":0,"b":0}
    })
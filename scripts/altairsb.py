import pandas as pd
import altair as alt

# Load the cleaned CSV
df = pd.read_csv("../data/cleaned_synbiohub_parts.csv")

# Extract year from 'created' using ISO8601 format to handle mixed formats
df['year'] = pd.to_datetime(df['created'], format='ISO8601', errors='coerce').dt.year

# Replace NaN in 'type' with 'Unidentified'
df['type'] = df['type'].fillna('Unidentified')

# Remove types that start with 'SO:'
df = df[~df['type'].str.startswith('SO:')]

# Group by 'type' and 'year', count occurrences
counts = df.groupby(['type', 'year']).size().reset_index(name='count')

# Explicitly show all years present in the data
all_years = sorted(df['year'].dropna().unique())
all_types = counts['type'].unique()
full_index = pd.MultiIndex.from_product([all_types, all_years], names=['type', 'year'])
counts = counts.set_index(['type', 'year']).reindex(full_index, fill_value=0).reset_index()

# Filter to show only years between 2002 and 2016 (inclusive)
counts = counts[(counts['year'] >= 2002) & (counts['year'] <= 2016)]

# Altair interactive chart with legend highlight (dims others), no horizontal grid lines or y-axis ticks
selection = alt.selection_point(fields=['type'], bind='legend')

line = alt.Chart(counts).mark_line().encode(
    x=alt.X('year:O', scale=alt.Scale(padding=0.1)),
    y=alt.Y('count:Q', axis=alt.Axis(grid=False, ticks=False)),
    color='type:N',
    tooltip=['type:N', 'year:O', 'count:Q'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
).add_params(selection)

points = alt.Chart(counts).mark_point(size=30).encode(
    x='year:O',
    y=alt.Y('count:Q', axis=alt.Axis(grid=False, ticks=False)),
    color='type:N',
    tooltip=['type:N', 'year:O', 'count:Q'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
)

chart = (line + points).properties(width=900, height=500).interactive()
chart = chart.configure_axis(domain=False, ticks=False).configure_view(strokeWidth=0)

# Add title and subtitle with formatting
title = alt.TitleParams(
    text="How Synthetic Biology Design Repositories Grew Over Time",
    subtitle=[
        "Annual count of part submissions by biological category",
        "Interactive: use legend to highlight individual types"
    ],
    anchor="middle",
    fontSize=18,
    subtitleFontSize=12
)

chart = chart.properties(title=title).configure_title(
    fontSize=18, subtitleFontSize=12, fontWeight='bold', anchor='start'
)

# Save the chart to an HTML file & print confirmation
chart.save('../outputs/chart.html')
print("Chart saved as chart.html. Open this file in your browser to view the interactive visualization.")
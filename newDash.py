import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from shared import translated_negative_reviews as data

# Define the mappings for categories and languages
category_language_mapping = {
    "User Interface Issues": {
        "TR": "Kullanıcı Arayüzü Sorunları (TR)",
        "EN": "User Interface Issues (EN)"
    },
    "Performance Problems": {
        "TR": "Performans Sorunları (TR)",
        "EN": "Performance Problems (EN)"
    },
    "Job Search Functionality": {
        "TR": "İş Arama İşlevselliği (TR)",
        "EN": "Job Search Functionality (EN)"
    },
    "Notification Issues": {
        "TR": "Bildirim Sorunları (TR)",
        "EN": "Notification Issues (EN)"
    },
    "Application Process": {
        "TR": "Başvuru Süreci (TR)",
        "EN": "Application Process (EN)"
    },
    "Profile Management": {
        "TR": "Profil Yönetimi (TR)",
        "EN": "Profile Management (EN)"
    },
    "Customer Support": {
        "TR": "Müşteri Desteği (TR)",
        "EN": "Customer Support (EN)"
    },
    "Account Management": {
        "TR": "Hesap Yönetimi (TR)",
        "EN": "Account Management (EN)"
    }
}

# Flatten the mapping for easier access
flattened_mapping = {v[lang]: k for k, v in category_language_mapping.items() for lang in v}

# Start the app with a more visually appealing Bootstrap theme (LUX theme)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Prepare UI layout
app.layout = dbc.Container(
    [
        html.H2("📊 Negative Reviews Dashboard", style={'text-align': 'center', 'margin-bottom': '30px', 'font-weight': 'bold'}),
        
        # Sidebar and main panel
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Sidebar for filtering options
                        dbc.Card(
                            [
                                dbc.CardHeader("Filters", style={"background-color": "#f8f9fa", "font-size": "18px", "font-weight": "bold"}),
                                dbc.CardBody(
                                    [
                                        # Select Category Dropdown
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Label("Select Category"), width=12),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id="category",
                                                        options=[{'label': k, 'value': k} for k in category_language_mapping.keys()],
                                                        value="User Interface Issues",
                                                        style={"margin-bottom": "10px"}
                                                    ),
                                                    width=12
                                                ),
                                            ]
                                        ),
                                        # Select Language Radio Buttons
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Label("Select Language"), width=12),
                                                dbc.Col(
                                                    dcc.RadioItems(
                                                        id="language",
                                                        options=[
                                                            {'label': 'Turkish', 'value': 'TR'},
                                                            {'label': 'English', 'value': 'EN'}
                                                        ],
                                                        value="TR",
                                                        labelStyle={'margin-right': '10px'}
                                                    ),
                                                    width=12
                                                ),
                                            ],
                                            style={"margin-bottom": "15px"}
                                        ),
                                        # Keyword Search Input
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Label("Keyword Search"), width=12),
                                                dbc.Col(
                                                    dbc.Input(id="keyword", placeholder="Enter a keyword", type="text", style={"margin-bottom": "10px"}),
                                                    width=12
                                                ),
                                            ]
                                        ),
                                        # Show Comments Button (replacing block=True with className="w-100")
                                        dbc.Button("Show Comments", id="show_comments", color="primary", n_clicks=0, className="mt-3 w-100"),
                                    ]
                                ),
                            ],
                            style={"margin-bottom": "20px", "box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border": "1px solid #ddd"}
                        ),
                    ],
                    width=3
                ),
                dbc.Col(
                    [
                        # Row for displaying stats
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("📝 Total Comments", className="card-title"),
                                                html.P(id="total_comments", className="card-text", style={"font-size": "24px", "font-weight": "bold"})
                                            ]
                                        ),
                                        className="mb-4",
                                        style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border": "1px solid #ddd"}
                                    ),
                                    width=4
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("📈 Highest Commented Category", className="card-title"),
                                                html.P(id="highest_category", className="card-text", style={"font-size": "20px", "font-weight": "bold"})
                                            ]
                                        ),
                                        className="mb-4",
                                        style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border": "1px solid #ddd"}
                                    ),
                                    width=4
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("📉 Lowest Commented Category", className="card-title"),
                                                html.P(id="lowest_category", className="card-text", style={"font-size": "20px", "font-weight": "bold"})
                                            ]
                                        ),
                                        className="mb-4",
                                        style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border": "1px solid #ddd"}
                                    ),
                                    width=4
                                ),
                            ]
                        ),
                        
                        # Bar Chart for Comments by Category
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Bar Chart of Comments by Category 📊", className="card-title"),
                                    dcc.Graph(id="comments_bar_chart")
                                ]
                            ),
                            className="mb-4",
                            style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border": "1px solid #ddd"}
                        ),
                        
                        # Identified Patterns Section
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Identified Patterns 🔍", className="card-title"),
                                    html.P(id="identified_patterns", style={"white-space": "pre-line"})
                                ]
                            ),
                            className="mb-4",
                            style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border": "1px solid #ddd"}
                        ),
                        
                        # Comments Section
                        html.Div(id="comments_section", style={'margin-top': '20px'})
                    ],
                    width=9
                )
            ]
        )
    ],
    fluid=True
)

# Callback to handle the filtering of data based on category, language, and keyword
@app.callback(
    Output("total_comments", "children"),
    Output("highest_category", "children"),
    Output("lowest_category", "children"),
    Output("comments_bar_chart", "figure"),
    Output("identified_patterns", "children"),
    Output("comments_section", "children"),
    Input("category", "value"),
    Input("language", "value"),
    Input("keyword", "value"),
    Input("show_comments", "n_clicks"),
)
def update_dashboard(category, language, keyword, n_clicks):
    # Get the correct column based on the category and language
    category_col = category_language_mapping.get(category, {}).get(language, None)

    # Handle the case where the category does not exist in the selected language
    if category_col is None or category_col not in data.columns:
        filtered_df = pd.DataFrame(columns=['Feedback'])
    else:
        # Filter the data based on the selected category and language
        filtered_df = data[[category_col]].dropna()

        # If a keyword is entered, filter further by keyword
        if keyword:
            filtered_df = filtered_df[filtered_df[category_col].str.lower().str.contains(keyword.lower())]

        # Rename the column to 'Feedback'
        filtered_df.columns = ['Feedback']

    # Get overall stats
    total_comments = "63"  # Set manually as per the original code

    comments_by_category = {category: data[col].notna().sum() for col, category in flattened_mapping.items()}

    highest_category = max(comments_by_category, key=comments_by_category.get)
    lowest_category = min(comments_by_category, key=comments_by_category.get)

    # Bar chart of comments by category
    df = pd.DataFrame(list(comments_by_category.items()), columns=['Category', 'Count'])
    fig = px.bar(df, x='Category', y='Count', title='Number of Comments by Category')
    fig.update_layout(xaxis_tickangle=-45)

    # Identified patterns
    identified_patterns = """
        Patterns Identified Successfully

        Common patterns and keywords prominently listed in user comments:

        1. Errors:
            • Encountered during application operation
            • Issues viewing job postings
            • Application crashes
            • Malfunctioning filters
            • Problems sending emails

        2. Lack of Response:
            • No feedback received for job applications

        3. Filtering Issues:
            • Improper functioning in job searches and postings

        4. Location Inaccuracies:
            • Errors in location-based ranking
            • Irrelevant job postings from undesired cities
    """

    # Comments section if "Show Comments" button is clicked
    comments_section = None
    if n_clicks > 0 and not filtered_df.empty:
        # If filtered_df is not empty, display the comments
        comments_section = dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Filtered Feedback 🗣️"),
                    html.Ul([html.Li(comment) for comment in filtered_df['Feedback'].tolist()])
                ]
            ),
            className="mt-3",
            style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border": "1px solid #ddd"}
        )
    elif n_clicks > 0 and filtered_df.empty:
        # If no feedback is found, show a message
        comments_section = dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Filtered Feedback 🗣️"),
                    html.P("No comments match the selected filters.")
                ]
            ),
            className="mt-3",
            style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border": "1px solid #ddd"}
        )

    return total_comments, highest_category, lowest_category, fig, identified_patterns, comments_section


if __name__ == '__main__':
    app.run_server(debug=True)

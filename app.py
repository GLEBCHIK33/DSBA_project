from flask import Flask, render_template, send_file, request, redirect
import pandas as pd
import time
import pipreqs
import plotly_express as px


app = Flask(__name__)

links = {"Download results": "/download_results",
         "Download_stats": "/download_stats",
         "View Raw Data(results)": "/view_data(results)",
         "View Raw Data(stats)": "/view_data(stats)",
         "Descriptive statistics": "/descriptive_statistics",
         "Plots": "/plots",
         }


def statistics(data: pd.read_csv, column: str) -> list:
    median = data[column].median()
    mean = data[column].mean()
    dev = data[column].std()
    return [median, mean, dev]


def graph(data: pd.read_csv, stat1: str, stat2: str):
    ex_s = data.groupby(stat2, as_index=False)[stat1].sum()
    fig = px.line(ex_s, x=stat2, y=stat1)
    return fig.sh


def render_index(image=None, html_string=None, filters=None, errors=None, current_filter_value="", html_table=None,
                 html_li=None, alpha=None):
    return render_template("index1.html", links=links, image=image, code=time.time(), html_string=html_string,
                           filters=filters, errors=errors, current_filter_value=current_filter_value,
                           html_table=html_table, html_li=html_li, alpha=alpha)

@app.after_request
def add_header(r):
    """Do not clog the cache."""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods=['GET'])
def main_page():
    return render_index()


@app.route(links["Download results"], methods=['GET'])
def download_data1():
    """User can download results.csv"""
    return send_file("data/results.csv", as_attachment=True)


@app.route(links["Download_stats"], methods=['GET'])
def download_data2():
    """User can download stats.csv"""
    return send_file("data/stats.csv", as_attachment=True)


@app.route(links["View Raw Data(results)"], methods=['GET', 'POST'])
def view_data_results():
    """User can see the full results.csv"""
    df = pd.read_csv("data/results.csv")
    current_filter_value = ""
    html_string = df.to_html()
    return render_index(html_string=html_string, current_filter_value=current_filter_value)


@app.route(links["View Raw Data(stats)"], methods=['GET', 'POST'])
def view_data_stats():
    """User can see the full stats_csv"""
    df = pd.read_csv("data/stats.csv")
    current_filter_value = ""
    html_string = df.to_html()
    return render_index(html_string=html_string, current_filter_value=current_filter_value)


@app.route(links["Descriptive statistics"], methods=['GET', 'POST'])
def view_statics():
    """User can see statistics for each column of stats.csv"""
    df = pd.read_csv("data/stats.csv")
    values = 0
    current_filter_value = ""
    if request.method == "POST":
        current_filter = request.form.get('selectvalue')
        current_filter_value = current_filter
        values = statistics(df, current_filter)
    return render_index(html_table=values, html_li=list(pd.read_csv("data/stats.csv").columns),
                        current_filter_value=current_filter_value)


@app.route(links["Plots"], methods=['GET', 'POST'])
def plots_paint():
    """User can see any line-graph f(x)"""
    df = pd.read_csv("data/stats.csv")
    current_filter_value = ""
    gr = ""
    if request.method == "POST":
        current_filter1 = request.form.get("val_x")
        current_filter2 = request.form.get("val_y")
        current_filter_value = current_filter2
        gr = graph(df, current_filter2, current_filter1)
    return render_index(html_string=gr, html_li=list(pd.read_csv("data/stats.csv").columns),
                        current_filter_value=current_filter_value)


if __name__ == '__main__':
    app.run()

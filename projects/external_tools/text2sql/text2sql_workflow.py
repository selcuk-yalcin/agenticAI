"""Text2SQL Workflow scaffold

Run as:
    python text2sql_workflow.py "Show total sales per month for 2024"

This script provides a small, runnable demo using SQLite. It contains stubs for:
- question_to_sql(question, schema_hint) -> str
- run_sql_to_df(sql, db_uri) -> pandas.DataFrame
- df_to_chart(df, output_path) -> str

Dependencies: pandas, sqlalchemy, matplotlib
"""

from __future__ import annotations
import os
import sys
import sqlite3
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def question_to_sql(question: str, schema_hint: Optional[str] = None) -> str:
    """Convert a natural-language question into SQL.

    This is a simple heuristic stub. Replace with an LLM call or better parser.
    """
    q = question.lower()
    # naive examples
    if "sales" in q and "month" in q:
        return (
            "SELECT strftime('%Y-%m', created_at) AS month, SUM(amount) AS total"
            " FROM sales WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'"
            " GROUP BY month ORDER BY month;"
        )
    # fallback to user-provided schema hint
    if schema_hint:
        return f"-- Unable to auto-generate SQL. Schema hint: {schema_hint}\nSELECT ..."
    raise ValueError("Cannot convert question to SQL: ambiguous question")


def run_sql_to_df(sql: str, db_uri: str = "sqlite:///./demo.db", limit: int = 10000) -> pd.DataFrame:
    """Execute SQL and return a pandas DataFrame. db_uri supports sqlite for demo.

    db_uri examples:
      sqlite:///./demo.db
    """
    if db_uri.startswith("sqlite:///"):
        path = db_uri.replace("sqlite:///", "")
        conn = sqlite3.connect(path)
        try:
            df = pd.read_sql_query(sql + (f" LIMIT {limit}" if "limit" not in sql.lower() else ""), conn)
            return df
        finally:
            conn.close()
    else:
        # Minimal SQLAlchemy path (optional)
        from sqlalchemy import create_engine
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            df = pd.read_sql_query(sql + (f" LIMIT {limit}" if "limit" not in sql.lower() else ""), conn)
            return df


def df_to_chart(df: pd.DataFrame, output_path: str = "./outputs/chart.png") -> str:
    """Create a chart based on DataFrame contents and save it.

    Returns the output_path.
    """
    if df.empty:
        # create a text image explaining empty result
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.text(0.5, 0.5, "No results", ha="center", va="center", fontsize=14)
        ax.axis("off")
        fig.savefig(output_path, bbox_inches="tight")
        plt.close(fig)
        return output_path

    # simple heuristics
    df_cols = list(df.columns)
    # datetime detection
    date_col = None
    for c in df_cols:
        if "date" in c or "time" in c or "created" in c or "month" in c:
            date_col = c
            break

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if date_col and numeric_cols:
        # line chart
        df[date_col] = pd.to_datetime(df[date_col])
        plt.figure(figsize=(10, 5))
        for col in numeric_cols:
            sns.lineplot(x=date_col, y=col, data=df, label=col)
        plt.xlabel(date_col)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return output_path

    if len(numeric_cols) == 1 and len(df_cols) >= 2:
        # bar chart: group by first non-numeric column
        cat_cols = [c for c in df_cols if c not in numeric_cols]
        if cat_cols:
            x = cat_cols[0]
            y = numeric_cols[0]
            plt.figure(figsize=(10, 5))
            sns.barplot(x=x, y=y, data=df)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(output_path)
            plt.close()
            return output_path

    # fallback: save preview of dataframe as table image
    fig, ax = plt.subplots(figsize=(min(12, 0.6 * len(df.columns)), min(8, 0.25 * len(df))))
    ax.axis('off')
    tbl = ax.table(cellText=df.head(50).values, colLabels=df.columns, loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.5)
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def create_demo_db(path: str = "./demo.db") -> None:
    """Create a small demo sqlite DB with a `sales` table."""
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS sales;")
    c.execute(
        """
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            created_at TEXT,
            amount REAL,
            channel TEXT
        )
        """
    )
    # insert demo rows
    import random
    from datetime import datetime, timedelta
    base = datetime(2024, 1, 1)
    for i in range(200):
        d = (base + timedelta(days=i * 3)).strftime("%Y-%m-%d")
        amt = round(random.uniform(10, 500), 2)
        ch = random.choice(["organic", "ads", "referral"])
        c.execute("INSERT INTO sales (created_at, amount, channel) VALUES (?, ?, ?)", (d, amt, ch))
    conn.commit()
    conn.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python text2sql_workflow.py \"Your question\"")
        sys.exit(1)
    question = sys.argv[1]
    demo_db = "./demo.db"
    create_demo_db(demo_db)
    try:
        sql = question_to_sql(question)
    except Exception as e:
        print("Error generating SQL:", e)
        sys.exit(2)
    print("Generated SQL:\n", sql)
    df = run_sql_to_df(sql, db_uri=f"sqlite:///{demo_db}")
    print("Rows:", len(df))
    out = df_to_chart(df, output_path=str(OUTPUT_DIR / "chart.png"))
    print("Chart saved to", out)


if __name__ == "__main__":
    main()

Text-to-SQL Workflow

Overview

This document describes a 3-step pipeline for converting a natural-language question into a visual chart. The pipeline is designed to be simple, testable, and safe to run locally.

Steps

1) Question -> SQL
   - Input: A plain-English question (e.g., "Show monthly signups for 2024 by source").
   - Output: A single SQL string that answers the question.
   - Responsibility: A `question_to_sql(question: str) -> str` function must produce syntactically valid SQL for the target database schema.
   - Error modes: Ambiguous question, missing schema info, or unsupported constructs. The function should either return a SQL comment explaining the ambiguity or raise a clear exception.

2) SQL -> Data
   - Input: The SQL string produced in step 1.
   - Action: Execute the SQL against a configured database connection and return the result as a pandas DataFrame.
   - Function: `run_sql_to_df(sql: str, db_uri: str) -> pandas.DataFrame`.
   - Error modes: SQL syntax errors, missing tables, connection failures. The function should raise informative exceptions.

3) Data -> Chart
   - Input: The DataFrame returned in step 2.
   - Action: Inspect the DataFrame and choose an appropriate chart type:
     - Time series (datetime index or a column named `date`/`timestamp`): line chart
     - Single numeric column grouped by categorical column(s): bar chart
     - Multiple numeric columns across a time axis: stacked/line chart
     - Fallback: table display or scatter plot
   - Function: `df_to_chart(df: pandas.DataFrame, output_path: str) -> str` returns the image path.
   - Error modes: No numeric columns, too many rows (cap the plot), missing axis labels. The function should sanitize inputs and provide warnings.

Contract (inputs/outputs)

- `question_to_sql(question: str, schema_hint: Optional[str]=None) -> str`
  - Inputs: natural language question, optional schema hint describing table/column names.
  - Outputs: SQL string.

- `run_sql_to_df(sql: str, db_uri: str, limit: int=10000) -> pandas.DataFrame`
  - Inputs: SQL string, DB connection URI, optional limit to avoid huge result sets.
  - Outputs: pandas DataFrame.

- `df_to_chart(df: pandas.DataFrame, output_path: str='./outputs/chart.png') -> str`
  - Inputs: DataFrame, desired output image path.
  - Outputs: Path to saved chart image.

Edge cases

- Empty results: return an empty DataFrame and a short textual explanation image (or JSON with message).
- PII / secrets: Do not log query results. Keep logs minimal.
- Very wide tables: limit numeric columns to top N by variance for plotting.

Dependencies

- Python 3.10+
- pandas
- sqlalchemy
- matplotlib
- seaborn (optional)
- sqlite3 (for demo)

Quick run example (local demo)

1) Populate a local SQLite database (demo included in the scaffold script).
2) Run the script and pass a question:

   python text2sql_workflow.py "Show total sales per month for 2024"

The script will: generate SQL (stub), run it on the demo DB, and save a chart to `./outputs/chart.png`.

Security

- Never commit real API keys or production database URIs into the repo. Use environment variables or CI secrets.
- If you commit this scaffold, replace any test credentials before sharing.

Next steps

- Integrate a real text-to-SQL model (OpenAI / other LLM) in `question_to_sql`.
- Add unit tests for the mapping logic and chart selection heuristics.
- Extend charting choices and formatting options.

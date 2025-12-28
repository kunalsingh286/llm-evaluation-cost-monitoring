import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "llm_logs.db"


# ---------- Helper ----------
def get_data(query: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ---------- Page config ----------
st.set_page_config(
    page_title="LLM Evaluation & Cost Monitoring Dashboard",
    layout="wide"
)

st.title("📊 LLM Evaluation & Cost Monitoring Dashboard")


# ---------- Load data with EXPLICIT aliases ----------
calls_df = get_data("""
SELECT
    id AS call_id,
    timestamp,
    estimated_cost
FROM llm_calls
ORDER BY timestamp
""")

eval_df = get_data("""
SELECT
    llm_call_id,
    rule_score,
    judge_score
FROM evaluations
""")

reg_df = get_data("""
SELECT
    old_call_id,
    new_call_id,
    score_delta,
    verdict,
    timestamp
FROM regressions
""")


# ---------- Overview ----------
st.header("Overview")

col1, col2, col3 = st.columns(3)

total_calls = len(calls_df)
total_cost = calls_df["estimated_cost"].sum() if total_calls > 0 else 0
avg_judge_score = eval_df["judge_score"].mean() if len(eval_df) > 0 else 0

col1.metric("Total LLM Calls", total_calls)
col2.metric("Total Estimated Cost", round(total_cost, 4))
col3.metric("Average Judge Score", round(avg_judge_score, 2))


# ---------- Cost Analytics ----------
st.header("💸 Cost Analytics")

if total_calls > 0:
    cost_chart_df = (
        calls_df
        .set_index("timestamp")[["estimated_cost"]]
    )
    st.line_chart(cost_chart_df)
else:
    st.info("No LLM calls recorded yet.")


# ---------- Quality Analytics ----------
st.header("📈 Quality Analytics")

if len(eval_df) > 0 and total_calls > 0:
    quality_df = eval_df.merge(
        calls_df,
        left_on="llm_call_id",
        right_on="call_id",
        how="inner"
    )

    quality_chart_df = (
        quality_df
        .sort_values("timestamp")
        .set_index("timestamp")[["rule_score", "judge_score"]]
    )

    st.line_chart(quality_chart_df)
else:
    st.info("No evaluation data available yet.")


# ---------- Regression Analytics ----------
st.header("⚠️ Prompt Regression Tests")

if len(reg_df) > 0:
    st.dataframe(reg_df)
else:
    st.info("No regression tests run yet.")

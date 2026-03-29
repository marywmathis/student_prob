import streamlit as st
import pandas as pd
import numpy as np
import math
import random
from scipy import stats

st.set_page_config(page_title="EpiLab Student: Probability & Health", layout="wide")

PRIMARY  = "#1B3A6B"
SECONDARY= "#E05A2B"
ACCENT   = "#F5A623"
GREEN    = "#2e7d32"
LIGHT_BG = "#F0F4FF"

# ── LOGIN ──────────────────────────────────────────────────
def check_credentials(u, p):
    users = st.secrets.get("users", {})
    return u in users and users[u] == p

def login_screen():
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""<div style='text-align:center;padding:32px;background:{LIGHT_BG};
        border-radius:12px;border-top:4px solid {PRIMARY};'>
        <h2 style='color:{PRIMARY};margin-bottom:4px;'>EpiLab Student</h2>
        <h3 style='color:{SECONDARY};margin-top:0;'>Probability & Health</h3>
        <p style='color:#555;'>Enter your access credentials to continue.</p></div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        u = st.text_input("Username", key="lu")
        p = st.text_input("Password", type="password", key="lp")
        if st.button("Log In", type="primary", use_container_width=True):
            if check_credentials(u, p):
                st.session_state["auth"] = True; st.rerun()
            else:
                st.error("Incorrect username or password.")
        st.caption("Access provided by your course instructor.")

if not st.session_state.get("auth"):
    login_screen(); st.stop()

# ── HEADER ─────────────────────────────────────────────────
c1, c2 = st.columns([6,1])
with c1:
    st.markdown(f"""<div style='padding:16px 0 8px 0;'>
    <span style='font-size:28px;font-weight:800;color:{PRIMARY};'>EpiLab Student</span>
    <span style='font-size:18px;color:{SECONDARY};margin-left:12px;'>Probability & Health</span></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Log Out"): st.session_state["auth"] = False; st.rerun()

st.markdown(f"<div style='height:3px;background:linear-gradient(to right,{PRIMARY},{SECONDARY},{ACCENT});border-radius:2px;margin-bottom:16px;'></div>", unsafe_allow_html=True)

tab_learn, tab_practice, tab_glossary = st.tabs([
    "📊 Learn: Probability & Health",
    "🎯 Practice Scenarios",
    "📖 Glossary"
])

# ══════════════════════════════════════════════════════════
# HELPER: CI bar
# ══════════════════════════════════════════════════════════
def prob_bar(label, value, color=None):
    if color is None:
        color = GREEN if value >= 0.7 else SECONDARY if value >= 0.4 else "#c0392b"
    pct = round(value * 100, 1)
    st.markdown(f"""
<div style='margin:6px 0;'>
  <div style='display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px;'>
    <span style='color:{PRIMARY};font-weight:bold;'>{label}</span>
    <span style='color:{color};font-weight:bold;'>{pct}%</span>
  </div>
  <div style='background:#e0e0e0;border-radius:6px;height:18px;overflow:hidden;'>
    <div style='width:{pct}%;height:100%;background:{color};border-radius:6px;'></div>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 1: LEARN
# ══════════════════════════════════════════════════════════
with tab_learn:

    if "lr" not in st.session_state: st.session_state["lr"] = 0
    ch, cr = st.columns([5,1])
    with ch:
        st.markdown(f"### <span style='color:{PRIMARY}'>Probability in Health & Clinical Practice</span>", unsafe_allow_html=True)
    with cr:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset", key="rst_learn"):
            st.session_state["lr"] += 1
            for k in [k for k in st.session_state if k.startswith("l_")]: del st.session_state[k]
            st.rerun()
    lrc = st.session_state["lr"]

    st.markdown("""
Probability is the language of uncertainty in medicine and public health. Every clinical decision,
screening test, and risk estimate rests on probabilistic reasoning. This module builds the core
concepts from the ground up — from basic rules to Bayes' theorem to communicating risk.
    """)

    # ── SECTION 1: BASIC RULES ─────────────────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>1. Basic Probability Rules</span>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
<div style='background:{LIGHT_BG};border-radius:10px;padding:16px;border-top:4px solid {PRIMARY};margin-bottom:12px;'>
<b style='color:{PRIMARY}'>Probability basics:</b><br><br>
• Probability ranges from <b>0</b> (impossible) to <b>1</b> (certain)<br>
• P(A) = number of favorable outcomes / total outcomes<br>
• P(not A) = 1 − P(A) &nbsp;<i>(complement rule)</i><br>
• All probabilities in a sample space sum to 1
</div>""", unsafe_allow_html=True)
        st.markdown(f"""
<div style='background:#FFF5F0;border-radius:10px;padding:16px;border-top:4px solid {SECONDARY};'>
<b style='color:{SECONDARY}'>Addition rule:</b><br><br>
P(A or B) = P(A) + P(B) − P(A and B)<br><br>
If A and B are <b>mutually exclusive</b> (can't both happen):<br>
P(A or B) = P(A) + P(B)
</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
<div style='background:#F0FFF4;border-radius:10px;padding:16px;border-top:4px solid {GREEN};margin-bottom:12px;'>
<b style='color:{GREEN}'>Multiplication rule:</b><br><br>
P(A and B) = P(A) × P(B|A)<br><br>
If A and B are <b>independent</b> (one doesn't affect the other):<br>
P(A and B) = P(A) × P(B)
</div>""", unsafe_allow_html=True)
        st.markdown(f"""
<div style='background:#FFFBF0;border-radius:10px;padding:16px;border-top:4px solid {ACCENT};'>
<b style='color:{ACCENT}'>Health example:</b><br><br>
P(diabetes) = 0.11 in US adults<br>
P(no diabetes) = 1 − 0.11 = <b>0.89</b><br><br>
P(hypertension) = 0.47<br>
If independent: P(both) = 0.11 × 0.47 = <b>0.052</b><br>
<i>(In reality they are not independent — both share risk factors)</i>
</div>""", unsafe_allow_html=True)

    st.markdown("#### Interactive Probability Calculator")
    col1, col2 = st.columns(2)
    with col1:
        pA = st.slider("P(A)", 0.0, 1.0, 0.3, 0.01, key=f"l_pA_{lrc}")
        pB = st.slider("P(B)", 0.0, 1.0, 0.2, 0.01, key=f"l_pB_{lrc}")
        independent = st.checkbox("A and B are independent", value=True, key=f"l_ind_{lrc}")
    with col2:
        if independent:
            pAandB = round(pA * pB, 4)
        else:
            pAandB = st.slider("P(A and B) — enter manually if not independent", 0.0, min(pA,pB), min(round(pA*pB,2),min(pA,pB)), 0.01, key=f"l_pAB_{lrc}")
        pAorB = round(pA + pB - pAandB, 4)
        pnotA = round(1 - pA, 4)
        st.markdown(f"""
| Expression | Value |
|---|---|
| P(A) | {pA} |
| P(B) | {pB} |
| P(not A) | {pnotA} |
| P(A and B) | {pAandB} |
| P(A or B) | {min(1.0, pAorB)} |
        """)
        if pAorB > 1:
            st.warning("P(A or B) > 1 — check your P(A and B) value.")

    # ── SECTION 2: CONDITIONAL PROBABILITY ────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>2. Conditional Probability & Independence</span>", unsafe_allow_html=True)

    st.markdown("""
**Conditional probability** P(B|A) — pronounced "probability of B given A" — is the probability of B
occurring **knowing that A has already occurred**. This is fundamental in clinical practice: given
that a patient has a positive test result, what is the probability they actually have the disease?

**P(B|A) = P(A and B) / P(A)**

Two events are **independent** if knowing one tells you nothing about the other: P(B|A) = P(B).
In health research, independence is rarely the default assumption — exposure and disease are almost
always correlated with shared risk factors.
    """)

    st.markdown("#### Interactive Conditional Probability")
    st.markdown("Use a 2×2 table to explore conditional probabilities:")

    col1, col2 = st.columns(2)
    with col1:
        cp_a  = st.number_input("Disease+ AND Exposed",   min_value=1, value=80,  key=f"l_cp_a_{lrc}")
        cp_b  = st.number_input("Disease− AND Exposed",   min_value=1, value=120, key=f"l_cp_b_{lrc}")
        cp_c  = st.number_input("Disease+ AND Unexposed", min_value=1, value=40,  key=f"l_cp_c_{lrc}")
        cp_d  = st.number_input("Disease− AND Unexposed", min_value=1, value=260, key=f"l_cp_d_{lrc}")
    with col2:
        N_cp  = cp_a+cp_b+cp_c+cp_d
        pDis  = round((cp_a+cp_c)/N_cp, 4)
        pExp  = round((cp_a+cp_b)/N_cp, 4)
        pDisGivenExp   = round(cp_a/(cp_a+cp_b), 4)
        pDisGivenUnexp = round(cp_c/(cp_c+cp_d), 4)
        pExpGivenDis   = round(cp_a/(cp_a+cp_c), 4)
        st.markdown(f"""
| Probability | Value | Meaning |
|---|---|---|
| P(Disease) | {pDis} | Unconditional disease probability |
| P(Exposed) | {pExp} | Unconditional exposure probability |
| P(Disease|Exposed) | {pDisGivenExp} | Risk in exposed group |
| P(Disease|Unexposed) | {pDisGivenUnexp} | Risk in unexposed group |
| P(Exposed|Disease) | {pExpGivenDis} | Exposure among cases |
| RR | {round(pDisGivenExp/pDisGivenUnexp, 2)} | Risk ratio |
        """)
        if abs(pDisGivenExp - pDisGivenUnexp) < 0.02:
            st.success("P(Disease|Exposed) ≈ P(Disease|Unexposed) — exposure and disease are approximately independent.")
        else:
            st.info(f"P(Disease|Exposed) ≠ P(Disease|Unexposed) — knowing exposure status changes disease probability. Not independent.")

    # ── SECTION 3: BAYES' THEOREM ─────────────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>3. Bayes' Theorem</span>", unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown("""
**Bayes' theorem** tells us how to update a probability estimate when we receive new information.
In clinical practice, this is exactly what happens when a test result comes in:

**P(Disease|Test+) = P(Test+|Disease) × P(Disease) / P(Test+)**

Where:
- **P(Disease)** = prior probability (pre-test probability / prevalence)
- **P(Test+|Disease)** = sensitivity (true positive rate)
- **P(Test+)** = total probability of a positive test (from diseased AND non-diseased)
- **P(Disease|Test+)** = posterior probability (positive predictive value)

Bayes' theorem formalizes the intuition that a positive test means more when the disease is common
and when the test rarely gives false positives.
        """)
    with col2:
        st.markdown(f"""
<div style='background:{LIGHT_BG};border-radius:10px;padding:16px;border-top:4px solid {PRIMARY};'>
<b style='color:{PRIMARY}'>Plain language version:</b><br><br>
Prior belief + new evidence = updated belief<br><br>
<b>Before the test:</b> How likely is this patient to have the disease? (prevalence, risk factors)<br><br>
<b>The test result:</b> How good is the test at detecting disease? How often does it give false positives?<br><br>
<b>After the test:</b> Given the result, what is the probability the patient actually has it?
</div>""", unsafe_allow_html=True)

    st.markdown("#### Bayes' Theorem Calculator")
    col1, col2 = st.columns(2)
    with col1:
        b_prev = st.slider("Pre-test probability / Prevalence (%)", 0.1, 99.0, 5.0, 0.1, key=f"l_bprev_{lrc}") / 100
        b_sens = st.slider("Sensitivity (%) — P(Test+|Disease+)", 50, 100, 90, 1, key=f"l_bsens_{lrc}") / 100
        b_spec = st.slider("Specificity (%) — P(Test−|Disease−)", 50, 100, 95, 1, key=f"l_bspec_{lrc}") / 100
    with col2:
        fpr = 1 - b_spec
        tp = b_prev * b_sens
        fp = (1 - b_prev) * fpr
        fn = b_prev * (1 - b_sens)
        tn = (1 - b_prev) * b_spec
        ppv = round(tp / (tp + fp), 4) if (tp+fp) > 0 else 0
        npv = round(tn / (tn + fn), 4) if (tn+fn) > 0 else 0

        st.markdown("**Per 1,000 people tested:**")
        n = 1000
        tp_n = round(b_prev * b_sens * n)
        fp_n = round((1-b_prev) * fpr * n)
        fn_n = round(b_prev * (1-b_sens) * n)
        tn_n = round((1-b_prev) * b_spec * n)

        st.markdown(f"""
| | Test + | Test − | Total |
|---|---|---|---|
| **Disease +** | {tp_n} (TP) | {fn_n} (FN) | {round(b_prev*n)} |
| **Disease −** | {fp_n} (FP) | {tn_n} (TN) | {round((1-b_prev)*n)} |
| **Total** | {tp_n+fp_n} | {fn_n+tn_n} | {n} |
        """)

    prob_bar("Positive Predictive Value (PPV)", ppv, GREEN if ppv >= 0.7 else SECONDARY)
    prob_bar("Negative Predictive Value (NPV)", npv, GREEN if npv >= 0.9 else SECONDARY)

    with st.expander("📐 Show me the math — Bayes' Theorem"):
        st.markdown(f"""
**P(Disease|Test+) = P(Test+|Disease) × P(Disease) / P(Test+)**

**Step 1:** P(Test+|Disease) × P(Disease) = sensitivity × prevalence = {b_sens} × {round(b_prev,4)} = **{round(tp,6)}**

**Step 2:** P(Test+|No Disease) × P(No Disease) = FPR × (1−prevalence) = {round(fpr,3)} × {round(1-b_prev,4)} = **{round(fp,6)}**

**Step 3:** P(Test+) = {round(tp,6)} + {round(fp,6)} = **{round(tp+fp,6)}**

**Step 4:** PPV = {round(tp,6)} / {round(tp+fp,6)} = **{ppv}** ({round(ppv*100,1)}%)

**Why does prevalence matter so much?**
When disease is rare (low prevalence), even a specific test produces many false positives relative
to true positives. A positive result in a low-prevalence population is less likely to be a true positive.
Try setting prevalence to 0.1% and observe how PPV collapses even with 95% sensitivity and 99% specificity.
        """)

    with st.expander("💡 The base rate fallacy"):
        st.markdown(f"""
A common error in clinical reasoning: ignoring prevalence when interpreting test results.

**Example:** A test for a rare disease (prevalence 1 in 10,000) has 99% sensitivity and 99% specificity.
A patient tests positive. What is the probability they have the disease?

Most people guess ~99%. The actual answer:

PPV = (0.99 × 0.0001) / (0.99 × 0.0001 + 0.01 × 0.9999)
= 0.0000990 / (0.0000990 + 0.009999)
= **0.98% — less than 1%**

The disease is so rare that even with a highly accurate test, most positive results are false positives.
This is why population-level screening for rare diseases must be carefully justified.
        """)

    # ── SECTION 4: SENS / SPEC / PPV / NPV ───────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>4. Sensitivity, Specificity, PPV & NPV</span>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
<div style='background:{LIGHT_BG};border-radius:10px;padding:16px;border-top:4px solid {PRIMARY};margin-bottom:12px;'>
<b style='color:{PRIMARY}'>Sensitivity (True Positive Rate)</b><br><br>
P(Test+|Disease+) = TP / (TP + FN)<br><br>
Of all people who <b>have</b> the disease, what fraction test positive?<br><br>
High sensitivity → few false negatives → good for <b>ruling OUT</b> disease (SnNout).<br>
A sensitive test that comes back negative makes disease unlikely.
</div>""", unsafe_allow_html=True)
        st.markdown(f"""
<div style='background:#F0FFF4;border-radius:10px;padding:16px;border-top:4px solid {GREEN};'>
<b style='color:{GREEN}'>PPV (Positive Predictive Value)</b><br><br>
P(Disease+|Test+) = TP / (TP + FP)<br><br>
Of all people who <b>test positive</b>, what fraction actually have the disease?<br><br>
Depends heavily on <b>prevalence</b>. Same test → different PPV in different populations.
</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
<div style='background:#FFF5F0;border-radius:10px;padding:16px;border-top:4px solid {SECONDARY};margin-bottom:12px;'>
<b style='color:{SECONDARY}'>Specificity (True Negative Rate)</b><br><br>
P(Test−|Disease−) = TN / (TN + FP)<br><br>
Of all people who do <b>not</b> have the disease, what fraction test negative?<br><br>
High specificity → few false positives → good for <b>ruling IN</b> disease (SpPin).<br>
A specific test that comes back positive strongly suggests disease.
</div>""", unsafe_allow_html=True)
        st.markdown(f"""
<div style='background:#FFFBF0;border-radius:10px;padding:16px;border-top:4px solid {ACCENT};'>
<b style='color:{ACCENT}'>NPV (Negative Predictive Value)</b><br><br>
P(Disease−|Test−) = TN / (TN + FN)<br><br>
Of all people who <b>test negative</b>, what fraction are truly disease-free?<br><br>
Also depends on prevalence. High prevalence → lower NPV (more missed cases).
</div>""", unsafe_allow_html=True)

    st.markdown("#### Screening Test Calculator")
    col1, col2, col3 = st.columns(3)
    with col1:
        sc_sens = st.slider("Sensitivity (%)", 50, 100, 85, 1, key=f"l_scsens_{lrc}") / 100
        sc_spec = st.slider("Specificity (%)", 50, 100, 92, 1, key=f"l_scspec_{lrc}") / 100
    with col2:
        sc_prev = st.slider("Prevalence (%)", 0.1, 50.0, 2.0, 0.1, key=f"l_scprev_{lrc}") / 100
        sc_n = st.number_input("Population size", 1000, 1000000, 10000, 1000, key=f"l_scn_{lrc}")
    with col3:
        sc_tp = round(sc_prev * sc_sens * sc_n)
        sc_fp = round((1-sc_prev) * (1-sc_spec) * sc_n)
        sc_fn = round(sc_prev * (1-sc_sens) * sc_n)
        sc_tn = round((1-sc_prev) * sc_spec * sc_n)
        sc_ppv = round(sc_tp/(sc_tp+sc_fp),4) if (sc_tp+sc_fp)>0 else 0
        sc_npv = round(sc_tn/(sc_tn+sc_fn),4) if (sc_tn+sc_fn)>0 else 0
        prob_bar("Sensitivity", sc_sens, PRIMARY)
        prob_bar("Specificity", sc_spec, PRIMARY)
        prob_bar("PPV", sc_ppv, GREEN if sc_ppv>=0.7 else SECONDARY)
        prob_bar("NPV", sc_npv, GREEN if sc_npv>=0.9 else SECONDARY)

    st.markdown(f"""
| | Test + | Test − | Total |
|---|---|---|---|
| **Disease +** | {sc_tp:,} TP | {sc_fn:,} FN | {round(sc_prev*sc_n):,} |
| **Disease −** | {sc_fp:,} FP | {sc_tn:,} TN | {round((1-sc_prev)*sc_n):,} |
| **Total** | {sc_tp+sc_fp:,} | {sc_fn+sc_tn:,} | {sc_n:,} |
    """)
    st.info(f"Out of {sc_tp+sc_fp:,} positive tests, only **{sc_tp:,}** ({round(sc_ppv*100,1)}%) are true positives. {sc_fp:,} are false positives.")

    # ── SECTION 5: PRE/POST-TEST PROBABILITY ──────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>5. Pre-test & Post-test Probability</span>", unsafe_allow_html=True)

    st.markdown("""
**Pre-test probability** is your best estimate of disease probability BEFORE a test is performed —
based on prevalence, symptoms, risk factors, and clinical judgment.

**Post-test probability** is the updated probability AFTER the test result — calculated using Bayes'
theorem. The **Likelihood Ratio (LR)** is the most efficient way to update:

- **LR+ = Sensitivity / (1 − Specificity)** — how much a positive result raises the odds
- **LR− = (1 − Sensitivity) / Specificity** — how much a negative result lowers the odds
- **Post-test odds = Pre-test odds × LR**
- **Post-test probability = Post-test odds / (Post-test odds + 1)**
    """)

    col1, col2 = st.columns(2)
    with col1:
        pt_prev = st.slider("Pre-test probability (%)", 1, 99, 15, 1, key=f"l_ptprev_{lrc}") / 100
        pt_sens = st.slider("Test Sensitivity (%)", 50, 100, 88, 1, key=f"l_ptsens_{lrc}") / 100
        pt_spec = st.slider("Test Specificity (%)", 50, 100, 94, 1, key=f"l_ptspec_{lrc}") / 100
    with col2:
        lr_pos = round(pt_sens / (1-pt_spec), 2)
        lr_neg = round((1-pt_sens) / pt_spec, 3)
        pre_odds = pt_prev / (1-pt_prev)
        post_odds_pos = pre_odds * lr_pos
        post_odds_neg = pre_odds * lr_neg
        post_prob_pos = round(post_odds_pos / (post_odds_pos+1), 4)
        post_prob_neg = round(post_odds_neg / (post_odds_neg+1), 4)

        st.metric("LR+ (positive test)", lr_pos)
        st.metric("LR− (negative test)", lr_neg)
        col_a, col_b = st.columns(2)
        col_a.metric("Post-test prob (Test+)", f"{round(post_prob_pos*100,1)}%", delta=f"+{round((post_prob_pos-pt_prev)*100,1)}%")
        col_b.metric("Post-test prob (Test−)", f"{round(post_prob_neg*100,1)}%", delta=f"{round((post_prob_neg-pt_prev)*100,1)}%", delta_color="inverse")

        if lr_pos >= 10: st.success(f"LR+ = {lr_pos} — very strong evidence of disease when positive.")
        elif lr_pos >= 5: st.success(f"LR+ = {lr_pos} — moderately strong evidence of disease when positive.")
        elif lr_pos >= 2: st.info(f"LR+ = {lr_pos} — weak evidence of disease when positive.")
        else: st.warning(f"LR+ = {lr_pos} — positive result barely changes probability.")

    # ── SECTION 6: RISK COMMUNICATION ─────────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>6. Risk Communication</span>", unsafe_allow_html=True)

    st.markdown("""
How you express risk dramatically affects how patients and the public understand and act on information.
The same number can sound alarming or reassuring depending on framing.
    """)

    col1, col2 = st.columns(2)
    with col1:
        rc_r_exp  = st.slider("Risk in exposed group (%)", 0.1, 50.0, 4.0, 0.1, key=f"l_rcexp_{lrc}") / 100
        rc_r_unexp= st.slider("Risk in unexposed group (%)", 0.1, 50.0, 2.0, 0.1, key=f"l_rcunexp_{lrc}") / 100
        rc_pe     = st.slider("Exposure prevalence in population (%)", 1, 99, 30, 1, key=f"l_rcpe_{lrc}") / 100
    with col2:
        if rc_r_exp > 0 and rc_r_unexp > 0:
            rr_rc  = round(rc_r_exp/rc_r_unexp, 2)
            ar_rc  = round((rc_r_exp - rc_r_unexp)*100, 2)
            ar_pct = round((rc_r_exp-rc_r_unexp)/rc_r_exp*100, 1)
            par    = round((rc_pe*(rc_r_exp-rc_r_unexp))/((rc_pe*rc_r_exp+(1-rc_pe)*rc_r_unexp))*100, 1)
            nnt    = round(1/(rc_r_exp-rc_r_unexp)) if rc_r_exp > rc_r_unexp else None

            st.markdown(f"""
| Measure | Value | What it says |
|---|---|---|
| Relative Risk (RR) | **{rr_rc}×** | Exposed have {rr_rc}× the risk |
| Absolute Risk Difference | **{ar_rc}%** | {ar_rc} extra cases per 100 exposed |
| Attributable Risk % (AR%) | **{ar_pct}%** | {ar_pct}% of exposed cases are due to exposure |
| PAR% | **{par}%** | {par}% of all population cases are due to exposure |
| NNH (if harmful) | **{nnt if nnt else 'N/A'}** | {f'{nnt} people exposed for 1 additional case' if nnt else 'Exposure is protective'} |
            """)

    with st.expander("💡 Framing effects in risk communication"):
        if rc_r_exp > rc_r_unexp:
            rr_rc2 = round(rc_r_exp/rc_r_unexp,2)
            ar_rc2 = round((rc_r_exp-rc_r_unexp)*100,2)
            rr_red = round((1-1/rr_rc2)*100,1) if rr_rc2>0 else 0
            st.markdown(f"""
**The same data, four ways to say it:**

1. **Relative risk framing:** "Exposed people have {rr_rc2}× the risk" — sounds alarming
2. **Relative risk reduction framing:** "Removing the exposure reduces risk by {rr_red}%" — sounds impressive
3. **Absolute risk framing:** "Risk increases by {ar_rc2} percentage points" — sounds modest
4. **NNH framing:** "{nnt if nnt else '?'} people need to be exposed for one additional case" — most intuitive for clinical decisions

**Best practice:** Always report BOTH relative and absolute measures. Relative risk alone can be
misleading — a 100% increase in risk sounds alarming but means going from 0.01% to 0.02%.
            """)

    # ── SECTION 7: PROBABILITY DISTRIBUTIONS ──────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>7. Probability Distributions</span>", unsafe_allow_html=True)

    dist_tab1, dist_tab2 = st.tabs(["Normal Distribution", "Binomial Distribution"])

    with dist_tab1:
        st.markdown("""
The **normal distribution** (bell curve) describes many continuous health measurements: blood pressure,
BMI, lab values. It is defined by its mean (μ) and standard deviation (σ).

**68-95-99.7 rule:** 68% of values fall within ±1σ, 95% within ±2σ, 99.7% within ±3σ.
        """)
        col1, col2 = st.columns(2)
        with col1:
            n_mean = st.number_input("Mean (μ)", value=120.0, key=f"l_nmean_{lrc}")
            n_sd   = st.number_input("Standard deviation (σ)", min_value=0.1, value=15.0, key=f"l_nsd_{lrc}")
            n_x    = st.number_input("Value of interest (x)", value=140.0, key=f"l_nx_{lrc}")
        with col2:
            z = round((n_x - n_mean)/n_sd, 2)
            p_below = round(stats.norm.cdf(z), 4)
            p_above = round(1 - p_below, 4)
            st.metric("Z-score", z)
            st.metric(f"P(X ≤ {n_x})", f"{round(p_below*100,1)}%")
            st.metric(f"P(X > {n_x})", f"{round(p_above*100,1)}%")
            st.markdown(f"""
**Interpretation:** A value of {n_x} is **{abs(z)} standard deviations {'above' if z>0 else 'below'} the mean**.
{round(p_below*100,1)}% of values in this distribution fall at or below {n_x}.
            """)

        with st.expander("📐 Show me the math — Normal Distribution"):
            st.markdown(f"""
**Z-score:** z = (x − μ) / σ = ({n_x} − {n_mean}) / {n_sd} = **{z}**

The z-score tells you how many standard deviations a value is from the mean.
A z-score of {z} corresponds to a percentile of {round(p_below*100,1)}%.

**68-95-99.7 rule for μ = {n_mean}, σ = {n_sd}:**
- 68% of values: {round(n_mean-n_sd,1)} to {round(n_mean+n_sd,1)}
- 95% of values: {round(n_mean-2*n_sd,1)} to {round(n_mean+2*n_sd,1)}
- 99.7% of values: {round(n_mean-3*n_sd,1)} to {round(n_mean+3*n_sd,1)}
            """)

    with dist_tab2:
        st.markdown("""
The **binomial distribution** models the number of successes in n independent trials,
each with probability p of success. Used for: number of patients who respond to treatment,
number of positive tests in a sample, number of disease cases in a fixed-size group.
        """)
        col1, col2 = st.columns(2)
        with col1:
            b_n   = st.number_input("Number of trials (n)", min_value=1, max_value=500, value=20, key=f"l_bn_{lrc}")
            b_p   = st.slider("Probability of success per trial (p)", 0.01, 0.99, 0.30, 0.01, key=f"l_bp_{lrc}")
            b_k   = st.number_input("Number of successes of interest (k)", min_value=0, max_value=int(b_n), value=5, key=f"l_bk_{lrc}")
        with col2:
            b_mean = round(b_n * b_p, 2)
            b_var  = round(b_n * b_p * (1-b_p), 2)
            b_sd   = round(math.sqrt(b_var), 2)
            p_exact= round(stats.binom.pmf(b_k, b_n, b_p), 4)
            p_le_k = round(stats.binom.cdf(b_k, b_n, b_p), 4)
            p_ge_k = round(1 - stats.binom.cdf(b_k-1, b_n, b_p), 4)
            st.metric("Expected value (mean)", f"{b_mean}")
            st.metric("Standard deviation", f"{b_sd}")
            st.metric(f"P(X = {b_k})", f"{round(p_exact*100,2)}%")
            st.metric(f"P(X ≤ {b_k})", f"{round(p_le_k*100,2)}%")
            st.metric(f"P(X ≥ {b_k})", f"{round(p_ge_k*100,2)}%")

        with st.expander("📐 Show me the math — Binomial"):
            comb = math.comb(int(b_n), int(b_k))
            st.markdown(f"""
**Formula:** P(X = k) = C(n,k) × p^k × (1−p)^(n−k)

**C(n,k)** = n! / (k! × (n−k)!) = C({b_n},{b_k}) = **{comb:,}**

**p^k** = {b_p}^{b_k} = **{round(b_p**b_k, 6)}**

**(1−p)^(n−k)** = {round(1-b_p,2)}^{int(b_n)-int(b_k)} = **{round((1-b_p)**(b_n-b_k), 6)}**

**P(X = {b_k})** = {comb:,} × {round(b_p**b_k,6)} × {round((1-b_p)**(b_n-b_k),6)} = **{round(p_exact,4)}** ({round(p_exact*100,2)}%)

**Mean:** μ = n × p = {b_n} × {b_p} = **{b_mean}**
**Variance:** σ² = n × p × (1−p) = {b_n} × {b_p} × {round(1-b_p,2)} = **{b_var}**
**SD:** σ = **{b_sd}**
            """)

    # ── SECTION 8: EXPECTED VALUE & DECISION TREES ────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>8. Expected Value & Decision Trees</span>", unsafe_allow_html=True)

    st.markdown("""
**Expected value** is the weighted average of all possible outcomes, where weights are probabilities.
In clinical decision-making, we compare expected values (often in quality-adjusted life years, costs,
or outcomes) across treatment options to identify the best choice under uncertainty.

**E(X) = Σ [outcome × P(outcome)]**

**Decision trees** visualize multi-stage decisions: each branch is a choice or chance event,
and we work backward from outcomes to choose the branch with the highest expected value.
    """)

    st.markdown("#### Clinical Decision Tree: Treat vs. Test First")
    st.info("Scenario: A patient has a 30% pre-test probability of a bacterial infection. Should you treat empirically with antibiotics, or test first?")

    col1, col2 = st.columns(2)
    with col1:
        ev_prev   = st.slider("Pre-test probability of infection (%)", 5, 95, 30, 5, key=f"l_evprev_{lrc}") / 100
        ev_cure   = st.slider("P(cure | correct treatment)", 50, 99, 85, 1, key=f"l_evcure_{lrc}") / 100
        ev_harm   = st.slider("P(antibiotic side effect)", 1, 30, 10, 1, key=f"l_evharm_{lrc}") / 100
        ev_se_val = st.slider("Utility loss from side effect (0=worst, 1=no loss)", 0.0, 0.5, 0.1, 0.05, key=f"l_evse_{lrc}")
        ev_miss   = st.slider("Utility loss from missed/delayed treatment", 0.0, 1.0, 0.4, 0.05, key=f"l_evmiss_{lrc}")
    with col2:
        # Treat empirically
        ev_treat_inf   = ev_cure * 1.0 + (1-ev_cure) * (1-ev_miss)  # infected, treated
        ev_treat_no_inf= (1-ev_harm)*1.0 + ev_harm*(1-ev_se_val)     # not infected, treated unnecessarily
        ev_treat = round(ev_prev*ev_treat_inf + (1-ev_prev)*ev_treat_no_inf, 3)

        # Test first (assume test sens=90%, spec=95%, then treat based on result)
        sens_t, spec_t = 0.90, 0.95
        tp_t = ev_prev*sens_t; fp_t=(1-ev_prev)*(1-spec_t)
        fn_t = ev_prev*(1-sens_t); tn_t=(1-ev_prev)*spec_t
        # Test+: treat → same as treat empirically but conditional on test+
        ppv_t = tp_t/(tp_t+fp_t) if (tp_t+fp_t)>0 else 0
        npv_t = tn_t/(tn_t+fn_t) if (tn_t+fn_t)>0 else 0
        ev_testpos = ppv_t*ev_treat_inf + (1-ppv_t)*ev_treat_no_inf
        ev_testneg = (1-npv_t)*(1-ev_miss) + npv_t*1.0   # FN → untreated; TN → no treatment
        p_testpos = tp_t + fp_t
        ev_test = round(p_testpos*ev_testpos + (1-p_testpos)*ev_testneg, 3)

        st.markdown("**Expected Utility Comparison:**")
        col_a, col_b = st.columns(2)
        col_a.metric("Treat empirically", ev_treat, help="Expected utility if you treat all patients without testing")
        col_b.metric("Test first, then treat", ev_test, help="Expected utility if you test first and treat only positives")
        recommendation = "Treat empirically" if ev_treat >= ev_test else "Test first"
        diff = round(abs(ev_treat - ev_test), 3)
        if diff < 0.02:
            st.info(f"The strategies are nearly equivalent (difference = {diff}). Clinical judgment and cost should guide the decision.")
        elif ev_treat >= ev_test:
            st.success(f"✅ **Treat empirically** has higher expected utility ({ev_treat} vs {ev_test}). Treat without waiting for test results.")
        else:
            st.success(f"✅ **Test first** has higher expected utility ({ev_test} vs {ev_treat}). Testing reduces unnecessary antibiotic use.")

    with st.expander("📐 Show me the math — Expected Value"):
        st.markdown(f"""
**Treat empirically:**
- If infected ({round(ev_prev*100)}% chance): E = P(cure)×1 + P(no cure)×(1−miss_loss) = {ev_cure}×1 + {round(1-ev_cure,2)}×{round(1-ev_miss,2)} = {round(ev_treat_inf,3)}
- If not infected ({round((1-ev_prev)*100)}% chance): E = P(no SE)×1 + P(SE)×(1−SE_loss) = {round(1-ev_harm,2)}×1 + {ev_harm}×{round(1-ev_se_val,2)} = {round(ev_treat_no_inf,3)}
- **Total E(Treat) = {ev_prev}×{round(ev_treat_inf,3)} + {round(1-ev_prev,2)}×{round(ev_treat_no_inf,3)} = {ev_treat}**

**Test first (sens=90%, spec=95%):**
- PPV = {round(ppv_t,3)}, NPV = {round(npv_t,3)}
- P(Test+) = {round(p_testpos,3)}
- E(Test+, then treat) = {round(ev_testpos,3)}
- E(Test−, no treat) = {round(ev_testneg,3)}
- **Total E(Test) = {round(p_testpos,3)}×{round(ev_testpos,3)} + {round(1-p_testpos,3)}×{round(ev_testneg,3)} = {ev_test}**
        """)

# ══════════════════════════════════════════════════════════
# TAB 2: PRACTICE
# ══════════════════════════════════════════════════════════
with tab_practice:
    st.markdown(f"### <span style='color:{PRIMARY}'>Practice Scenarios</span>", unsafe_allow_html=True)
    st.markdown("Work through each scenario one question at a time.")

    SCENARIOS = [
        {
            "id":"pr1","title":"Scenario 1: HIV Screening in a Low-Prevalence Population",
            "description":"A community health clinic screens asymptomatic adults for HIV. HIV prevalence in this population is 0.5%. The test used has 99.5% sensitivity and 99.8% specificity. A patient tests positive.",
            "questions":[
                {"q":"With 99.5% sensitivity and 99.8% specificity in a population where HIV prevalence is 0.5%, what is the approximate PPV?",
                 "options":["— Select —","20%","55%","71%","99%"],"correct":"71%",
                 "hint":"TP = 0.005×0.995 = 0.004975. FP = 0.995×0.002 = 0.00199. PPV = 0.004975/(0.004975+0.00199) = **71.4%**. Even with an excellent test, 29% of positives are false in a low-prevalence population.",
                 "wrong":{"20%":"❌ This would be expected with much lower specificity. With 99.8% specificity in a 0.5% prevalence population: PPV = 0.004975/0.006965 ≈ 71%.","55%":"❌ PPV = TP/(TP+FP) = 0.004975/(0.004975+0.00199) ≈ 71%. Check your false positive rate calculation.","99%":"❌ PPV is not the same as sensitivity. Despite 99.5% sensitivity, a positive result in a low-prevalence population is only 71% likely to be true. This is the base rate fallacy."}},
                {"q":"The patient asks: 'Does this mean I definitely have HIV?' What is the most accurate response?",
                 "options":["— Select —","Yes — the test is 99.5% accurate","No — there is approximately a 29% chance this is a false positive","No — this test is too unreliable to act on","Yes — a positive result always confirms diagnosis"],"correct":"No — there is approximately a 29% chance this is a false positive",
                 "hint":"PPV = 71% means 71% of positives are true positives and 29% are false positives. A confirmatory test (Western blot) is needed. This is standard practice for HIV screening — reactive ELISA is always confirmed.",
                 "wrong":{"Yes — the test is 99.5% accurate":"❌ '99.5% accurate' refers to sensitivity — detecting true cases. It does not mean a positive result is 99.5% likely to be a true positive. PPV depends on both test performance AND prevalence.","No — this test is too unreliable to act on":"❌ The test is excellent. The issue is not reliability but prevalence. A confirmatory test is needed, not abandoning the result.","Yes — a positive result always confirms diagnosis":"❌ No screening test alone confirms diagnosis. All reactive HIV screening tests require confirmatory testing."}},
                {"q":"If this same test were used in a population with HIV prevalence of 10% (e.g., a high-risk clinic), how would PPV change?",
                 "options":["— Select —","PPV would decrease","PPV would stay the same","PPV would increase","Cannot determine without more information"],"correct":"PPV would increase",
                 "hint":"PPV increases with prevalence. At 10% prevalence: TP = 0.10×0.995 = 0.0995, FP = 0.90×0.002 = 0.0018. PPV = 0.0995/0.1013 = **98.2%** — dramatically higher than 71%.",
                 "wrong":{"PPV would decrease":"❌ Higher prevalence → more true positives relative to false positives → higher PPV. PPV always increases as prevalence increases (holding sensitivity and specificity constant).","PPV would stay the same":"❌ PPV depends on prevalence. The same test produces different PPV in different populations. This is why population context matters for interpreting test results.","Cannot determine without more information":"❌ We have all the information needed. Sensitivity = 99.5%, specificity = 99.8%, new prevalence = 10%. PPV can be calculated directly."}}
            ],
            "calculation":{"type":"ppv_npv","prev":0.005,"sens":0.995,"spec":0.998,"n":10000}
        },
        {
            "id":"pr2","title":"Scenario 2: Mammography Screening",
            "description":"A 45-year-old woman with no family history of breast cancer undergoes routine mammography. Breast cancer prevalence in women her age is approximately 1.5%. Digital mammography has sensitivity of 85% and specificity of 90%. Her mammogram comes back as 'suspicious — recall for further imaging.'",
            "questions":[
                {"q":"What is the approximate PPV of this mammogram result?",
                 "options":["— Select —","11%","50%","85%","90%"],"correct":"11%",
                 "hint":"TP = 0.015×0.85 = 0.01275. FP = 0.985×0.10 = 0.0985. PPV = 0.01275/(0.01275+0.0985) = **0.115 ≈ 11%**. Most recalls after mammography are false positives.",
                 "wrong":{"50%":"❌ PPV = TP/(TP+FP) = 0.01275/0.111 ≈ 11%. The high false positive rate (10%) overwhelms the true positives in this low-prevalence population.","85%":"❌ 85% is the sensitivity — the probability of a positive test GIVEN disease. PPV is the probability of disease GIVEN a positive test. These are very different at low prevalence.","90%":"❌ 90% is the specificity. PPV = TP/(TP+FP) ≈ 11% in this population. The majority of positive mammograms in average-risk women are false positives."}},
                {"q":"Which statement best explains why so many recalls after mammography are false positives?",
                 "options":["— Select —","The test has poor sensitivity","Breast cancer is relatively rare in the screened population","Radiologists read mammograms incorrectly most of the time","The test is not specific enough for clinical use"],"correct":"Breast cancer is relatively rare in the screened population",
                 "hint":"The base rate (prevalence) drives PPV. With only 1.5% prevalence, even a 10% false positive rate generates far more false positives than a 1.5% disease rate generates true positives. This is the fundamental challenge of cancer screening.",
                 "wrong":{"The test has poor sensitivity":"❌ 85% sensitivity is actually reasonable. The issue is prevalence, not sensitivity. Even a 99% sensitive test would still produce mostly false positives in a 1.5% prevalence population.","Radiologists read mammograms incorrectly most of the time":"❌ The false positive rate reflects the test's specificity (90%), not radiologist error. At 90% specificity, 10% of true negatives will test positive by design.","The test is not specific enough for clinical use":"❌ 90% specificity is typical and within the accepted range for mammography. The clinical challenge is the math of low prevalence, not inadequate specificity."}},
                {"q":"The patient is understandably anxious. What should be communicated?",
                 "options":["— Select —","She almost certainly has cancer","About 9 out of 10 women recalled after mammography do not have cancer","The mammogram result is not reliable enough to act on","She should have avoided screening"],"correct":"About 9 out of 10 women recalled after mammography do not have cancer",
                 "hint":"PPV ≈ 11% means about 11 in 100 women recalled have cancer — approximately 9 in 10 do NOT. This is accurate, evidence-based risk communication that is reassuring without being dismissive.",
                 "wrong":{"She almost certainly has cancer":"❌ PPV ≈ 11% means the probability of cancer after a suspicious mammogram is about 11%, not near certain. This communication would cause unnecessary harm.","The mammogram result is not reliable enough to act on":"❌ The result is reliable — it correctly identified a finding warranting further investigation. The appropriate action is recall for additional imaging (ultrasound or biopsy), not dismissal.","She should have avoided screening":"❌ False positives are an acknowledged tradeoff of screening programs. The benefit of detecting true cancers is weighed against the harm of false positive callbacks. Screening is still recommended for eligible women."}}
            ],
            "calculation":{"type":"ppv_npv","prev":0.015,"sens":0.85,"spec":0.90,"n":10000}
        },
        {
            "id":"pr3","title":"Scenario 3: Drug Efficacy — Absolute vs. Relative Risk",
            "description":"A clinical trial of a new statin reports: 'Treatment reduced cardiovascular events by 36% compared to placebo.' In the trial, 4.8% of placebo patients had an event vs. 3.1% of treated patients over 5 years.",
            "questions":[
                {"q":"What does the '36% reduction' figure represent?",
                 "options":["— Select —","Absolute risk reduction","Relative risk reduction","Number needed to treat","Attributable risk percent"],"correct":"Relative risk reduction",
                 "hint":"RRR = (Risk_control − Risk_treated) / Risk_control = (4.8% − 3.1%) / 4.8% = 1.7% / 4.8% = **35.4% ≈ 36%**. This is the proportional (relative) reduction, not the absolute reduction.",
                 "wrong":{"Absolute risk reduction":"❌ Absolute risk reduction = 4.8% − 3.1% = 1.7%. The 36% figure is the relative risk reduction — how much of the control group's risk was eliminated.","Number needed to treat":"❌ NNT = 1 / absolute risk reduction = 1 / 0.017 ≈ 59. The 36% figure is the relative risk reduction.","Attributable risk percent":"❌ AR% = (risk_exposed − risk_unexposed) / risk_exposed — typically applied to harmful exposures, not treatments. The 36% is the relative risk reduction."}},
                {"q":"What is the absolute risk reduction and NNT?",
                 "options":["— Select —","ARR = 36%, NNT = 3","ARR = 1.7%, NNT = 59","ARR = 3.1%, NNT = 32","ARR = 4.8%, NNT = 21"],"correct":"ARR = 1.7%, NNT = 59",
                 "hint":"ARR = 4.8% − 3.1% = **1.7%**. NNT = 1/0.017 = **59**. For every 59 patients treated for 5 years, 1 cardiovascular event is prevented.",
                 "wrong":{"ARR = 36%, NNT = 3":"❌ 36% is the relative risk reduction, not the absolute risk reduction. ARR = 4.8% − 3.1% = 1.7%. NNT = 1/0.017 = 59.","ARR = 3.1%, NNT = 32":"❌ 3.1% is the event rate in the treated group, not the absolute risk reduction. ARR = difference in event rates = 4.8% − 3.1% = 1.7%.","ARR = 4.8%, NNT = 21":"❌ 4.8% is the control group's event rate, not the absolute risk reduction. ARR = 4.8% − 3.1% = 1.7%."}},
                {"q":"A patient says 'If this drug reduces my risk by 36%, I definitely want it.' What additional information is most important to share?",
                 "options":["— Select —","The cost of the medication","That the absolute reduction is only 1.7% over 5 years, meaning 58 of 59 patients get no event benefit","That relative risk reduction always overstates the benefit","That NNT of 59 means the drug is ineffective"],"correct":"That the absolute reduction is only 1.7% over 5 years, meaning 58 of 59 patients get no event benefit",
                 "hint":"NNT = 59 means 59 patients must be treated for 5 years for 1 to benefit. This does not mean the drug is bad — it means the patient should understand the absolute magnitude of benefit alongside the relative figure. The decision also depends on side effects, cost, and individual risk.",
                 "wrong":{"The cost of the medication":"❌ Cost is relevant but secondary. The most important clinical information is helping the patient understand that a '36% reduction' means 1.7 percentage points — a meaningful but modest absolute benefit.","That relative risk reduction always overstates the benefit":"❌ RRR doesn't inherently overstate — it's a valid metric. The issue is that RRR alone, without ARR context, can be misleading. Both should be communicated.","That NNT of 59 means the drug is ineffective":"❌ NNT = 59 for a 5-year cardiovascular outcome is actually quite reasonable for a preventive medication. NNT must be interpreted in the context of disease severity and treatment burden."}}
            ],
            "calculation":{"type":"risk_comm","r_exp":0.031,"r_unexp":0.048}
        },
        {
            "id":"pr4","title":"Scenario 4: Bayes' Theorem — Chest Pain in the ED",
            "description":"A 55-year-old male smoker presents to the ED with chest pain. Based on his age, sex, smoking history, and symptom character, the emergency physician estimates a pre-test probability of acute MI of 40%. A troponin test is ordered with sensitivity = 93% and specificity = 89%.",
            "questions":[
                {"q":"What are the likelihood ratios for a positive and negative troponin result?",
                 "options":["— Select —","LR+ = 8.5, LR− = 0.08","LR+ = 9.3, LR− = 0.07","LR+ = 6.5, LR− = 0.12","LR+ = 4.7, LR− = 0.19"],"correct":"LR+ = 8.5, LR− = 0.08",
                 "hint":"LR+ = Sensitivity / (1−Specificity) = 0.93 / (1−0.89) = 0.93 / 0.11 = **8.45 ≈ 8.5**. LR− = (1−Sensitivity) / Specificity = (1−0.93) / 0.89 = 0.07 / 0.89 = **0.079 ≈ 0.08**.",
                 "wrong":{"LR+ = 9.3, LR− = 0.07":"❌ LR+ = sensitivity/(1−specificity) = 0.93/0.11 = 8.45 ≈ 8.5. LR− = (1−sensitivity)/specificity = 0.07/0.89 = 0.079 ≈ 0.08.","LR+ = 6.5, LR− = 0.12":"❌ LR+ = 0.93/(1−0.89) = 0.93/0.11 = 8.45. LR− = 0.07/0.89 = 0.079. Check your specificity subtraction.","LR+ = 4.7, LR− = 0.19":"❌ LR+ = sensitivity/(1−specificity) = 0.93/0.11 = 8.45 ≈ 8.5, not 4.7."}},
                {"q":"If troponin is POSITIVE, what is the post-test probability of MI?",
                 "options":["— Select —","40%","74%","85%","93%"],"correct":"85%",
                 "hint":"Pre-test odds = 0.40/0.60 = 0.667. Post-test odds = 0.667 × 8.5 = 5.667. Post-test probability = 5.667/(5.667+1) = **0.85 = 85%**.",
                 "wrong":{"40%":"❌ 40% is the pre-test probability — before the test. A positive troponin substantially raises this. Post-test probability = pre-test odds × LR+ converted back to probability = 85%.","74%":"❌ Post-test odds = (0.40/0.60) × 8.5 = 5.667. Post-test prob = 5.667/6.667 = 85%, not 74%.","93%":"❌ 93% is the sensitivity. Post-test probability = 85%. They are different: sensitivity is P(Test+|Disease), post-test prob is P(Disease|Test+)."}},
                {"q":"If troponin is NEGATIVE, what is the post-test probability of MI?",
                 "options":["— Select —","5%","8%","14%","32%"],"correct":"5%",
                 "hint":"Pre-test odds = 0.667. Post-test odds (negative) = 0.667 × 0.08 = 0.0533. Post-test prob = 0.0533/1.0533 = **0.051 ≈ 5%**. A negative troponin in this patient reduces MI probability from 40% to 5%.",
                 "wrong":{"8%":"❌ Post-test odds = 0.667 × 0.08 = 0.0533. Prob = 0.0533/(1+0.0533) = 5.1%, approximately 5%.","14%":"❌ Post-test odds = pre-test odds × LR− = (0.40/0.60) × 0.08 = 0.0533. Prob = 5.1%.","32%":"❌ 32% would result from a much weaker LR−. With LR− = 0.08: post-test prob = 5%. A negative troponin in this patient is quite reassuring."}}
            ],
            "calculation":{"type":"likelihood_ratio","prev":0.40,"sens":0.93,"spec":0.89}
        },
        {
            "id":"pr5","title":"Scenario 5: Probability Rules — Disease Co-occurrence",
            "description":"In a population-based study, 11% of adults have type 2 diabetes (T2D), 47% have hypertension, and 8% have both conditions. Use probability rules to answer the questions below.",
            "questions":[
                {"q":"What is the probability that a randomly selected adult has T2D OR hypertension (or both)?",
                 "options":["— Select —","50%","58%","50.2%","58% minus some overlap"],"correct":"50%",
                 "hint":"P(T2D or HTN) = P(T2D) + P(HTN) − P(both) = 0.11 + 0.47 − 0.08 = **0.50 = 50%**. Don't forget to subtract the overlap — otherwise you'd count people with both conditions twice.",
                 "wrong":{"58%":"❌ 58% = 0.11 + 0.47 without subtracting the overlap. P(A or B) = P(A) + P(B) − P(A and B) = 0.11 + 0.47 − 0.08 = 0.50.","50.2%":"❌ P(T2D or HTN) = 0.11 + 0.47 − 0.08 = 0.50 exactly. Check your arithmetic.","58% minus some overlap":"❌ 'Some overlap' must be specified: P(A or B) = P(A) + P(B) − P(A and B) = 0.11 + 0.47 − 0.08 = 0.50."}},
                {"q":"Are T2D and hypertension independent in this population?",
                 "options":["— Select —","Yes — both are common diseases","No — P(T2D and HTN) ≠ P(T2D) × P(HTN)","Yes — 8% overlap is small","Cannot be determined"],"correct":"No — P(T2D and HTN) ≠ P(T2D) × P(HTN)",
                 "hint":"If independent: P(T2D and HTN) = 0.11 × 0.47 = **0.0517 = 5.17%**. Observed: **8%**. Since 8% ≠ 5.17%, they are NOT independent — people with T2D are more likely to also have hypertension (shared risk factors: obesity, age, metabolic syndrome).",
                 "wrong":{"Yes — both are common diseases":"❌ Being common does not make events independent. Independence requires P(A and B) = P(A) × P(B). Here: 0.11 × 0.47 = 5.17% ≠ 8% observed.","Yes — 8% overlap is small":"❌ Absolute size doesn't determine independence. If independent, we'd expect 5.17% overlap. Observing 8% — 54% more than expected — indicates strong non-independence.","Cannot be determined":"❌ Independence can be tested: if P(A and B) = P(A) × P(B), they are independent. Here 0.11 × 0.47 = 5.17% ≠ 8%, so they are not independent."}},
                {"q":"Given that a patient has T2D, what is P(hypertension)?",
                 "options":["— Select —","47%","58%","73%","8%"],"correct":"73%",
                 "hint":"P(HTN|T2D) = P(HTN and T2D) / P(T2D) = 0.08 / 0.11 = **0.727 = 73%**. Among patients with T2D, 73% also have hypertension — much higher than the 47% population prevalence.",
                 "wrong":{"47%":"❌ 47% is the unconditional probability of hypertension. P(HTN|T2D) = P(both)/P(T2D) = 0.08/0.11 = 73%. Knowing a patient has T2D substantially increases the probability of hypertension.","58%":"❌ P(HTN|T2D) = 0.08/0.11 = 72.7%. 58% doesn't correspond to any meaningful calculation here.","8%":"❌ 8% is P(T2D and HTN) — the joint probability. Conditional probability P(HTN|T2D) = P(both)/P(T2D) = 0.08/0.11 = 73%."}}
            ],
            "calculation":{"type":"prob_rules","pA":0.11,"pB":0.47,"pAandB":0.08}
        },
        {
            "id":"pr6","title":"Scenario 6: Normal Distribution — Blood Pressure Screening",
            "description":"Systolic blood pressure in a population of 40–60 year olds follows a normal distribution with mean 125 mmHg and standard deviation 18 mmHg. Hypertension is defined as systolic BP ≥ 140 mmHg.",
            "questions":[
                {"q":"What z-score corresponds to a systolic BP of 140 mmHg?",
                 "options":["— Select —","z = 0.83","z = 0.78","z = 1.39","z = 1.83"],"correct":"z = 0.83",
                 "hint":"z = (x − μ) / σ = (140 − 125) / 18 = 15/18 = **0.833 ≈ 0.83**",
                 "wrong":{"z = 0.78":"❌ z = (140−125)/18 = 15/18 = 0.833 ≈ 0.83, not 0.78. Check your subtraction: 140−125 = 15.","z = 1.39":"❌ z = (140−125)/18 = 0.833. 1.39 would correspond to BP of 125 + 1.39×18 = 150 mmHg.","z = 1.83":"❌ z = 15/18 = 0.833. 1.83 would correspond to BP = 125 + 1.83×18 = 158 mmHg."}},
                {"q":"Approximately what percentage of this population has hypertension (SBP ≥ 140)?",
                 "options":["— Select —","10%","20%","30%","40%"],"correct":"20%",
                 "hint":"z = 0.833. P(Z > 0.833) = 1 − Φ(0.833) ≈ 1 − 0.798 = **0.202 ≈ 20%**. About 1 in 5 adults in this age group has hypertension.",
                 "wrong":{"10%":"❌ P(Z > 0.833) ≈ 20%. 10% would correspond to z ≈ 1.28, i.e., BP = 125 + 1.28×18 = 148 mmHg.","30%":"❌ P(Z > 0.833) ≈ 20%. 30% would correspond to a lower z-score, i.e., a lower BP cutoff.","40%":"❌ P(Z > 0.833) ≈ 20%. 40% would correspond to z < 0.25, i.e., BP cutoff below 130 mmHg."}},
                {"q":"A patient's BP is 158 mmHg. What percentile does this represent?",
                 "options":["— Select —","84th","91st","96th","99th"],"correct":"96th",
                 "hint":"z = (158−125)/18 = 33/18 = 1.833. P(Z ≤ 1.833) ≈ **0.967 = 97th percentile** — closest answer is 96th.",
                 "wrong":{"84th":"❌ The 84th percentile corresponds to z = 1.0, i.e., BP = 125 + 18 = 143 mmHg. z = 1.833 corresponds to approximately the 97th percentile.","91st":"❌ The 91st percentile corresponds to z ≈ 1.34, i.e., BP ≈ 149 mmHg. For BP = 158: z = 1.833 → approximately 97th percentile.","99th":"❌ The 99th percentile corresponds to z ≈ 2.33, i.e., BP ≈ 167 mmHg. For BP = 158: z = 1.833 → approximately 97th percentile."}}
            ],
            "calculation":{"type":"normal","mean":125,"sd":18,"x":140}
        },
        {
            "id":"pr7","title":"Scenario 7: Binomial — Adverse Events in a Clinical Trial",
            "description":"A new vaccine has a 5% rate of a mild adverse event (arm soreness lasting >24 hours) in clinical trials. A clinic administers the vaccine to 30 patients today.",
            "questions":[
                {"q":"What is the expected number of patients who will experience this adverse event?",
                 "options":["— Select —","0.5 patients","1.5 patients","3.0 patients","5.0 patients"],"correct":"1.5 patients",
                 "hint":"E(X) = n × p = 30 × 0.05 = **1.5 patients**. On average, 1.5 of 30 vaccinated patients will experience the adverse event.",
                 "wrong":{"0.5 patients":"❌ E(X) = n × p = 30 × 0.05 = 1.5. 0.5 would be n × p = 10 × 0.05 (only 10 patients).","3.0 patients":"❌ E(X) = 30 × 0.05 = 1.5, not 3.0. 3.0 would result from p = 10% with n = 30.","5.0 patients":"❌ E(X) = n × p = 30 × 0.05 = 1.5. 5.0 would result from n × p = 100 × 0.05."}},
                {"q":"What is the probability that EXACTLY 3 patients experience the adverse event?",
                 "options":["— Select —","2.4%","5.0%","8.9%","14.3%"],"correct":"8.9%",
                 "hint":"P(X=3) = C(30,3) × 0.05³ × 0.95²⁷ = 4060 × 0.000125 × 0.2503 = **0.089 = 8.9%**",
                 "wrong":{"2.4%":"❌ P(X=3) = C(30,3) × 0.05³ × 0.95²⁷ = 4060 × 0.000125 × 0.2503 ≈ 8.9%. Check your binomial coefficient: C(30,3) = 30!/(3!×27!) = 4060.","5.0%":"❌ 5% is the per-patient probability, not P(exactly 3 out of 30). P(X=3) = C(30,3) × 0.05³ × 0.95²⁷ ≈ 8.9%.","14.3%":"❌ P(X=3) ≈ 8.9%. 14.3% might correspond to a different k value or different probability."}},
                {"q":"What is the probability that 5 OR MORE patients experience the adverse event?",
                 "options":["— Select —","1.5%","3.2%","8.7%","15.4%"],"correct":"3.2%",
                 "hint":"P(X≥5) = 1 − P(X≤4). Using the binomial CDF: P(X≤4) ≈ 0.968. So P(X≥5) ≈ **1 − 0.968 = 0.032 = 3.2%**. Seeing 5+ adverse events would be unusual — worth investigating.",
                 "wrong":{"1.5%":"❌ P(X≥5) = 1 − P(X≤4) ≈ 1 − 0.968 = 3.2%. 1.5% corresponds approximately to P(X≥6).","8.7%":"❌ P(X≥5) ≈ 3.2%, not 8.7%. 8.7% would correspond to P(X≥3) or P(X≥4) approximately.","15.4%":"❌ P(X≥5) = 1 − P(X≤4) ≈ 3.2%. 15.4% would correspond to P(X≥2) approximately."}}
            ],
            "calculation":{"type":"binomial","n":30,"p":0.05,"k":3}
        },
        {
            "id":"pr8","title":"Scenario 8: Conditional Probability — Contact Tracing",
            "description":"During a COVID-19 outbreak investigation, a contact tracing team identifies 500 close contacts of confirmed cases. Of these, 80 test positive (infected). Among the 80 infected contacts, 60 had attended an indoor gathering (Event A). Among the 420 uninfected contacts, 100 had also attended Event A.",
            "questions":[
                {"q":"What is P(infected | attended Event A)?",
                 "options":["— Select —","12%","37.5%","60%","75%"],"correct":"37.5%",
                 "hint":"Those who attended Event A: 60 infected + 100 not infected = 160 total. P(infected|Event A) = 60/160 = **0.375 = 37.5%**.",
                 "wrong":{"12%":"❌ P(infected|Event A) = 60/(60+100) = 60/160 = 37.5%. 12% would be the overall attack rate (80/500 = 16%), not the conditional probability given event attendance.","60%":"❌ 60 is the number of infected attendees, not the probability. P(infected|Event A) = 60/(60+100) = 37.5%.","75%":"❌ P(infected|Event A) = 60/160 = 37.5%. 75% would mean 75% of Event A attendees were infected."}},
                {"q":"What is P(infected | did NOT attend Event A)?",
                 "options":["— Select —","5.9%","20%","37.5%","50%"],"correct":"5.9%",
                 "hint":"Non-attendees: 500−160 = 340 total. Infected non-attendees: 80−60 = 20. P(infected|no event) = 20/340 = **0.059 = 5.9%**.",
                 "wrong":{"20%":"❌ 20 is the number of infected non-attendees, not the probability. P(infected|no event) = 20/340 = 5.9%.","37.5%":"❌ 37.5% is P(infected|attended event). P(infected|did NOT attend) = 20/340 = 5.9% — much lower.","50%":"❌ P(infected|no event) = 20/340 = 5.9%. 50% would require half of non-attendees to be infected."}},
                {"q":"Based on this conditional probability analysis, what can be concluded about Event A?",
                 "options":["— Select —","Event A caused COVID-19 infection","Attending Event A is strongly associated with infection (RR ≈ 6.4)","Event A is not related to infection risk","The sample size is too small to draw any conclusions"],"correct":"Attending Event A is strongly associated with infection (RR ≈ 6.4)",
                 "hint":"RR = P(infected|event) / P(infected|no event) = 37.5% / 5.9% = **6.4**. Attendees were 6.4× more likely to be infected. This is a strong association warranting further investigation as a potential transmission event.",
                 "wrong":{"Event A caused COVID-19 infection":"❌ Association ≠ causation. The strong association (RR=6.4) suggests Event A is a likely transmission venue, but this observational analysis alone does not prove causation.","Event A is not related to infection risk":"❌ P(infected|event) = 37.5% vs P(infected|no event) = 5.9% is a very large difference. RR = 6.4. Event A is strongly associated with infection.","The sample size is too small to draw any conclusions":"❌ n=500 with 80 infected cases is adequate for this analysis. The RR of 6.4 is both statistically and epidemiologically meaningful."}}
            ],
            "calculation":{"type":"conditional","table":[[60,100],[20,320]]}
        },
        {
            "id":"pr9","title":"Scenario 9: Pre/Post-Test Probability — Lung Cancer Screening",
            "description":"A 62-year-old man with a 45 pack-year smoking history is referred for low-dose CT (LDCT) chest screening. His pre-test probability of lung cancer is estimated at 3.5% based on clinical risk factors. LDCT has sensitivity of 94% and specificity of 73% for lung cancer detection.",
            "questions":[
                {"q":"What is LR+ for this LDCT test?",
                 "options":["— Select —","2.4","3.5","3.9","12.8"],"correct":"3.5",
                 "hint":"LR+ = sensitivity / (1−specificity) = 0.94 / (1−0.73) = 0.94 / 0.27 = **3.48 ≈ 3.5**",
                 "wrong":{"2.4":"❌ LR+ = sensitivity/(1−specificity) = 0.94/0.27 = 3.48 ≈ 3.5. 2.4 would result from different test characteristics.","3.9":"❌ LR+ = 0.94/0.27 = 3.48 ≈ 3.5, not 3.9. Check: 1−specificity = 1−0.73 = 0.27.","12.8":"❌ LR+ = 0.94/0.27 = 3.5. 12.8 would require specificity ≈ 92.7% (LR+ = 0.94/0.073)."}},
                {"q":"If the LDCT is POSITIVE, what is the post-test probability of lung cancer?",
                 "options":["— Select —","3.5%","11%","22%","35%"],"correct":"11%",
                 "hint":"Pre-test odds = 0.035/0.965 = 0.0363. Post-test odds = 0.0363 × 3.5 = 0.127. Post-test prob = 0.127/(1+0.127) = **11.3% ≈ 11%**. A positive LDCT raises probability from 3.5% to 11%.",
                 "wrong":{"3.5%":"❌ 3.5% is the pre-test probability. A positive LDCT result raises this. Post-test prob = pre-test odds × LR+ converted to probability = 11%.","22%":"❌ Post-test odds = (0.035/0.965) × 3.5 = 0.127. Post-test prob = 0.127/1.127 = 11.3%. Not 22%.","35%":"❌ 35% would require a much higher LR+ or higher pre-test probability. With LR+ = 3.5 and pre-test = 3.5%: post-test = 11%."}},
                {"q":"The LDCT specificity is only 73%, meaning 27% of non-diseased patients test positive. Why is LDCT still recommended for high-risk smokers?",
                 "options":["— Select —","It is not recommended — the false positive rate is too high","The pre-test probability (3.5%) justifies screening despite low specificity","The benefit of detecting true early-stage cancers outweighs the harm from false positives in this high-risk group","Low-dose CT has no radiation risk so false positives are not harmful"],"correct":"The benefit of detecting true early-stage cancers outweighs the harm from false positives in this high-risk group",
                 "hint":"Lung cancer is a deadly but treatable disease when caught early. In high-risk smokers, the benefits (early detection, reduced mortality) outweigh the harms (false positives leading to additional imaging or procedures). This is a risk-benefit judgment, not just a mathematical one.",
                 "wrong":{"It is not recommended — the false positive rate is too high":"❌ LDCT is specifically recommended by USPSTF for high-risk smokers (ages 50–80, ≥20 pack-year history). The mortality benefit in this population has been demonstrated in the NLST trial.","The pre-test probability (3.5%) justifies screening despite low specificity":"❌ The justification is not solely mathematical — it involves clinical judgment about the severity of the disease, treatability when caught early, and the relative harm of false positives vs. missed cancers.","Low-dose CT has no radiation risk so false positives are not harmful":"❌ LDCT does involve radiation (though low-dose). False positives cause harm through anxiety, additional imaging, and occasionally invasive procedures. The recommendation reflects that benefits outweigh these harms."}}
            ],
            "calculation":{"type":"likelihood_ratio","prev":0.035,"sens":0.94,"spec":0.73}
        },
        {
            "id":"pr10","title":"Scenario 10: Decision Tree — Screening Program Design",
            "description":"A public health department is deciding whether to implement universal screening for a metabolic disorder in adults aged 40–60. Prevalence is 4%. A screening test costs $25, has 88% sensitivity and 92% specificity. If detected, treatment costs $800/year and reduces severe complications by 70%. Without screening, complications occur in 15% of undetected cases at a cost of $12,000 each.",
            "questions":[
                {"q":"In a population of 10,000 adults, how many true cases will be MISSED (false negatives) by universal screening?",
                 "options":["— Select —","24 cases","48 cases","96 cases","160 cases"],"correct":"48 cases",
                 "hint":"True cases = 10,000 × 0.04 = 400. False negatives = 400 × (1−0.88) = 400 × 0.12 = **48 cases**. These 48 people have the disorder but will test negative and not receive treatment.",
                 "wrong":{"24 cases":"❌ FN = total cases × (1−sensitivity) = 400 × 0.12 = 48. 24 would be FN if sensitivity were 94%.","96 cases":"❌ FN = 400 × (1−0.88) = 400 × 0.12 = 48. 96 would result from sensitivity of 76%.","160 cases":"❌ FN = 400 × 0.12 = 48. 160 would mean 40% of true cases are missed — that would require 60% sensitivity."}},
                {"q":"How many false positives will the screening program generate?",
                 "options":["— Select —","480 people","560 people","768 people","920 people"],"correct":"768 people",
                 "hint":"Non-diseased = 10,000 − 400 = 9,600. FP = 9,600 × (1−0.92) = 9,600 × 0.08 = **768 people** who will test positive but don't have the disorder.",
                 "wrong":{"480 people":"❌ FP = (N − true cases) × (1−specificity) = 9,600 × 0.08 = 768. 480 would result from 95% specificity.","560 people":"❌ FP = 9,600 × 0.08 = 768. 560 would result from specificity of approximately 94.2%.","920 people":"❌ FP = 9,600 × (1−0.92) = 9,600 × 0.08 = 768. 920 would require specificity of approximately 90.4%."}},
                {"q":"Which factor most strongly argues FOR implementing the screening program?",
                 "options":["— Select —","The test is highly sensitive (88%)","Early detection reduces severe complications by 70%, which have a high cost ($12,000) and significant health burden","The test is inexpensive ($25 per person)","The false positive rate is acceptably low at 8%"],"correct":"Early detection reduces severe complications by 70%, which have a high cost ($12,000) and significant health burden",
                 "hint":"The central argument for screening is the benefit of early detection — preventing a high-cost, high-burden complication. The 70% reduction in a 15% complication rate in a detectable population represents substantial prevented harm. Cost-effectiveness depends on the magnitude of the benefit prevented, not just test cost or accuracy alone.",
                 "wrong":{"The test is highly sensitive (88%)":"❌ 88% sensitivity means 12% of cases are missed. While reasonable, sensitivity alone doesn't justify a program — the key is whether early detection leads to meaningful improved outcomes.","The test is inexpensive ($25 per person)":"❌ Test cost ($25 × 10,000 = $250,000) is one factor, but the primary justification is the clinical benefit. A cheap test for a condition that isn't treatable or doesn't benefit from early detection would not justify screening.","The false positive rate is acceptably low at 8%":"❌ 8% FPR in a 4% prevalence population still generates 768 false positives vs. 352 true positives — less than a 1:1 ratio. The FPR alone doesn't justify or reject screening."}}
            ],
            "calculation":{"type":"screening_program","prev":0.04,"sens":0.88,"spec":0.92,"n":10000}
        },
    ]

    if "pr" not in st.session_state: st.session_state["pr"] = 0
    if "po" not in st.session_state:
        o = list(range(len(SCENARIOS))); random.shuffle(o)
        st.session_state["po"] = o
    rc = st.session_state["pr"]

    ch2, cr2 = st.columns([5,1])
    with ch2: st.caption(f"**{len(SCENARIOS)} scenarios** — one question at a time.")
    with cr2:
        if st.button("🔄 Reset", key="rst_prac"):
            st.session_state["pr"] += 1
            for k in [k for k in st.session_state if k.startswith("p_") and k not in ["pr","po"]]: del st.session_state[k]
            if "po" in st.session_state: del st.session_state["po"]
            st.rerun()

    SHUFFLED = [SCENARIOS[i] for i in st.session_state["po"]]

    for sc in SHUFFLED:
        st.divider()
        sid = sc["id"]
        q_states = [st.session_state.get(f"p_{sid}_q{qi}_c_{rc}") for qi in range(len(sc["questions"]))]
        all_done = all(q is True for q in q_states)
        correct_count = sum(1 for q in q_states if q is True)

        st.markdown(f"""
<div style='background:{LIGHT_BG};border-radius:8px;padding:14px 18px;border-left:4px solid {PRIMARY};'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <b style='color:{PRIMARY};font-size:16px;'>{sc['title']}</b>
    <span style='background:{"#2e7d32" if all_done else SECONDARY};color:white;border-radius:12px;padding:2px 12px;font-size:13px;'>{correct_count}/{len(sc['questions'])} correct</span>
  </div>
</div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown(sc["description"])

        for qi, q in enumerate(sc["questions"]):
            prev_ok = st.session_state.get(f"p_{sid}_q{qi-1}_c_{rc}") if qi > 0 else True
            if prev_ok is not True and qi > 0: break
            answered_correctly = st.session_state.get(f"p_{sid}_q{qi}_c_{rc}", False)
            st.markdown(f"**Question {qi+1}:** {q['q']}")
            if answered_correctly:
                st.success(f"✅ **{st.session_state.get(f'p_{sid}_q{qi}_a_{rc}')}** — {q['hint']}")
            else:
                choice = st.selectbox("Select your answer:", q["options"], key=f"p_{sid}_q{qi}_s_{rc}", label_visibility="collapsed")
                if choice != "— Select —":
                    if st.button("Submit Answer", key=f"p_{sid}_q{qi}_b_{rc}", type="primary"):
                        st.session_state[f"p_{sid}_q{qi}_a_{rc}"] = choice
                        st.session_state[f"p_{sid}_q{qi}_c_{rc}"] = (choice == q["correct"])
                        st.rerun()
                last_ans = st.session_state.get(f"p_{sid}_q{qi}_a_{rc}")
                last_cor = st.session_state.get(f"p_{sid}_q{qi}_c_{rc}")
                if last_ans and last_cor is False:
                    st.error(q.get("wrong",{}).get(last_ans,"❌ Not quite. Review the hint and try again."))
                    st.info(f"💡 **Hint:** {q['hint']}")

        if all_done and "calculation" in sc:
            st.markdown("---")
            st.markdown("### 🎉 All correct! Now run the calculations.")
            d = sc["calculation"]

            if d["type"] == "ppv_npv":
                tp = d["prev"]*d["sens"]; fp=(1-d["prev"])*(1-d["spec"])
                fn = d["prev"]*(1-d["sens"]); tn=(1-d["prev"])*d["spec"]
                ppv = round(tp/(tp+fp),4); npv = round(tn/(tn+fn),4)
                n = d["n"]
                col1,col2 = st.columns(2)
                col1.metric("PPV",f"{round(ppv*100,1)}%"); col2.metric("NPV",f"{round(npv*100,1)}%")
                st.markdown(f"Per {n:,} people: {round(tp*n):,} TP, {round(fp*n):,} FP, {round(fn*n):,} FN, {round(tn*n):,} TN")

            elif d["type"] == "likelihood_ratio":
                lr_p = round(d["sens"]/(1-d["spec"]),2); lr_n=round((1-d["sens"])/d["spec"],3)
                pre_o = d["prev"]/(1-d["prev"])
                pp_pos = round(pre_o*lr_p/(pre_o*lr_p+1),3)
                pp_neg = round(pre_o*lr_n/(pre_o*lr_n+1),3)
                col1,col2,col3,col4 = st.columns(4)
                col1.metric("LR+",lr_p); col2.metric("LR−",lr_n)
                col3.metric("Post-test prob (Test+)",f"{round(pp_pos*100,1)}%")
                col4.metric("Post-test prob (Test−)",f"{round(pp_neg*100,1)}%")

            elif d["type"] == "risk_comm":
                rr = round(d["r_unexp"]/d["r_exp"],2) if d["r_unexp"]!=0 else 0
                arr = round(abs(d["r_exp"]-d["r_unexp"])*100,2)
                rrr = round(abs(d["r_exp"]-d["r_unexp"])/d["r_unexp"]*100,1)
                nnt = round(1/abs(d["r_exp"]-d["r_unexp"]))
                col1,col2,col3,col4 = st.columns(4)
                col1.metric("RR",round(d["r_exp"]/d["r_unexp"],2)); col2.metric("ARR",f"{arr}%")
                col3.metric("RRR",f"{rrr}%"); col4.metric("NNT",nnt)

            elif d["type"] == "prob_rules":
                p_or = round(d["pA"]+d["pB"]-d["pAandB"],4)
                p_cond = round(d["pAandB"]/d["pA"],4)
                indep_expected = round(d["pA"]*d["pB"],4)
                col1,col2,col3 = st.columns(3)
                col1.metric("P(A or B)",f"{round(p_or*100,1)}%")
                col2.metric("P(B|A)",f"{round(p_cond*100,1)}%")
                col3.metric("Expected if independent",f"{round(indep_expected*100,1)}%")
                st.info(f"Observed P(both) = {round(d['pAandB']*100,1)}% vs. expected if independent = {round(indep_expected*100,1)}% — {'NOT independent' if abs(d['pAandB']-indep_expected)>0.005 else 'approximately independent'}.")

            elif d["type"] == "normal":
                z = round((d["x"]-d["mean"])/d["sd"],3)
                p_b = round(stats.norm.cdf(z)*100,1)
                p_a = round((1-stats.norm.cdf(z))*100,1)
                col1,col2,col3 = st.columns(3)
                col1.metric("Z-score",z); col2.metric(f"P(X ≤ {d['x']})",f"{p_b}%"); col3.metric(f"P(X > {d['x']})",f"{p_a}%")

            elif d["type"] == "binomial":
                p_ex = round(stats.binom.pmf(d["k"],d["n"],d["p"])*100,2)
                p_le = round(stats.binom.cdf(d["k"],d["n"],d["p"])*100,2)
                p_ge = round((1-stats.binom.cdf(d["k"]-1,d["n"],d["p"]))*100,2)
                col1,col2,col3,col4 = st.columns(4)
                col1.metric("E(X)",round(d["n"]*d["p"],1))
                col2.metric(f"P(X={d['k']})",f"{p_ex}%")
                col3.metric(f"P(X≤{d['k']})",f"{p_le}%")
                col4.metric(f"P(X≥{d['k']})",f"{p_ge}%")

            elif d["type"] == "screening_program":
                n = d["n"]; tp_s=round(n*d["prev"]*d["sens"]); fn_s=round(n*d["prev"]*(1-d["sens"]))
                fp_s=round(n*(1-d["prev"])*(1-d["spec"])); tn_s=round(n*(1-d["prev"])*d["spec"])
                ppv_s=round(tp_s/(tp_s+fp_s)*100,1); npv_s=round(tn_s/(tn_s+fn_s)*100,1)
                col1,col2,col3,col4 = st.columns(4)
                col1.metric("True Positives",f"{tp_s:,}"); col2.metric("False Negatives",f"{fn_s:,}")
                col3.metric("False Positives",f"{fp_s:,}"); col4.metric("PPV",f"{ppv_s}%")

    st.divider()
    if st.button("📊 Show My Score", key="show_score"):
        total_q = sum(len(sc["questions"]) for sc in SCENARIOS)
        correct_q = sum(sum(1 for qi in range(len(sc["questions"])) if st.session_state.get(f"p_{sc['id']}_q{qi}_c_{rc}") is True) for sc in SCENARIOS)
        answered = sum(sum(1 for qi in range(len(sc["questions"])) if st.session_state.get(f"p_{sc['id']}_q{qi}_c_{rc}") is not None) for sc in SCENARIOS)
        if answered == 0: st.info("You haven't answered any questions yet.")
        else:
            pct = round(correct_q/answered*100)
            st.subheader(f"Score: {correct_q} / {answered} questions")
            st.progress(pct/100)
            if pct==100: st.success("🏆 Perfect score!")
            elif pct>=80: st.success("Great work! Review any scenarios you found challenging.")
            elif pct>=60: st.info("Good progress. Revisit the Learn tab for concepts you're unsure about.")
            else: st.warning("Keep practicing. Use the Learn tab and Glossary to review.")

# ══════════════════════════════════════════════════════════
# TAB 3: GLOSSARY
# ══════════════════════════════════════════════════════════
with tab_glossary:
    st.markdown(f"### <span style='color:{PRIMARY}'>Glossary: Probability & Health</span>", unsafe_allow_html=True)

    with st.expander("📐 Basic Probability Rules", expanded=True):
        st.markdown("""
**Probability** — A number between 0 and 1 representing the likelihood of an event. P=0 means impossible; P=1 means certain.

**Complement rule** — P(not A) = 1 − P(A). If P(rain) = 0.3, then P(no rain) = 0.7.

**Addition rule** — P(A or B) = P(A) + P(B) − P(A and B). Subtract the overlap to avoid double-counting.

**Multiplication rule** — P(A and B) = P(A) × P(B|A). If independent: P(A and B) = P(A) × P(B).

**Mutually exclusive events** — Events that cannot both occur. P(A and B) = 0. P(A or B) = P(A) + P(B).

**Independence** — Two events are independent if P(B|A) = P(B). Knowing A occurred tells you nothing about B.
        """)

    with st.expander("🔬 Diagnostic Test Performance"):
        st.markdown("""
**Sensitivity** — P(Test+|Disease+) = TP/(TP+FN). Proportion of true cases correctly identified. High sensitivity → few false negatives → good for **ruling OUT** disease (SnNout).

**Specificity** — P(Test−|Disease−) = TN/(TN+FP). Proportion of true negatives correctly identified. High specificity → few false positives → good for **ruling IN** disease (SpPin).

**PPV** — P(Disease+|Test+) = TP/(TP+FP). Of all positives, what fraction are true? Increases with prevalence.

**NPV** — P(Disease−|Test−) = TN/(TN+FN). Of all negatives, what fraction are truly disease-free? Decreases with prevalence.

**LR+ = Sensitivity / (1−Specificity)** — How much a positive test multiplies the odds of disease. LR+ > 10 = strong evidence.

**LR− = (1−Sensitivity) / Specificity** — How much a negative test reduces the odds of disease. LR− < 0.1 = strong evidence against.

**Post-test odds = Pre-test odds × LR. Post-test probability = Post-test odds / (Post-test odds + 1)**
        """)

    with st.expander("📊 Bayes' Theorem"):
        st.markdown("""
**Bayes' theorem:** P(Disease|Test+) = P(Test+|Disease) × P(Disease) / P(Test+)

**Prior probability** — Your probability estimate BEFORE seeing new evidence (pre-test probability, prevalence).

**Posterior probability** — Updated probability AFTER incorporating new evidence (post-test probability, PPV).

**Base rate fallacy** — The error of ignoring prevalence when interpreting test results. A positive test for a rare disease is usually a false positive even with high sensitivity and specificity.

**Key insight:** The same test has different PPV in different populations depending on disease prevalence. Always consider the clinical context before ordering a test.
        """)

    with st.expander("⚠️ Risk Communication"):
        st.markdown("""
**Absolute Risk (AR)** — The actual probability of an event occurring in a group. AR = events/total.

**Relative Risk (RR)** — Ratio of risks in exposed vs. unexposed. RR = AR_exposed / AR_unexposed.

**Absolute Risk Difference (ARD)** — AR_exposed − AR_unexposed. The actual difference in event rates.

**Relative Risk Reduction (RRR)** — (ARD / AR_control) × 100%. Proportional reduction in risk. Can be misleading if ARD is small.

**NNT (Number Needed to Treat)** — 1 / ARD. How many patients need to receive treatment for one to benefit. Most intuitive measure for clinical decisions.

**NNH (Number Needed to Harm)** — 1 / ARD (where exposure is harmful). How many people need to be exposed for one additional harm.

**Best practice:** Always present BOTH relative and absolute risk measures. Relative risk alone, without absolute context, commonly misleads patients and clinicians.
        """)

    with st.expander("📈 Probability Distributions"):
        st.markdown("""
**Normal distribution** — Bell-shaped, symmetric. Defined by mean (μ) and standard deviation (σ). Used for continuous measurements (BP, height, lab values).

**68-95-99.7 rule** — 68% of values fall within ±1σ, 95% within ±2σ, 99.7% within ±3σ of the mean.

**Z-score** — (x − μ) / σ. Number of standard deviations a value is from the mean. Allows comparison across different scales.

**Binomial distribution** — Models number of successes in n independent trials with probability p. Mean = np. SD = √(np(1−p)).

**P(X=k) = C(n,k) × p^k × (1−p)^(n−k)**

Used for: number of patients responding, number of positive tests in a sample, disease cases in a group.
        """)

    with st.expander("🌳 Expected Value & Decision Trees"):
        st.markdown("""
**Expected value** — The probability-weighted average of all possible outcomes. E(X) = Σ[outcome × P(outcome)].

**Decision tree** — A diagram that maps out choices, chance events, and outcomes in a sequential decision problem. We calculate expected value at each node and choose the branch with the highest expected utility.

**Utility** — A measure of the value or desirability of an outcome, often expressed on a 0–1 scale (0 = worst, 1 = best health state).

**QALY (Quality-Adjusted Life Year)** — A measure combining quality and quantity of life. Used in cost-effectiveness analysis to compare health interventions.

**Key principle:** Expected value helps make consistent decisions under uncertainty, but it must be combined with clinical judgment, patient values, and resource considerations.
        """)

    with st.expander("❓ Common Confusions"):
        st.markdown("""
**Sensitivity ≠ PPV.** Sensitivity is P(Test+|Disease). PPV is P(Disease|Test+). They are the reverse of each other and differ dramatically at low prevalence.

**p-value ≠ probability the null hypothesis is true.** p = P(data this extreme | H0 is true). It does not tell you whether H0 is true.

**Relative risk reduction alone misleads.** A drug reducing risk from 0.02% to 0.01% is a "50% reduction" — but ARD = 0.01% and NNT = 10,000. Always check absolute numbers.

**Independence is rarely the default in health.** Most disease risk factors are correlated. Don't multiply probabilities without verifying independence.

**High sensitivity does not guarantee high PPV.** A test with 99% sensitivity and 90% specificity has PPV of only 9% in a 1% prevalence population. Prevalence drives PPV.

**Expected value is a population concept.** For an individual patient, the actual outcome will be one specific result — not the average. Expected value guides policy; clinical judgment guides the individual encounter.
        """)

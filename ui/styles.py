"""Application stylesheet, injected once per run."""

CSS = """
<style>
.hero {background: linear-gradient(120deg,#1e3a5f,#2c5f8a); color:#fff;
       padding:1.4rem 1.8rem; border-radius:14px; margin-bottom:1rem;}
.hero h1 {margin:0; font-size:1.9rem;}
.hero p {margin:.3rem 0 0 0; opacity:.9;}
.metric-card {background:#f7f9fc; border:1px solid #e1e7ef; border-radius:12px;
              padding:1rem; text-align:center; min-height:108px;}
.metric-card .label {font-size:.8rem; color:#5b6878; text-transform:uppercase;
                     letter-spacing:.05em;}
.metric-card .value {font-size:1.5rem; font-weight:700; color:#1e3a5f; word-wrap:break-word;}
.pill {display:inline-block; padding:.25rem .85rem; border-radius:999px;
       font-weight:600; font-size:.85rem; color:#fff;}
.pill-safe {background:#1b8a4b;}
.pill-warn {background:#d98e04;}
.pill-danger {background:#c0392b;}
.sev {display:inline-block; padding:.15rem .6rem; border-radius:6px;
      font-size:.75rem; font-weight:700; color:#fff; margin-right:.4rem;}
.sev-Low {background:#2e86c1;}
.sev-Medium {background:#d98e04;}
.sev-High {background:#e67e22;}
.sev-Critical {background:#c0392b;}
.alert {border-left:5px solid #c0392b; background:#fdf2f0; padding:.8rem 1rem;
        border-radius:8px; margin-bottom:.6rem;}
.alert-info {border-left-color:#2e86c1; background:#eef6fc;}
.alert-warn {border-left-color:#d98e04; background:#fdf6e3;}
</style>
"""

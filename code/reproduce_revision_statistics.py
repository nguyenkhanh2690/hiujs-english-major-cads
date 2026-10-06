#!/usr/bin/env python3
from pathlib import Path
import json, sys
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

BASE = Path(__file__).resolve().parents[1]
INFILE = BASE / 'derived_outputs' / 'theme_by_university.csv'
OUTDIR = BASE / 'validation'
OUTDIR.mkdir(exist_ok=True)
SEED = 20260802
N_BOOT = 10000
THEMES = [
    'Employability','Internationalisation','Professional competence','Digital skills',
    'Intercultural competence','Career identities','Promotional evaluation','Agency and modality'
]

def rbc(private, public):
    a=np.asarray(private); b=np.asarray(public)
    u=mannwhitneyu(a,b,alternative='two-sided',method='asymptotic').statistic
    return float(2*u/(len(a)*len(b))-1), float(u)

def bootstrap_cis(df):
    rng=np.random.default_rng(SEED)
    out={}
    for theme in THEMES:
        pri=df[df['Ownership']=='Private'][f'{theme} per 10,000'].to_numpy(float)
        pub=df[df['Ownership']=='Public'][f'{theme} per 10,000'].to_numpy(float)
        pri_b = pri[rng.integers(0, len(pri), size=(N_BOOT, len(pri)))]
        pub_b = pub[rng.integers(0, len(pub), size=(N_BOOT, len(pub)))]
        gt = (pri_b[:, :, None] > pub_b[:, None, :]).sum(axis=(1,2))
        eq = (pri_b[:, :, None] == pub_b[:, None, :]).sum(axis=(1,2))
        u = gt + 0.5*eq
        vals = 2*u/(len(pri)*len(pub)) - 1
        lo,hi=np.quantile(vals,[0.025,0.975])
        out[theme]=(float(lo),float(hi))
    return out

def full_table(df):
    cis=bootstrap_cis(df)
    rows=[]; ps=[]
    for theme in THEMES:
        pri=df[df['Ownership']=='Private'][f'{theme} per 10,000'].to_numpy(float)
        pub=df[df['Ownership']=='Public'][f'{theme} per 10,000'].to_numpy(float)
        r,u=rbc(pri,pub)
        p=float(mannwhitneyu(pri,pub,alternative='two-sided',method='asymptotic').pvalue)
        ps.append(p)
        rows.append({
            'Theme':theme,
            'PUC median':float(np.median(pub)), 'PUC Q1':float(np.quantile(pub,.25)), 'PUC Q3':float(np.quantile(pub,.75)),
            'PrUC median':float(np.median(pri)), 'PrUC Q1':float(np.quantile(pri,.25)), 'PrUC Q3':float(np.quantile(pri,.75)),
            'Mann-Whitney U (Private vs Public)':u, 'Rank-biserial':r,
            'CI lower':cis[theme][0], 'CI upper':cis[theme][1], 'Raw p':p
        })
    adj=multipletests(ps,alpha=.05,method='fdr_bh')[1]
    for row,a in zip(rows,adj): row['BH-adjusted p']=float(a)
    return pd.DataFrame(rows)

def length_trimmed(df):
    keep=[]
    for own in ['Public','Private']:
        g=df[df['Ownership']==own].sort_values('Analytic tokens')
        keep.append(g.iloc[2:-2])
    d=pd.concat(keep,ignore_index=True)
    rows=[]; ps=[]
    for theme in THEMES:
        pri=d[d['Ownership']=='Private'][f'{theme} per 10,000'].to_numpy(float)
        pub=d[d['Ownership']=='Public'][f'{theme} per 10,000'].to_numpy(float)
        r,u=rbc(pri,pub); p=float(mannwhitneyu(pri,pub,alternative='two-sided',method='asymptotic').pvalue)
        ps.append(p); rows.append({'Theme':theme,'n Public':len(pub),'n Private':len(pri),'Rank-biserial':r,'Raw p':p})
    adj=multipletests(ps,alpha=.05,method='fdr_bh')[1]
    for row,a in zip(rows,adj): row['BH-adjusted p']=float(a)
    return pd.DataFrame(rows)

def leave_one_out(df):
    rows=[]
    for excluded in df['School ID']:
        d=df[df['School ID']!=excluded]
        ps=[]; tmp=[]
        for theme in THEMES:
            pri=d[d['Ownership']=='Private'][f'{theme} per 10,000'].to_numpy(float)
            pub=d[d['Ownership']=='Public'][f'{theme} per 10,000'].to_numpy(float)
            r,u=rbc(pri,pub); p=float(mannwhitneyu(pri,pub,alternative='two-sided',method='asymptotic').pvalue)
            ps.append(p); tmp.append((theme,r,u,p))
        adj=multipletests(ps,alpha=.05,method='fdr_bh')[1]
        for (theme,r,u,p),a in zip(tmp,adj):
            rows.append({'Excluded School ID':excluded,'Theme':theme,'Rank-biserial':r,'Raw p':p,'BH-adjusted p':float(a)})
    return pd.DataFrame(rows)

def main():
    df=pd.read_csv(INFILE)
    table4=full_table(df); table4.to_csv(OUTDIR/'table4_revised.csv',index=False)
    trim=length_trimmed(df); trim.to_csv(OUTDIR/'length_trimmed_sensitivity.csv',index=False)
    loo=leave_one_out(df); loo.to_csv(OUTDIR/'leave_one_out_runs.csv',index=False)
    base_sign=dict(zip(table4['Theme'], np.sign(table4['Rank-biserial'])))
    summary=[]
    for theme in THEMES:
        x=loo[loo['Theme']==theme]
        summary.append({
            'Theme':theme,
            'Direction retained':int((np.sign(x['Rank-biserial'])==base_sign[theme]).sum()),
            'Total leave-one-out runs':len(x),
            'Raw p < .05':int((x['Raw p']<.05).sum()),
            'BH-adjusted p < .05':int((x['BH-adjusted p']<.05).sum())
        })
    pd.DataFrame(summary).to_csv(OUTDIR/'leave_one_out_summary.csv',index=False)
    fig=table4[['Theme','PUC median','PUC Q1','PUC Q3','PrUC median','PrUC Q1','PrUC Q3','BH-adjusted p']].copy()
    fig.to_csv(OUTDIR/'figure1_thematic_profile_data.csv',index=False)
    print('OK: wrote revised Table 4, sensitivity analyses, leave-one-out outputs, and Figure 1 source data.')
if __name__=='__main__': main()

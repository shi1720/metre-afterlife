from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent))
from analyze import read,budget
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'savefig.bbox':'tight'})
colors=['#244c66','#aa673a','#358178','#8f627c','#b8a45a']
def save(fig,name):
 fig.savefig(ROOT/'figures'/f'{name}.pdf');fig.savefig(ROOT/'figures'/f'{name}.png',dpi=180);plt.close(fig)
# Documentary layers, no inferred use rates.
fig,ax=plt.subplots(figsize=(6.8,2.8))
ax.set(xlim=(1958,2001),ylim=(-.55,2.65),yticks=[0,1,2],yticklabels=['Laboratory practice','Authorized realization','Unit definition'],xticks=[1960,1963,1975,1983,1992,1997,2000])
ax.hlines(2,1960,1983,color=colors[1],lw=3);ax.hlines(2,1983,2000,color=colors[0],lw=3)
ax.text(1965,2.12,'Krypton transition',fontsize=9);ax.text(1986,2.12,'Fixed speed of light',fontsize=9)
ax.hlines(1,1963,1997,color=colors[2],lw=3)
for year in [1963,1983,1992,1997]:ax.plot(year,1,'o',color=colors[2])
ax.text(1964,1.14,'Lamp recommendations retained; laser routes added',fontsize=8)
ax.scatter([1992,2000],[0,0],s=45,color=colors[3]);ax.text(1991.4,-.18,'BIPM repairs',ha='right',fontsize=8);ax.text(2000,-.18,'NRC staged upgrades',ha='right',fontsize=8)
ax.axvline(1983,ls='--',color='grey',lw=.8);ax.grid(axis='x',alpha=.15)
fig.tight_layout();save(fig,'authority_layers')
# Assigned uncertainty and conditions: mode-aware labels.
fig,axes=plt.subplots(1,3,figsize=(7.0,2.65),sharey=True)
r=read('radiations.csv')
for ax,key,title in zip(axes,['i633','ch4-cell','ca657'],['Iodine, 633 nm','Methane, 3.39 micrometres','Calcium, 657 nm']):
 a=[x for x in r if x['key']==key];xx=[int(x['year']) for x in a];yy=[float(x['standard_relative']) for x in a]
 ax.plot(xx,yy,'o-',color=colors[0],lw=1.4,label='Assigned regime')
 if key=='ch4-cell':
  b=[x for x in r if x['key']=='ch4-resolved'];ax.plot([int(x['year']) for x in b],[float(x['standard_relative']) for x in b],'^--',color=colors[1],label='Resolved regime')
  ax.legend(fontsize=6.8,frameon=False,loc='lower left')
 ax.set(title=title,yscale='log',xticks=[1983,1992,1997],xlim=(1981,1999),ylim=(3e-13,8e-10));ax.grid(axis='y',alpha=.15);ax.tick_params(axis='x',rotation=45)
axes[0].set_ylabel('Assigned relative standard uncertainty*')
fig.tight_layout();save(fig,'uncertainty_modes')
fig,axes=plt.subplots(1,4,figsize=(7,2.15))
conditions=[('Cell wall (C)',[(16,50),(20,30),(20,30)]),('Cold finger (C)',[(14,16),(14.8,15.2),(14.8,15.2)]),('Power (mW)',[(5,25),(5,15),(5,15)]),('Modulation (MHz)',[(5,7),(5.7,6.3),(5.7,6.3)])]
for ax,(title,intervals) in zip(axes,conditions):
 for i,(lo,hi) in enumerate(intervals):ax.plot([lo,hi],[i,i],lw=4,color=colors[i]);ax.plot([lo,hi],[i,i],'|',color=colors[i])
 ax.set(title=title,yticks=[0,1,2],yticklabels=['1983','1992','1997'],ylim=(2.5,-.5));ax.grid(axis='x',alpha=.15)
fig.tight_layout();save(fig,'iodine_conditions')
fig,ax=plt.subplots(figsize=(6.8,2.7));b=read('nrc_budget.csv');lengths=[10,100,1000];zs=[budget(b,x) for x in lengths];bottom=np.zeros(3)
for g,c in zip(['End effects','Optics','Laser','Thermal','Air'],colors):
 vals=[100*z['variance_shares'][g] for z in zs];ax.bar(range(3),vals,bottom=bottom,label=g,color=c,width=.58);bottom+=vals
ax.set(xticks=range(3),xticklabels=['10 mm','100 mm','1000 mm'],ylabel='Share of reconstructed variance (%)',ylim=(0,100));ax.legend(ncol=5,loc='upper center',bbox_to_anchor=(.5,1.19),frameon=False,fontsize=8)
fig.tight_layout();save(fig,'nrc_variance')

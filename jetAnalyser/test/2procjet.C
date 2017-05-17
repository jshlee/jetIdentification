{

TFile *file = new TFile("jet15.root");
TTree *tree = (TTree *)file->Get("jetAnalyser/jetAnalyser");

int partonId;
float jetpt;
std::vector<float> *dau_jetNum, *dau_ptnId, *dau_charge, *dau_deta, *dau_dphi, *dau_pt;
int all=0;
int draw=0;
double pi=TMath::Pi();
double const maxx=0.4/1;
double const maxy=0.4/1;
int const arnum=16;
char filename[100];
int num,flavour,charge;
double x,y,pt;
double mineta=0.,minphi=0.,maxeta=0.,maxphi=0.;
double maxnpt=0.,maxcpt=0.,maxmul=0.;
double gmaxnpt=0.,gmaxcpt=0.,gmaxmul=0.;
double qmaxnpt=0.,qmaxcpt=0.,qmaxmul=0.;
double sumnpt=0.,sumcpt=0.,summul=0.;
double gsumnpt=0.,gsumcpt=0.,gsummul=0.;
double qsumnpt=0.,qsumcpt=0.,qsummul=0.;
double armu[arnum*2+1][arnum*2+1][3];
double arpt1[arnum*2+1][arnum*2+1][3];
double arde[arnum*2+1][arnum*2+1][3];
double arpt[arnum*2+1][arnum*2+1][3];
double garpt[arnum*2+1][arnum*2+1][3];
double qarpt[arnum*2+1][arnum*2+1][3];
int bbb=arnum*2+1;
double bx=2.*maxx/(2.*arnum+1.);
double by=2.*maxy/(2.*arnum+1.);

tree->SetBranchAddress("partonId",&partonId);
tree->SetBranchAddress("pt",&jetpt);
tree->SetBranchAddress("dau_ptnId",&dau_ptnId);
tree->SetBranchAddress("dau_charge",&dau_charge);
tree->SetBranchAddress("dau_deta",&dau_deta);
tree->SetBranchAddress("dau_dphi",&dau_dphi);
tree->SetBranchAddress("dau_pt",&dau_pt);
ofstream outjet;
outjet.open("pixel/ccdata05_17.csv");
ifstream getsum("pixel/sumdata");
ifstream getmu("pixel/mudata");
ifstream getde("pixel/dedata");
//ofstream outmu;
////outmu.open("pixel/dedata");
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
getmu>>maxcpt>>maxnpt>>maxmul;
getde>>gmaxcpt>>gmaxnpt>>gmaxmul;
armu[i][j][0]=maxnpt;
armu[i][j][1]=maxcpt;
armu[i][j][2]=maxmul;
arde[i][j][0]=gmaxnpt;
arde[i][j][1]=gmaxcpt;
arde[i][j][2]=gmaxmul;
}}
getmu.close();
getde.close();
TCanvas *c1 = new TCanvas("c1","mmmm",800,1600);
c1->Divide(2,4);
for(auto iev = 0; iev < tree->GetEntries(); iev++){
sumnpt=1;sumcpt=1;summul=1;
gsumnpt=1;gsumcpt=1;gsummul=1;
qsumnpt=1;qsumcpt=1;qsummul=1;
tree->GetEntry(iev);
flavour=partonId;
for(int th=0;th<8;th++){
if(th!=0){break;}
if(all==0){
for(int i=0;i<bbb;i++){
for(int j=0;j<bbb;j++){
for(int k=0;k<3;k++){
arpt[i][j][k]=0.;
}
}
}
}
//getsum>>sumnpt>>sumcpt>>summul>>gsumnpt>>gsumcpt>>gsummul>>qsumnpt>>qsumcpt>>qsummul;
for(int di = 0; di<dau_deta->size(); ++di){//++i??
x=(*dau_deta)[di];
y=(*dau_dphi)[di];
pt=(*dau_pt)[di];
charge=(*dau_charge)[di];
//cout<<(*dau_deta)[di]<<endl;
x=cos(th*pi/4)*x-sin(th*pi/4)*y;
y=sin(th*pi/4)*x+cos(th*pi/4)*y;
if(x<0. && x<mineta){mineta=x;}
if(x>0. && x>maxeta){maxeta=x;}
if(y<0. && y<minphi){minphi=y;}
if(y>0. && y>maxphi){maxphi=y;}
for(int i=0;i<=arnum;i++){
	if(abs(x)>=bx*(i-0.5) && abs(x)<bx*(i+0.5)){
		for(int j=0;j<=arnum;j++){
			if(abs(y)>=by*(j-0.5) && abs(y)<by*(j+0.5)){
				if(x>=0.){
					if(y>=0.){
						if(charge==0){
							arpt[arnum+i][arnum+j][0]+=pt/sumnpt;
							arpt1[arnum+i][arnum+j][0]+=pt/sumnpt;
//							sumnpt+=pt;
							//arpt[arnum+i][arnum+j][2]+=1;
							if(flavour==21){
//								garpt[arnum+i][arnum+j][0]+=pt/gsumnpt;
//								gsumnpt+=pt;
							}		
							else{
//								qarpt[arnum+i][arnum+j][0]+=pt/qsumnpt;
//								qsumnpt+=pt;
							}
						}
						else{
							arpt[arnum+i][arnum+j][1]+=pt/sumcpt;
							arpt[arnum+i][arnum+j][2]+=1/summul;
							arpt1[arnum+i][arnum+j][1]+=pt/sumcpt;
							arpt1[arnum+i][arnum+j][2]+=1/summul;
//							sumcpt+=pt;
//							summul+=1;
							if(flavour==21){
//								garpt[arnum+i][arnum+j][1]+=pt/gsumcpt;
//								garpt[arnum+i][arnum+j][2]+=1/gsummul;
//								gsumcpt+=pt;
//								gsummul+=1;
							}
							else{
//								qarpt[arnum+i][arnum+j][1]+=pt/qsumcpt;
//								qarpt[arnum+i][arnum+j][2]+=1/qsummul;
//								qsumcpt+=pt;
//								qsummul+=1;
							}
						}
					}
					else{
						if(charge==0){
							arpt[arnum+i][arnum-j][0]+=pt/sumnpt;
							arpt1[arnum+i][arnum-j][0]+=pt/sumnpt;
//							sumnpt+=pt;
							if(flavour==21){
//								garpt[arnum+i][arnum-j][0]+=pt/gsumnpt;
//								gsumnpt+=pt;
							}
							else{
//								qarpt[arnum+i][arnum-j][0]+=pt/qsumnpt;
//								qsumnpt+=pt;
							}
							//arpt[arnum+i][arnum-j][2]+=1;
						}
						else{
							arpt[arnum+i][arnum-j][1]+=pt/sumcpt;
							arpt[arnum+i][arnum-j][2]+=1/summul;
							arpt1[arnum+i][arnum-j][1]+=pt/sumcpt;
							arpt1[arnum+i][arnum-j][2]+=1/summul;
//							sumcpt+=pt;
//							summul+=1;
							if(flavour==21){
//								garpt[arnum+i][arnum-j][1]+=pt/gsumcpt;
//								garpt[arnum+i][arnum-j][2]+=1/gsummul;
//								gsumcpt+=pt;
//								gsummul+=1;
							}
							else{
//								qarpt[arnum+i][arnum-j][1]+=pt/qsumcpt;
//								qarpt[arnum+i][arnum-j][2]+=1/qsummul;
//								qsumcpt+=pt;
//								qsummul+=1;
							}
						}
					}
				}
				else{
					if(y>=0.){
						if(charge==0){
							arpt[arnum-i][arnum+j][0]+=pt/sumnpt;
							arpt1[arnum-i][arnum+j][0]+=pt/sumnpt;
//							sumnpt+=pt;
							//arpt[arnum-i][arnum+j][2]+=1;
							if(flavour==21){
//								garpt[arnum-i][arnum+j][0]+=pt/gsumnpt;
//								gsumnpt+=pt;
							}
							else{
//								qarpt[arnum-i][arnum+j][0]+=pt/qsumnpt;
//								qsumnpt+=pt;
							}
						}
						else{
							arpt[arnum-i][arnum+j][1]+=pt/sumcpt;
							arpt[arnum-i][arnum+j][2]+=1/summul;
							arpt1[arnum-i][arnum+j][1]+=pt/sumcpt;
							arpt1[arnum-i][arnum+j][2]+=1/summul;
//							sumcpt+=pt;
//							summul+=1;
							if(flavour==21){
//								garpt[arnum-i][arnum+j][1]+=pt/gsumcpt;
//								garpt[arnum-i][arnum+j][2]+=1/gsummul;
//								gsumcpt+=pt;
//								gsummul+=1;
							}
							else{
//								qarpt[arnum-i][arnum+j][1]+=pt/qsumcpt;
//								qarpt[arnum-i][arnum+j][2]+=1/qsummul;
//								qsumcpt+=pt;
//								qsummul+=1;
							}
						}
					}
					else{
						if(charge==0){
							arpt[arnum-i][arnum-j][0]+=pt/sumnpt;
							arpt1[arnum-i][arnum-j][0]+=pt/sumnpt;
//							sumnpt+=pt;
							//arpt[arnum-i][arnum-j][2]+=1;
							if(flavour==21){
//								garpt[arnum-i][arnum-j][0]+=pt/gsumnpt;
//								gsumnpt+=pt;
							}
							else{
//								qarpt[arnum-i][arnum-j][0]+=pt/qsumnpt;
//								qsumnpt+=pt;
							}
						}
						else{
							arpt[arnum-i][arnum-j][1]+=pt/sumcpt;
							arpt[arnum-i][arnum-j][2]+=1/summul;
							arpt1[arnum-i][arnum-j][1]+=pt/sumcpt;
							arpt1[arnum-i][arnum-j][2]+=1/summul;
//							sumcpt+=pt;
//							summul+=1;
							if(flavour==21){
//								garpt[arnum-i][arnum-j][1]+=pt/gsumcpt;
//								garpt[arnum-i][arnum-j][2]+=1/gsummul;
//								gsumcpt+=pt;
//								gsummul+=1;
							}
							else{
//								qarpt[arnum-i][arnum-j][1]+=pt/qsumcpt;
//								qarpt[arnum-i][arnum-j][2]+=1/qsummul;
//								qsumcpt+=pt;
//								qsummul+=1;
							}
						}
					}
				}
			}
		}
	}
}
}

for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
/*arpt[i][j][0]=arpt[i][j][0]-armu[i][j][0];
arpt[i][j][1]=arpt[i][j][1]-armu[i][j][1];
arpt[i][j][2]=arpt[i][j][2]-armu[i][j][2];*/
/*arpt1[i][j][0]=arpt1[i][j][0]-armu[i][j][0];
arpt1[i][j][1]=arpt1[i][j][1]-armu[i][j][1];
arpt1[i][j][2]=arpt1[i][j][2]-armu[i][j][2];*/
/*arpt[i][j][0]=arpt[i][j][0]/(arde[i][j][0]+0.00001);
arpt[i][j][1]=arpt[i][j][1]/(arde[i][j][1]+0.00001);
arpt[i][j][2]=arpt[i][j][2]/(arde[i][j][2]+0.00001);*/
/*if(flavour==21){
garpt[i][j][0]=garpt[i][j][0]-armu[i][j][0];
garpt[i][j][1]=garpt[i][j][1]-armu[i][j][1];
garpt[i][j][2]=garpt[i][j][2]-armu[i][j][2];
}
else{
qarpt[i][j][0]=qarpt[i][j][0]-armu[i][j][0];
qarpt[i][j][1]=qarpt[i][j][1]-armu[i][j][1];
qarpt[i][j][2]=qarpt[i][j][2]-armu[i][j][2];
}*/
/*arde[i][j][0]=arde[i][j][0]+arpt1[i][j][0]*arpt1[i][j][0];
arde[i][j][1]=arde[i][j][1]+arpt1[i][j][1]*arpt1[i][j][1];
arde[i][j][2]=arde[i][j][2]+arpt1[i][j][2]*arpt1[i][j][2];*/
}}

if(draw==0){
outjet<<flavour<<","<<jetpt<<endl;
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
if(i==0&&j==0){
outjet<<arpt[i][j][1]<<","<<arpt[i][j][0]<<","<<arpt[i][j][2];
}
else{
outjet<<","<<arpt[i][j][1]<<","<<arpt[i][j][0]<<","<<arpt[i][j][2];
}
}
}
outjet<<endl;
}

}
//outsum<<sumnpt<<"\t"<<sumcpt<<"\t"<<summul<<"\t"<<gsumnpt<<"\t"<<gsumcpt<<"\t"<<gsummul<<"\t"<<qsumnpt<<"\t"<<qsumcpt<<"\t"<<qsummul<<endl;



}
maxnpt=0.;maxcpt=0.;maxmul=0.;
gmaxnpt=0.;gmaxcpt=0.;gmaxmul=0.;
qmaxnpt=0.;qmaxcpt=0.;qmaxmul=0.;
/*sumnpt=0.;sumcpt=0.;summul=0.;
gsumnpt=0.;gsumcpt=0.;gsummul=0.;
qsumnpt=0.;qsumcpt=0.;qsummul=0.;
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
sumnpt+=arpt[i][j][0];
sumcpt+=arpt[i][j][1];
summul+=arpt[i][j][2];
gsumnpt+=garpt[i][j][0];
gsumcpt+=garpt[i][j][1];
gsummul+=garpt[i][j][2];
qsumnpt+=qarpt[i][j][0];
qsumcpt+=qarpt[i][j][1];
qsummul+=qarpt[i][j][2];
}}*/
//cout<<gsumnpt<<endl;
/*for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
arpt[i][j][0]=arpt[i][j][0]/(arde[i][j][0]+0.00001);
arpt[i][j][1]=arpt[i][j][1]/(arde[i][j][1]+0.00001);
arpt[i][j][2]=arpt[i][j][2]/(arde[i][j][2]+0.00001);
garpt[i][j][0]=garpt[i][j][0]/(arde[i][j][0]+0.00001);
garpt[i][j][1]=garpt[i][j][1]/(arde[i][j][1]+0.00001);
garpt[i][j][2]=garpt[i][j][2]/(arde[i][j][2]+0.00001);
qarpt[i][j][0]=qarpt[i][j][0]/(arde[i][j][0]+0.00001);
qarpt[i][j][1]=qarpt[i][j][1]/(arde[i][j][1]+0.00001);
qarpt[i][j][2]=qarpt[i][j][2]/(arde[i][j][2]+0.00001);*/
/*arde[i][j][0]=sqrt((arde[i][j][0]/tree->GetEntries())-(armu[i][j][0]*armu[i][j][0]));
arde[i][j][1]=sqrt((arde[i][j][1]/tree->GetEntries())-(armu[i][j][1]*armu[i][j][1]));
arde[i][j][2]=sqrt((arde[i][j][2]/tree->GetEntries())-(armu[i][j][2]*armu[i][j][2]));*/
/*if(maxnpt<arpt[i][j][0]){maxnpt=arpt[i][j][0];}
if(maxcpt<arpt[i][j][1]){maxcpt=arpt[i][j][1];}
if(maxmul<arpt[i][j][2]){maxmul=arpt[i][j][2];}
if(gmaxnpt<garpt[i][j][0]){gmaxnpt=garpt[i][j][0];}
if(gmaxcpt<garpt[i][j][1]){gmaxcpt=garpt[i][j][1];}
if(gmaxmul<garpt[i][j][2]){gmaxmul=garpt[i][j][2];}
if(qmaxnpt<qarpt[i][j][0]){qmaxnpt=qarpt[i][j][0];}
if(qmaxcpt<qarpt[i][j][1]){qmaxcpt=qarpt[i][j][1];}
if(qmaxmul<qarpt[i][j][2]){qmaxmul=qarpt[i][j][2];}
}}*/
if(draw==1){
float bb1=1./bbb;
for(int j=0;j<bbb;j++){
for(int i=0;i<bbb;i++){
//cout<<floor(arpt[i][j][2])<<" ";
TBox *b= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *c= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *n= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *m= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
Float_t nptcol=Float_t(255.*(qarpt[i][j][0]/qmaxnpt));
Float_t cptcol=Float_t(255.*(qarpt[i][j][1]/qmaxcpt));
Float_t mulcol=Float_t(255.*(qarpt[i][j][2]/qmaxmul));
//if(i==16 && j==16){ b->SetFillColor(TColor::GetColor(ptcolor,ptcolor,0*ptcolor));}
b->SetFillColor(TColor::GetColor(int(cptcol),int(nptcol),int(mulcol)));
c->SetFillColor(TColor::GetColor(int(cptcol),int(nptcol*0),int(mulcol*0)));
n->SetFillColor(TColor::GetColor(int(cptcol*0),int(nptcol),int(mulcol*0)));
m->SetFillColor(TColor::GetColor(int(cptcol*0),int(nptcol*0),int(mulcol)));
//b->SetFillColor(TColor::GetColor(i,j,i));
c1->cd(1);
b->Draw();
c1->cd(3);
c->Draw();
c1->cd(5);
n->Draw();
c1->cd(7);
m->Draw();
}
//cout<<endl;
}
for(int j=0;j<bbb;j++){
for(int i=0;i<bbb;i++){
//cout<<floor(arpt[i][j][2])<<" ";
TBox *b= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *c= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *n= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *m= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
Float_t nptcol=Float_t(255.*(garpt[i][j][0]/gmaxnpt));
Float_t cptcol=Float_t(255.*(garpt[i][j][1]/gmaxcpt));
Float_t mulcol=Float_t(255.*(garpt[i][j][2]/gmaxmul));
//if(i==16 && j==16){ b->SetFillColor(TColor::GetColor(ptcolor,ptcolor,0*ptcolor));}
b->SetFillColor(TColor::GetColor(int(cptcol),int(nptcol),int(mulcol)));
c->SetFillColor(TColor::GetColor(int(cptcol),int(nptcol*0),int(mulcol*0)));
n->SetFillColor(TColor::GetColor(int(cptcol*0),int(nptcol),int(mulcol*0)));
m->SetFillColor(TColor::GetColor(int(cptcol*0),int(nptcol*0),int(mulcol)));
//b->SetFillColor(TColor::GetColor(i,j,i));
c1->cd(2);
b->Draw();
c1->cd(4);
c->Draw();
c1->cd(6);
n->Draw();
c1->cd(8);
m->Draw();
}
//cout<<endl;
}

}
/*
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
if(i==0&&j==0){
outjet<<qarpt[i][j][1]<<","<<qarpt[i][j][0]<<","<<qarpt[i][j][2];
}
else{
outjet<<","<<qarpt[i][j][1]<<","<<qarpt[i][j][0]<<","<<qarpt[i][j][2];
}
}
}
outjet<<endl;
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
if(i==0&&j==0){
outjet<<garpt[i][j][1]<<","<<garpt[i][j][0]<<","<<garpt[i][j][2];
}
else{
outjet<<","<<garpt[i][j][1]<<","<<garpt[i][j][0]<<","<<garpt[i][j][2];
}
}
}
outjet<<endl;
*/
cout<<"mineta "<<mineta<<"\t"<<"maxeta "<<maxeta<<"\t"<<"minphi "<<minphi<<"\t"<<"maxphi "<<maxphi<<endl;
cout<<"maxnpt "<<maxnpt<<"\t"<<"gsumnpt"<<gsumnpt<<endl;

/*for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
if(i==0&&j==0){
outmu<<arpt[i][j][1]/tree->GetEntries()<<","<<arpt[i][j][0]/tree->GetEntries()<<","<<arpt[i][j][2]/tree->GetEntries();
}
else{
outmu<<","<<arpt[i][j][1]/tree->GetEntries()<<","<<arpt[i][j][0]/tree->GetEntries()<<","<<arpt[i][j][2]/tree->GetEntries();
}
}
}*/

/*for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
if(i==0&&j==0){
outmu<<arde[i][j][1]<<","<<arde[i][j][0]<<","<<arde[i][j][2];
}
else{
outmu<<","<<arde[i][j][1]<<","<<arde[i][j][0]<<","<<arde[i][j][2];
}
}
}*/
//outmu.close();
outjet.close();
getsum.close();
}

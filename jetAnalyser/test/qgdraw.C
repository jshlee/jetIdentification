{
/*#include <iostream>
#include <fstream>
#include "TCanvas.h"
#include "TColor.h"
#include "TH2.h"
#include "THStack.h"

using namespace std;
*/
int all=1;
double const maxx=0.4;
double const maxy=0.4;
//double const maxx=0.665/2;
//double const maxy=0.542/2;
int const arnum=32;//even number
int num,flavour,buflav,chek;
double x,y,pt;
int charge;
double mineta=0,minphi=0,maxeta=0,maxphi=0;
double maxnpt=0,maxcpt=0,maxmul=0;
double minnpt=0,mincpt=0,minmul=0;
double arpt[arnum*2+1][arnum*2+1][3];
double garpt[arnum*2+1][arnum*2+1][3];
int bbb=arnum*2+1;
double bx=2.*maxx/(2.*arnum+1.);
double by=2.*maxy/(2.*arnum+1.);
string dummy;
ifstream file ("data.txt");
getline(file,dummy);
TCanvas *c1 = new TCanvas("c1","mmmm",1600,800);
//TCanvas *c2 = new TCanvas("c2","mmmm",800,800);
int ccc=1;
c1->Divide(4,2);
TH2F *h1 = new TH2F("h1","h1",33,-maxx,maxx,33,-maxy,maxy);
for(int nnn=-1;nnn<ccc*ccc;nnn++){
for(int i=0;i<bbb;i++){
for(int j=0;j<bbb;j++){
for(int k=0;k<3;k++){
arpt[i][j][k]=0.;
garpt[i][j][k]=0.;
}
}
}
while (file >> num >> flavour >> x >> y >> pt >> charge){
if(x<0 && x<mineta){mineta=x;}
if(x>0 && x>maxeta){maxeta=x;}
if(y<0 && y<minphi){minphi=y;}
if(y>0 && y>maxphi){maxphi=y;}
if(all==0 && num!=nnn){chek=1;break;}
if(chek==1){buflav=flavour;chek=0;}
if(flavour==0){continue;}
for(int i=0;i<=arnum;i++){
if(abs(x)>=bx*(i-0.5) && abs(x)<bx*(i+0.5)){
for(int j=0;j<=arnum;j++){
if(abs(y)>=by*(j-0.5) && abs(y)<by*(j+0.5)){
//--
if(flavour!=21){
if(x>=0){
if(y>=0){
if(charge==0){
arpt[arnum+i][arnum+j][0]+=pt;
//arpt[arnum+i][arnum+j][2]+=1;
}
else{
arpt[arnum+i][arnum+j][1]+=pt;
arpt[arnum+i][arnum+j][2]+=1;
}
}
else{
if(charge==0){
arpt[arnum+i][arnum-j][0]+=pt;
//arpt[arnum+i][arnum-j][2]+=1;
}
else{
arpt[arnum+i][arnum-j][1]+=pt;
arpt[arnum+i][arnum-j][2]+=1;
}
}
}
else{
if(y>=0){
if(charge==0){
arpt[arnum-i][arnum+j][0]+=pt;
//arpt[arnum-i][arnum+j][2]+=1;
}
else{
arpt[arnum-i][arnum+j][1]+=pt;
arpt[arnum-i][arnum+j][2]+=1;
}
}
else{
if(charge==0){
arpt[arnum-i][arnum-j][0]+=pt;
//arpt[arnum-i][arnum-j][2]+=1;
}
else{
arpt[arnum-i][arnum-j][1]+=pt;
arpt[arnum-i][arnum-j][2]+=1;
}
}
}
}
if(flavour==21){
if(x>=0){
if(y>=0){
if(charge==0){
garpt[arnum+i][arnum+j][0]+=pt;
//arpt[arnum+i][arnum+j][2]+=1;
}
else{
garpt[arnum+i][arnum+j][1]+=pt;
garpt[arnum+i][arnum+j][2]+=1;
}
}
else{
if(charge==0){
garpt[arnum+i][arnum-j][0]+=pt;
//arpt[arnum+i][arnum-j][2]+=1;
}
else{
garpt[arnum+i][arnum-j][1]+=pt;
garpt[arnum+i][arnum-j][2]+=1;
}
}
}
else{
if(y>=0){
if(charge==0){
garpt[arnum-i][arnum+j][0]+=pt;
//arpt[arnum-i][arnum+j][2]+=1;
}
else{
garpt[arnum-i][arnum+j][1]+=pt;
garpt[arnum-i][arnum+j][2]+=1;
}
}
else{
if(charge==0){
garpt[arnum-i][arnum-j][0]+=pt;
//arpt[arnum-i][arnum-j][2]+=1;
}
else{
garpt[arnum-i][arnum-j][1]+=pt;
garpt[arnum-i][arnum-j][2]+=1;
}
}
}
}
//--
}

}
}
}

//TBox *b = new TBox(j/33,(33-1-i)/33,(j+1)/33,(33-i)/33);
//double col
//h1->Fill(x,y);
//cout<<"x "<< x<<" "<<"y "<<y<<" "<<"pt "<<pt<<" "<<"charge "<<charge<<endl;

}
if(all==0 && nnn==-1){continue;}
maxnpt=0.;maxcpt=0.;maxmul=0.;
minnpt=0.;mincpt=0.;minmul=0.;
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
if(maxnpt<arpt[i][j][0]){maxnpt=arpt[i][j][0];}
if(maxcpt<arpt[i][j][1]){maxcpt=arpt[i][j][1];}
if(maxmul<arpt[i][j][2]){maxmul=arpt[i][j][2];}
if(minnpt>arpt[i][j][0]){minnpt=arpt[i][j][0];}
if(mincpt>arpt[i][j][1]){mincpt=arpt[i][j][1];}
if(minmul>arpt[i][j][2]){minmul=arpt[i][j][2];}

}}
//if(all==1){c1->cd(1);}
//else{c1->cd(nnn+1);}

float bb1=1./bbb;
for(int j=0;j<bbb;j++){
for(int i=0;i<bbb;i++){
//cout<<floor(arpt[i][j][2])<<" ";
TBox *b= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *c= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *n= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *m= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
Float_t nptcol=Float_t(255.*((arpt[i][j][0]-minnpt)/(maxnpt-minnpt)));
Float_t cptcol=Float_t(255.*((arpt[i][j][1]-mincpt)/(maxcpt-mincpt)));
Float_t mulcol=Float_t(255.*((arpt[i][j][2]-minmul)/(maxmul-minmul)));
//cout<<nptcol+cptcol<<endl;
//if(i==16 && j==16){ b->SetFillColor(TColor::GetColor(ptcolor,ptcolor,0*ptcolor));}
//b->SetFillColor(TColor::GetColor(255.-(nptcol+mulcol)/2.,255.-(cptcol+mulcol)/2.,255.-(nptcol+cptcol)/2.));
b->SetFillColor(TColor::GetColor(int(255.-1.*(nptcol+mulcol)/2.),int(255.-(cptcol+mulcol)/2),int(255.-(nptcol+cptcol)/2.)));
//b->SetFillColor(TColor::GetColor(cptcol,nptcol,mulcol));
//c->SetFillColor(TColor::GetColor(cptcol,0.,0.));
c->SetFillColor(TColor::GetColor(255,255.-cptcol,255.-cptcol));
n->SetFillColor(TColor::GetColor(255.-nptcol,255,255.-nptcol));
//n->SetFillColor(TColor::GetColor(0.,nptcol,0.));
//if(nptcol>0){cout<<255.-nptcol<<endl;}
//m->SetFillColor(TColor::GetColor(0.,0.,mulcol));
m->SetFillColor(TColor::GetColor(255.-mulcol,255.-mulcol,255));
//b->SetFillColor(TColor::GetColor(i,j,i));
c1->cd(1);
b->Draw();
c1->cd(2);
c->Draw();
c1->cd(3);
n->Draw();
c1->cd(4);
m->Draw();
}
//cout<<endl;
}
//cout<<buflav<<" "<<maxcpt<<" "<<maxmul<<endl;

//gluon
if(all==0 && nnn==-1){continue;}
maxnpt=0.;maxcpt=0.;maxmul=0.;
minnpt=0.;mincpt=0.;minmul=0.;
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
if(maxnpt<garpt[i][j][0]){maxnpt=garpt[i][j][0];}
if(maxcpt<garpt[i][j][1]){maxcpt=garpt[i][j][1];}
if(maxmul<garpt[i][j][2]){maxmul=garpt[i][j][2];}
if(minnpt>garpt[i][j][0]){minnpt=garpt[i][j][0];}
if(mincpt>garpt[i][j][1]){mincpt=garpt[i][j][1];}
if(minmul>garpt[i][j][2]){minmul=garpt[i][j][2];}

}}
//if(all==1){c1->cd(1);}
//else{c1->cd(nnn+1);}
//float bb1=1./bbb;
for(int j=0;j<bbb;j++){
for(int i=0;i<bbb;i++){
//cout<<floor(arpt[i][j][2])<<" ";
TBox *b= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *c= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *n= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
TBox *m= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
Float_t nptcol=Float_t(255.*((garpt[i][j][0]-minnpt)/(maxnpt-minnpt)));
Float_t cptcol=Float_t(255.*((garpt[i][j][1]-mincpt)/(maxcpt-mincpt)));
Float_t mulcol=Float_t(255.*((garpt[i][j][2]-minmul)/(maxmul-minmul)));
//if(i==16 && j==16){ b->SetFillColor(TColor::GetColor(ptcolor,ptcolor,0*ptcolor));}
//if(i==0 && j==0){ b->SetFillColor(TColor::GetColor(0,255,0));}
//else{ b->SetFillColor(TColor::GetColor(cptcol,nptcol,mulcol));}
b->SetFillColor(TColor::GetColor(int(255.-1.*(nptcol+mulcol)/2.),int(255.-(cptcol+mulcol)/2),int(255.-(nptcol+cptcol)/2.)));
//c->SetFillColor(TColor::GetColor(cptcol,0.,0.));
//n->SetFillColor(TColor::GetColor(0.,nptcol,0.));
//m->SetFillColor(TColor::GetColor(0.,0.,mulcol));
c->SetFillColor(TColor::GetColor(255,255.-cptcol,255.-cptcol));
n->SetFillColor(TColor::GetColor(255.-nptcol,255,255.-nptcol));
m->SetFillColor(TColor::GetColor(255.-mulcol,255.-mulcol,255));
//b->SetFillColor(TColor::GetColor(i,j,i));
c1->cd(5);
b->Draw();
c1->cd(6);
c->Draw();
c1->cd(7);
n->Draw();
c1->cd(8);
m->Draw();
}
//cout<<endl;
}


if(all==1){break;}
}

/*tfile=new TFile("result.root","recreate");
c1->Write("result.root");
tfile->Close();*/
/*TBox *d= new TBox(.10,.10,.20,.20);
d->SetFillColor(TColor::GetColor(55,144,255));
d->Draw();*/
//c2->cd(1);
//h1->Draw("colz");
cout<<"mineta "<<mineta<<"\t"<<"maxeta "<<maxeta<<"\t"<<"minphi "<<minphi<<"\t"<<"maxphi "<<maxphi<<endl;
cout<<"maxnpt "<<maxnpt<<endl;
//cout<<dummy<<endl;
}

{
/*#include <iostream>
#include <fstream>
#include "TCanvas.h"
#include "TColor.h"
#include "TH2.h"
#include "THStack.h"

using namespace std;
*/
double const maxx=0.78;
double const maxy=0.56;
int const arnum=16;//even
int num,flavour;
double x,y,pt,charge;
double mineta=0;
double minphi=0;
double maxeta=0;
double maxphi=0;
double maxpt=0;
double arpt[arnum*2+1][arnum*2+1];
int bbb=arnum*2+1;
double bx=2*maxx/(2*arnum+1);
double by=2*maxy/(2*arnum+1);
string dummy;
ifstream file ("array.txt");
getline(file,dummy);
TCanvas *c1 = new TCanvas("c1","mmmm",1000,1000);
int ccc=7;
c1->Divide(ccc,ccc);
//TH2F *h1 = new TH2F("h1","h1",20,-maxx,maxx,20,-maxy,maxy);
for(int nnn=0;nnn<ccc*ccc;nnn++){
for(int i=0;i<bbb;i++){
for(int j=0;j<bbb;j++){
arpt[i][j]=0;
}
}
while (file >> num >> flavour >> x >> y >> pt >> charge){
if(x<0 && x<mineta){mineta=x;}
if(x>0 && x>maxeta){maxeta=x;}
if(y<0 && y<minphi){minphi=y;}
if(y>0 && y>maxphi){maxphi=y;}
if(num!=nnn){break;}
for(int i=0;i<=arnum;i++){
if(abs(x)>=bx*i && abs(x)<bx*(i+1)){
if(x>=0){
for(int j=0;j<=arnum;j++){
if(abs(y)>=by*j && abs(y)<by*(i+1)){
if(y>=0){
arpt[arnum+i][arnum+j]+=pt;
}
else{
arpt[arnum+i][arnum-j]+=pt;
}
}
}
}
else{
for(int j=0;j<=arnum;j++){
if(abs(y)>=by*j && abs(y)<by*(i+1)){
if(y>=0){
arpt[arnum-i][arnum+j]+=pt;
}
else{
arpt[arnum-i][arnum-j]+=pt;
}
}
}
}
}
}

//TBox *b = new TBox(j/33,(33-1-i)/33,(j+1)/33,(33-i)/33);
//double col
//h1->Fill(x,y);
//cout<<"x "<< x<<" "<<"y "<<y<<" "<<"pt "<<pt<<" "<<"charge "<<charge<<endl;
}
maxpt=0;
for(int j=0;j<bbb;j++){
for(int i=0;i<bbb;i++){
if(maxpt<arpt[i][j]){
maxpt=arpt[i][j];}
}}
c1->cd(nnn+1);
float bb1=1./bbb;
for(int j=0;j<bbb;j++){
for(int i=0;i<bbb;i++){
//cout<<floor(arpt[i][j])<<"\t";
TBox *b= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
Float_t ptcolor=Float_t(255*arpt[i][j]/maxpt);
if(i==16 && j==16){ b->SetFillColor(TColor::GetColor(ptcolor,0*ptcolor,ptcolor));}
else{ b->SetFillColor(TColor::GetColor(ptcolor,ptcolor,ptcolor));}
//b->SetFillColor(TColor::GetColor(i,j,i));
b->Draw();
}
//cout<<endl;
}
cout<<flavour<<endl;
}
/*tfile=new TFile("result.root","recreate");
c1->Write("result.root");
tfile->Close();*/
/*TBox *d= new TBox(.10,.10,.20,.20);
d->SetFillColor(TColor::GetColor(55,144,255));
d->Draw();*/
//c1->cd(1);
//ih1->Draw("colz");
cout<<"mineta "<<mineta<<"\t"<<"maxeta "<<maxeta<<"\t"<<"minphi "<<minphi<<"\t"<<"maxphi "<<maxphi<<endl;
cout<<"maxpt "<<maxpt<<endl;
//cout<<dummy<<endl;
}

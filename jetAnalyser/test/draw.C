{
/*#include <iostream>
#include <fstream>
#include "TCanvas.h"
#include "TColor.h"
#include "TH2.h"
#include "THStack.h"

using namespace std;
*/
int all=0;
int draw=1;
int ccc=10;
double const maxx=0.665/2;
double const maxy=0.542/2;
int const arnum=16;//even number
int num,flavour,buflav,chek;
double x,y,pt;
int charge;
char filename[100];
double mineta=0,minphi=0,maxeta=0,maxphi=0;
double maxnpt=0,maxcpt=0,maxmul=0;
double arpt[arnum*2+1][arnum*2+1][3];
int bbb=arnum*2+1;
double bx=2.*maxx/(2.*arnum+1.);
double by=2.*maxy/(2.*arnum+1.);
int exd=0;
string dummy;
ifstream file ("array.txt");
ofstream fout;
getline(file,dummy);
if(draw==1){
TCanvas *c1 = new TCanvas("c1","mmmm",800,800);
//TCanvas *c2 = new TCanvas("c2","mmmm",800,800);
c1->Divide(ccc,ccc);}
//TH2F *h1 = new TH2F("h1","h1",33,-maxx,maxx,33,-maxy,maxy);
for(int nnn=-1;nnn<ccc*ccc;nnn++){
for(int i=0;i<bbb;i++){
for(int j=0;j<bbb;j++){
for(int k=0;k<3;k++){
arpt[i][j][k]=0.;
}
}
}
if(exd==1){break;}
while (file >> num >> flavour >> x >> y >> pt >> charge){
if(num==-1){exd=1;break;}
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
if(x>=0){
if(y>=0){
if(charge==0){arpt[arnum+i][arnum+j][0]+=pt;
//arpt[arnum+i][arnum+j][2]+=1;
}
else{arpt[arnum+i][arnum+j][1]+=pt;
arpt[arnum+i][arnum+j][2]+=1;
}
}
else{
if(charge==0){arpt[arnum+i][arnum-j][0]+=pt;
//arpt[arnum+i][arnum-j][2]+=1;
}
else{arpt[arnum+i][arnum-j][1]+=pt;
arpt[arnum+i][arnum-j][2]+=1;
}
}
}
else{
if(y>=0){
if(charge==0){arpt[arnum-i][arnum+j][0]+=pt;
//arpt[arnum-i][arnum+j][2]+=1;
}
else{arpt[arnum-i][arnum+j][1]+=pt;
arpt[arnum-i][arnum+j][2]+=1;
}
}
else{
if(charge==0){arpt[arnum-i][arnum-j][0]+=pt;
//arpt[arnum-i][arnum-j][2]+=1;
}
else{arpt[arnum-i][arnum-j][1]+=pt;
arpt[arnum-i][arnum-j][2]+=1;
}
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
if(draw==1){
if(all==0 && nnn==-1){continue;}
maxnpt=0.;
maxcpt=0.;
maxmul=0.;
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
if(maxnpt<arpt[i][j][0]){maxnpt=arpt[i][j][0];}
if(maxcpt<arpt[i][j][1]){maxcpt=arpt[i][j][1];}
if(maxmul<arpt[i][j][2]){maxmul=arpt[i][j][2];}

}}
if(all==1){c1->cd(1);}
else{c1->cd(nnn+1);}

float bb1=1./bbb;
for(int j=0;j<bbb;j++){
for(int i=0;i<bbb;i++){
//cout<<floor(arpt[i][j][2])<<" ";
TBox *b= new TBox(i*bb1,j*bb1,(i+1)*bb1,(j+1)*bb1);
Float_t nptcol=Float_t(255.*(arpt[i][j][0]/maxnpt));
Float_t cptcol=Float_t(255.*(arpt[i][j][1]/maxcpt));
Float_t mulcol=Float_t(255.*(arpt[i][j][2]/maxmul));
//if(i==16 && j==16){ b->SetFillColor(TColor::GetColor(ptcolor,ptcolor,0*ptcolor));}
if(i==0 && j==0 && buflav==21){ b->SetFillColor(TColor::GetColor(100,100,100));}
else{ b->SetFillColor(TColor::GetColor(cptcol,nptcol,mulcol));}
//b->SetFillColor(TColor::GetColor(i,j,i));
b->Draw();
}
//cout<<endl;
}

}
sprintf(filename,"pixel/jet_%d",nnn);
fout.open(filename);
fout<<buflav<<endl;
for(int j=0;j<bbb;j++){for(int i=0;i<bbb;i++){
fout<<"("<<arpt[i][j][0]<<","<<arpt[i][j][1]<<","<<arpt[i][j][2]<<")";
fout<<"\t";}
fout<<"\n";}

fout.close();
cout<<buflav<<" "<<maxcpt<<" "<<num<<endl;
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
file.close();
}

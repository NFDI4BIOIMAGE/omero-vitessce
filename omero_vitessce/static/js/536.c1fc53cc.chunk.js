"use strict";(self.webpackChunkomero_vitessce=self.webpackChunkomero_vitessce||[]).push([[536],{536:(e,n,t)=>{t.r(n),t.d(n,{default:()=>k});var s=t(583);t(43),t(950);const r=new Int32Array([0,1,8,16,9,2,3,10,17,24,32,25,18,11,4,5,12,19,26,33,40,48,41,34,27,20,13,6,7,14,21,28,35,42,49,56,57,50,43,36,29,22,15,23,30,37,44,51,58,59,52,45,38,31,39,46,53,60,61,54,47,55,62,63]),o=4017,a=799,c=3406,i=2276,l=1567,f=3784,h=5793,u=2896;function m(e,n){let t=0;const s=[];let r=16;for(;r>0&&!e[r-1];)--r;s.push({children:[],index:0});let o,a=s[0];for(let c=0;c<r;c++){for(let r=0;r<e[c];r++){for(a=s.pop(),a.children[a.index]=n[t];a.index>0;)a=s.pop();for(a.index++,s.push(a);s.length<=c;)s.push(o={children:[],index:0}),a.children[a.index]=o.children,a=o;t++}c+1<r&&(s.push(o={children:[],index:0}),a.children[a.index]=o.children,a=o)}return s[0].children}function b(e,n,t,s,o,a,c,i,l){const{mcusPerLine:f,progressive:h}=t,u=n;let m=n,b=0,d=0;function p(){if(d>0)return d--,b>>d&1;if(b=e[m++],255===b){const n=e[m++];if(n)throw new Error(`unexpected marker: ${(b<<8|n).toString(16)}`)}return d=7,b>>>7}function k(e){let n,t=e;for(;null!==(n=p());){if(t=t[n],"number"==typeof t)return t;if("object"!=typeof t)throw new Error("invalid huffman sequence")}return null}function w(e){let n=e,t=0;for(;n>0;){const e=p();if(null===e)return;t=t<<1|e,--n}return t}function C(e){const n=w(e);return n>=1<<e-1?n:n+(-1<<e)+1}let v=0;let y,P=0;function T(e,n,t,s,r){const o=t%f,a=(t/f|0)*e.v+s,c=o*e.h+r;n(e,e.blocks[a][c])}function g(e,n,t){const s=t/e.blocksPerLine|0,r=t%e.blocksPerLine;n(e,e.blocks[s][r])}const x=s.length;let A,L,E,D,I,q;q=h?0===a?0===i?function(e,n){const t=k(e.huffmanTableDC),s=0===t?0:C(t)<<l;e.pred+=s,n[0]=e.pred}:function(e,n){n[0]|=p()<<l}:0===i?function(e,n){if(v>0)return void v--;let t=a;const s=c;for(;t<=s;){const s=k(e.huffmanTableAC),o=15&s,a=s>>4;if(0===o){if(a<15){v=w(a)+(1<<a)-1;break}t+=16}else{t+=a;n[r[t]]=C(o)*(1<<l),t++}}}:function(e,n){let t=a;const s=c;let o=0;for(;t<=s;){const s=r[t],a=n[s]<0?-1:1;switch(P){case 0:{const n=k(e.huffmanTableAC),t=15&n;if(o=n>>4,0===t)o<15?(v=w(o)+(1<<o),P=4):(o=16,P=1);else{if(1!==t)throw new Error("invalid ACn encoding");y=C(t),P=o?2:3}continue}case 1:case 2:n[s]?n[s]+=(p()<<l)*a:(o--,0===o&&(P=2===P?3:0));break;case 3:n[s]?n[s]+=(p()<<l)*a:(n[s]=y<<l,P=0);break;case 4:n[s]&&(n[s]+=(p()<<l)*a)}t++}4===P&&(v--,0===v&&(P=0))}:function(e,n){const t=k(e.huffmanTableDC),s=0===t?0:C(t);e.pred+=s,n[0]=e.pred;let o=1;for(;o<64;){const t=k(e.huffmanTableAC),s=15&t,a=t>>4;if(0===s){if(a<15)break;o+=16}else{o+=a;n[r[o]]=C(s),o++}}};let z,O,U=0;O=1===x?s[0].blocksPerLine*s[0].blocksPerColumn:f*t.mcusPerColumn;const M=o||O;for(;U<O;){for(L=0;L<x;L++)s[L].pred=0;if(v=0,1===x)for(A=s[0],I=0;I<M;I++)g(A,q,U),U++;else for(I=0;I<M;I++){for(L=0;L<x;L++){A=s[L];const{h:e,v:n}=A;for(E=0;E<n;E++)for(D=0;D<e;D++)T(A,q,U,E,D)}if(U++,U===O)break}if(d=0,z=e[m]<<8|e[m+1],z<65280)throw new Error("marker was not found");if(!(z>=65488&&z<=65495))break;m+=2}return m-u}function d(e,n){const t=[],{blocksPerLine:s,blocksPerColumn:r}=n,m=s<<3,b=new Int32Array(64),d=new Uint8Array(64);function p(e,t,s){const r=n.quantizationTable;let m,b,d,p,k,w,C,v,y;const P=s;let T;for(T=0;T<64;T++)P[T]=e[T]*r[T];for(T=0;T<8;++T){const e=8*T;0!==P[1+e]||0!==P[2+e]||0!==P[3+e]||0!==P[4+e]||0!==P[5+e]||0!==P[6+e]||0!==P[7+e]?(m=h*P[0+e]+128>>8,b=h*P[4+e]+128>>8,d=P[2+e],p=P[6+e],k=u*(P[1+e]-P[7+e])+128>>8,v=u*(P[1+e]+P[7+e])+128>>8,w=P[3+e]<<4,C=P[5+e]<<4,y=m-b+1>>1,m=m+b+1>>1,b=y,y=d*f+p*l+128>>8,d=d*l-p*f+128>>8,p=y,y=k-C+1>>1,k=k+C+1>>1,C=y,y=v+w+1>>1,w=v-w+1>>1,v=y,y=m-p+1>>1,m=m+p+1>>1,p=y,y=b-d+1>>1,b=b+d+1>>1,d=y,y=k*i+v*c+2048>>12,k=k*c-v*i+2048>>12,v=y,y=w*a+C*o+2048>>12,w=w*o-C*a+2048>>12,C=y,P[0+e]=m+v,P[7+e]=m-v,P[1+e]=b+C,P[6+e]=b-C,P[2+e]=d+w,P[5+e]=d-w,P[3+e]=p+k,P[4+e]=p-k):(y=h*P[0+e]+512>>10,P[0+e]=y,P[1+e]=y,P[2+e]=y,P[3+e]=y,P[4+e]=y,P[5+e]=y,P[6+e]=y,P[7+e]=y)}for(T=0;T<8;++T){const e=T;0!==P[8+e]||0!==P[16+e]||0!==P[24+e]||0!==P[32+e]||0!==P[40+e]||0!==P[48+e]||0!==P[56+e]?(m=h*P[0+e]+2048>>12,b=h*P[32+e]+2048>>12,d=P[16+e],p=P[48+e],k=u*(P[8+e]-P[56+e])+2048>>12,v=u*(P[8+e]+P[56+e])+2048>>12,w=P[24+e],C=P[40+e],y=m-b+1>>1,m=m+b+1>>1,b=y,y=d*f+p*l+2048>>12,d=d*l-p*f+2048>>12,p=y,y=k-C+1>>1,k=k+C+1>>1,C=y,y=v+w+1>>1,w=v-w+1>>1,v=y,y=m-p+1>>1,m=m+p+1>>1,p=y,y=b-d+1>>1,b=b+d+1>>1,d=y,y=k*i+v*c+2048>>12,k=k*c-v*i+2048>>12,v=y,y=w*a+C*o+2048>>12,w=w*o-C*a+2048>>12,C=y,P[0+e]=m+v,P[56+e]=m-v,P[8+e]=b+C,P[48+e]=b-C,P[16+e]=d+w,P[40+e]=d-w,P[24+e]=p+k,P[32+e]=p-k):(y=h*s[T+0]+8192>>14,P[0+e]=y,P[8+e]=y,P[16+e]=y,P[24+e]=y,P[32+e]=y,P[40+e]=y,P[48+e]=y,P[56+e]=y)}for(T=0;T<64;++T){const e=128+(P[T]+8>>4);t[T]=e<0?0:e>255?255:e}}for(let o=0;o<r;o++){const e=o<<3;for(let n=0;n<8;n++)t.push(new Uint8Array(m));for(let r=0;r<s;r++){p(n.blocks[o][r],d,b);let s=0;const a=r<<3;for(let n=0;n<8;n++){const r=t[e+n];for(let e=0;e<8;e++)r[a+e]=d[s++]}}}return t}class p{constructor(){this.jfif=null,this.adobe=null,this.quantizationTables=[],this.huffmanTablesAC=[],this.huffmanTablesDC=[],this.resetFrames()}resetFrames(){this.frames=[]}parse(e){let n=0;function t(){const t=e[n]<<8|e[n+1];return n+=2,t}function s(){const s=t(),r=e.subarray(n,n+s-2);return n+=r.length,r}function o(e){let n,t,s=0,r=0;for(t in e.components)e.components.hasOwnProperty(t)&&(n=e.components[t],s<n.h&&(s=n.h),r<n.v&&(r=n.v));const o=Math.ceil(e.samplesPerLine/8/s),a=Math.ceil(e.scanLines/8/r);for(t in e.components)if(e.components.hasOwnProperty(t)){n=e.components[t];const c=Math.ceil(Math.ceil(e.samplesPerLine/8)*n.h/s),i=Math.ceil(Math.ceil(e.scanLines/8)*n.v/r),l=o*n.h,f=a*n.v,h=[];for(let e=0;e<f;e++){const e=[];for(let n=0;n<l;n++)e.push(new Int32Array(64));h.push(e)}n.blocksPerLine=c,n.blocksPerColumn=i,n.blocks=h}e.maxH=s,e.maxV=r,e.mcusPerLine=o,e.mcusPerColumn=a}let a=t();if(65496!==a)throw new Error("SOI not found");for(a=t();65497!==a;){switch(a){case 65280:break;case 65504:case 65505:case 65506:case 65507:case 65508:case 65509:case 65510:case 65511:case 65512:case 65513:case 65514:case 65515:case 65516:case 65517:case 65518:case 65519:case 65534:{const e=s();65504===a&&74===e[0]&&70===e[1]&&73===e[2]&&70===e[3]&&0===e[4]&&(this.jfif={version:{major:e[5],minor:e[6]},densityUnits:e[7],xDensity:e[8]<<8|e[9],yDensity:e[10]<<8|e[11],thumbWidth:e[12],thumbHeight:e[13],thumbData:e.subarray(14,14+3*e[12]*e[13])}),65518===a&&65===e[0]&&100===e[1]&&111===e[2]&&98===e[3]&&101===e[4]&&0===e[5]&&(this.adobe={version:e[6],flags0:e[7]<<8|e[8],flags1:e[9]<<8|e[10],transformCode:e[11]});break}case 65499:{const s=t()+n-2;for(;n<s;){const s=e[n++],o=new Int32Array(64);if(s>>4){if(s>>4!==1)throw new Error("DQT: invalid table spec");for(let e=0;e<64;e++){o[r[e]]=t()}}else for(let t=0;t<64;t++){o[r[t]]=e[n++]}this.quantizationTables[15&s]=o}break}case 65472:case 65473:case 65474:{t();const s={extended:65473===a,progressive:65474===a,precision:e[n++],scanLines:t(),samplesPerLine:t(),components:{},componentsOrder:[]},r=e[n++];let c;for(let t=0;t<r;t++){c=e[n];const t=e[n+1]>>4,r=15&e[n+1],o=e[n+2];s.componentsOrder.push(c),s.components[c]={h:t,v:r,quantizationIdx:o},n+=3}o(s),this.frames.push(s);break}case 65476:{const s=t();for(let t=2;t<s;){const s=e[n++],r=new Uint8Array(16);let o=0;for(let t=0;t<16;t++,n++)r[t]=e[n],o+=r[t];const a=new Uint8Array(o);for(let t=0;t<o;t++,n++)a[t]=e[n];t+=17+o,s>>4?this.huffmanTablesAC[15&s]=m(r,a):this.huffmanTablesDC[15&s]=m(r,a)}break}case 65501:t(),this.resetInterval=t();break;case 65498:{t();const s=e[n++],r=[],o=this.frames[0];for(let t=0;t<s;t++){const t=o.components[e[n++]],s=e[n++];t.huffmanTableDC=this.huffmanTablesDC[s>>4],t.huffmanTableAC=this.huffmanTablesAC[15&s],r.push(t)}const a=e[n++],c=e[n++],i=e[n++],l=b(e,n,o,r,this.resetInterval,a,c,i>>4,15&i);n+=l;break}case 65535:255!==e[n]&&n--;break;default:if(255===e[n-3]&&e[n-2]>=192&&e[n-2]<=254){n-=3;break}throw new Error(`unknown JPEG marker ${a.toString(16)}`)}a=t()}}getResult(){const{frames:e}=this;if(0===this.frames.length)throw new Error("no frames were decoded");this.frames.length>1&&console.warn("more than one frame is not supported");for(let l=0;l<this.frames.length;l++){const e=this.frames[l].components;for(const n of Object.keys(e))e[n].quantizationTable=this.quantizationTables[e[n].quantizationIdx],delete e[n].quantizationIdx}const n=e[0],{components:t,componentsOrder:s}=n,r=[],o=n.samplesPerLine,a=n.scanLines;for(let l=0;l<s.length;l++){const e=t[s[l]];r.push({lines:d(0,e),scaleX:e.h/n.maxH,scaleY:e.v/n.maxV})}const c=new Uint8Array(o*a*r.length);let i=0;for(let l=0;l<a;++l)for(let e=0;e<o;++e)for(let n=0;n<r.length;++n){const t=r[n];c[i]=t.lines[0|l*t.scaleY][0|e*t.scaleX],++i}return c}}class k extends s.aQ{constructor(e){super(),this.reader=new p,e.JPEGTables&&this.reader.parse(e.JPEGTables)}decodeBlock(e){return this.reader.resetFrames(),this.reader.parse(new Uint8Array(e)),this.reader.getResult().buffer}}}}]);
//# sourceMappingURL=536.c1fc53cc.chunk.js.map
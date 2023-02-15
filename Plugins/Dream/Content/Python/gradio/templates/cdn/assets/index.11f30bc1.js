import{S as oe,i as ce,s as de,e as E,b as y,d as D,f as R,a4 as ye,l as N,n as B,z as ge,a as j,w as X,J as Ae,H as V,t as _e,h as he,A as rt,a6 as at,g as T,N as x,c as Z,m as G,K as $,j as J,k as P,o as I,E as qe,a7 as U,v as ve,C as ie,a8 as se,a9 as ue,D as fe,P as it,Q as st,R as ut,T as ft}from"./index.62d61aa4.js";import{U as ot}from"./Upload.b0343c69.js";import{d as ct}from"./dsv.7fe76a93.js";var De=Object.prototype.hasOwnProperty;function ee(r,e){var t,l;if(r===e)return!0;if(r&&e&&(t=r.constructor)===e.constructor){if(t===Date)return r.getTime()===e.getTime();if(t===RegExp)return r.toString()===e.toString();if(t===Array){if((l=r.length)===e.length)for(;l--&&ee(r[l],e[l]););return l===-1}if(!t||typeof r=="object"){l=0;for(t in r)if(De.call(r,t)&&++l&&!De.call(e,t)||!(t in e)||!ee(r[t],e[t]))return!1;return Object.keys(e).length===l}}return r!==r&&e!==e}function Le(r){let e,t,l;return{c(){e=E("input"),y(e,"class","absolute outline-none inset-2 bg-transparent border-0 translate-x-px flex-1 "),y(e,"tabindex","-1"),D(e,"translate-x-px",!r[3]),D(e,"font-bold",r[3])},m(a,i){R(a,e,i),ye(e,r[0]),r[8](e),t||(l=[N(e,"input",r[7]),N(e,"keydown",r[6]),N(e,"blur",ht)],t=!0)},p(a,i){i&1&&e.value!==a[0]&&ye(e,a[0]),i&8&&D(e,"translate-x-px",!a[3]),i&8&&D(e,"font-bold",a[3])},d(a){a&&B(e),r[8](null),t=!1,ge(l)}}}function dt(r){let e;return{c(){e=_e(r[0])},m(t,l){R(t,e,l)},p(t,l){l&1&&he(e,t[0])},d(t){t&&B(e)}}}function gt(r){let e,t;return{c(){e=new at(!1),t=rt(),e.a=t},m(l,a){e.m(r[0],l,a),R(l,t,a)},p(l,a){a&1&&e.p(l[0])},d(l){l&&B(t),l&&e.d()}}}function _t(r){let e,t,l,a,i=r[2]&&Le(r);function _(s,g){return s[4]==="markdown"||s[4]==="html"?gt:dt}let h=_(r),f=h(r);return{c(){i&&i.c(),e=j(),t=E("span"),f.c(),y(t,"tabindex","-1"),y(t,"role","button"),y(t,"class","p-2 outline-none border-0 flex-1"),D(t,"opacity-0",r[2]),D(t,"pointer-events-none",r[2])},m(s,g){i&&i.m(s,g),R(s,e,g),R(s,t,g),f.m(t,null),l||(a=N(t,"dblclick",r[5]),l=!0)},p(s,[g]){s[2]?i?i.p(s,g):(i=Le(s),i.c(),i.m(e.parentNode,e)):i&&(i.d(1),i=null),h===(h=_(s))&&f?f.p(s,g):(f.d(1),f=h(s),f&&(f.c(),f.m(t,null))),g&4&&D(t,"opacity-0",s[2]),g&4&&D(t,"pointer-events-none",s[2])},i:X,o:X,d(s){i&&i.d(s),s&&B(e),s&&B(t),f.d(),l=!1,a()}}}const ht=({currentTarget:r})=>r.setAttribute("tabindex","-1");function bt(r,e,t){let{edit:l}=e,{value:a=""}=e,{el:i}=e,{header:_=!1}=e,{datatype:h="str"}=e;function f(c){Ae.call(this,r,c)}function s(c){Ae.call(this,r,c)}function g(){a=this.value,t(0,a)}function w(c){V[c?"unshift":"push"](()=>{i=c,t(1,i)})}return r.$$set=c=>{"edit"in c&&t(2,l=c.edit),"value"in c&&t(0,a=c.value),"el"in c&&t(1,i=c.el),"header"in c&&t(3,_=c.header),"datatype"in c&&t(4,h=c.datatype)},[a,i,l,_,h,f,s,g,w]}class Fe extends oe{constructor(e){super(),ce(this,e,bt,_t,de,{edit:2,value:0,el:1,header:3,datatype:4})}}function Me(r,e,t){const l=r.slice();return l[52]=e[t],l[54]=t,l}function Te(r,e,t){const l=r.slice();return l[55]=e[t].value,l[56]=e[t].id,l[57]=e,l[58]=t,l}function Ee(r,e,t){const l=r.slice();return l[55]=e[t].value,l[56]=e[t].id,l[59]=e,l[54]=t,l}function Ce(r){let e,t;return{c(){e=E("p"),t=_e(r[1]),y(e,"class","text-gray-600 text-[0.855rem] mb-2 block dark:text-gray-200 relative z-40")},m(l,a){R(l,e,a),T(e,t)},p(l,a){a[0]&2&&he(t,l[1])},d(l){l&&B(e)}}}function He(r){let e,t;return{c(){e=E("caption"),t=_e(r[1]),y(e,"class","sr-only")},m(l,a){R(l,e,a),T(e,t)},p(l,a){a[0]&2&&he(t,l[1])},d(l){l&&B(e)}}}function Re(r,e){let t,l,a,i,_,h,f,s,g,w,c,b=e[56],o,v,S;function u(z){e[30](z,e[56])}function p(){return e[31](e[56])}let M={value:e[55],edit:e[13]===e[56],header:!0};e[10][e[56]].input!==void 0&&(M.el=e[10][e[56]].input),a=new Fe({props:M}),V.push(()=>x(a,"el",u)),a.$on("keydown",e[21]),a.$on("dblclick",p);function m(){return e[32](e[54])}const H=()=>e[33](t,b),F=()=>e[33](null,b);return{key:r,first:null,c(){t=E("th"),l=E("div"),Z(a.$$.fragment),_=j(),h=E("div"),f=ve("svg"),s=ve("path"),w=j(),y(s,"d","M4.49999 0L8.3971 6.75H0.602875L4.49999 0Z"),y(f,"width","1em"),y(f,"height","1em"),y(f,"class","fill-current text-[10px]"),y(f,"viewBox","0 0 9 7"),y(f,"fill","none"),y(f,"xmlns","http://www.w3.org/2000/svg"),y(h,"class",g="flex flex-none items-center justify-center p-2 cursor-pointer leading-snug transform transition-all "+(e[12]!==e[54]?"text-gray-200 hover:text-gray-500":"text-orange-500")+" "+(e[12]===e[54]&&e[11]==="des"?"-scale-y-[1]":"")),D(h,"text-gray-200",e[12]!==e[54]),y(l,"class","min-h-[2.3rem] flex outline-none"),y(t,"class","p-0 relative focus-within:ring-1 ring-orange-500 ring-inset outline-none"),y(t,"aria-sort",c=e[15](e[55],e[12],e[11])),D(t,"bg-orange-50",e[13]===e[56]),D(t,"dark:bg-transparent",e[13]===e[56]),D(t,"rounded-tl-lg",e[54]===0),D(t,"rounded-tr-lg",e[54]===e[8].length-1),this.first=t},m(z,C){R(z,t,C),T(t,l),G(a,l,null),T(l,_),T(l,h),T(h,f),T(f,s),T(t,w),H(),o=!0,v||(S=N(h,"click",m),v=!0)},p(z,C){e=z;const Y={};C[0]&256&&(Y.value=e[55]),C[0]&8448&&(Y.edit=e[13]===e[56]),!i&&C[0]&1280&&(i=!0,Y.el=e[10][e[56]].input,$(()=>i=!1)),a.$set(Y),(!o||C[0]&6400&&g!==(g="flex flex-none items-center justify-center p-2 cursor-pointer leading-snug transform transition-all "+(e[12]!==e[54]?"text-gray-200 hover:text-gray-500":"text-orange-500")+" "+(e[12]===e[54]&&e[11]==="des"?"-scale-y-[1]":"")))&&y(h,"class",g),C[0]&6400&&D(h,"text-gray-200",e[12]!==e[54]),(!o||C[0]&6400&&c!==(c=e[15](e[55],e[12],e[11])))&&y(t,"aria-sort",c),b!==e[56]&&(F(),b=e[56],H()),C[0]&8448&&D(t,"bg-orange-50",e[13]===e[56]),C[0]&8448&&D(t,"dark:bg-transparent",e[13]===e[56]),C[0]&256&&D(t,"rounded-tl-lg",e[54]===0),C[0]&256&&D(t,"rounded-tr-lg",e[54]===e[8].length-1)},i(z){o||(J(a.$$.fragment,z),o=!0)},o(z){P(a.$$.fragment,z),o=!1},d(z){z&&B(t),I(a),F(),v=!1,S()}}}function Be(r,e){let t,l,a,i,_,h=e[56],f,s,g;function w(m){e[34](m,e[55],e[57],e[58])}function c(m){e[35](m,e[56])}let b={edit:e[6]===e[56],datatype:Array.isArray(e[0])?e[0][e[58]]:e[0]};e[55]!==void 0&&(b.value=e[55]),e[10][e[56]].input!==void 0&&(b.el=e[10][e[56]].input),a=new Fe({props:b}),V.push(()=>x(a,"value",w)),V.push(()=>x(a,"el",c));const o=()=>e[36](t,h),v=()=>e[36](null,h);function S(){return e[37](e[56])}function u(){return e[38](e[56])}function p(){return e[39](e[56])}function M(...m){return e[40](e[54],e[58],e[56],...m)}return{key:r,first:null,c(){t=E("td"),l=E("div"),Z(a.$$.fragment),y(l,"class","min-h-[2.3rem] h-full outline-none flex items-center"),D(l,"border-transparent",e[7]!==e[56]),y(t,"tabindex","0"),y(t,"class","outline-none focus-within:ring-1 ring-orange-500 ring-inset focus-within:bg-orange-50 dark:focus-within:bg-gray-800 group-last:first:rounded-bl-lg group-last:last:rounded-br-lg relative"),this.first=t},m(m,H){R(m,t,H),T(t,l),G(a,l,null),o(),f=!0,s||(g=[N(t,"touchstart",S,{passive:!0}),N(t,"click",u),N(t,"dblclick",p),N(t,"keydown",M)],s=!0)},p(m,H){e=m;const F={};H[0]&576&&(F.edit=e[6]===e[56]),H[0]&513&&(F.datatype=Array.isArray(e[0])?e[0][e[58]]:e[0]),!i&&H[0]&512&&(i=!0,F.value=e[55],$(()=>i=!1)),!_&&H[0]&1536&&(_=!0,F.el=e[10][e[56]].input,$(()=>_=!1)),a.$set(F),H[0]&640&&D(l,"border-transparent",e[7]!==e[56]),h!==e[56]&&(v(),h=e[56],o())},i(m){f||(J(a.$$.fragment,m),f=!0)},o(m){P(a.$$.fragment,m),f=!1},d(m){m&&B(t),I(a),v(),s=!1,ge(g)}}}function Se(r,e){let t,l=[],a=new Map,i,_,h=e[52];const f=s=>s[56];for(let s=0;s<h.length;s+=1){let g=Te(e,h,s),w=f(g);a.set(w,l[s]=Be(w,g))}return{key:r,first:null,c(){t=E("tr");for(let s=0;s<l.length;s+=1)l[s].c();i=j(),y(t,"class","group border-b dark:border-gray-700 last:border-none divide-x dark:divide-gray-700 space-x-4 odd:bg-gray-50 dark:odd:bg-gray-900 group focus:bg-gradient-to-b focus:from-blue-100 dark:focus:from-blue-900 focus:to-blue-50 dark:focus:to-gray-900 focus:odd:bg-white"),this.first=t},m(s,g){R(s,t,g);for(let w=0;w<l.length;w+=1)l[w].m(t,null);T(t,i),_=!0},p(s,g){e=s,g[0]&460481&&(h=e[52],ie(),l=se(l,g,f,1,e,h,a,t,ue,Be,i,Te),fe())},i(s){if(!_){for(let g=0;g<h.length;g+=1)J(l[g]);_=!0}},o(s){for(let g=0;g<l.length;g+=1)P(l[g]);_=!1},d(s){s&&B(t);for(let g=0;g<l.length;g+=1)l[g].d()}}}function mt(r){let e,t,l,a,i=[],_=new Map,h,f,s=[],g=new Map,w,c=r[1]&&r[1].length!==0&&He(r),b=r[8];const o=u=>u[56];for(let u=0;u<b.length;u+=1){let p=Ee(r,b,u),M=o(p);_.set(M,i[u]=Re(M,p))}let v=r[9];const S=u=>u[52];for(let u=0;u<v.length;u+=1){let p=Me(r,v,u),M=S(p);g.set(M,s[u]=Se(M,p))}return{c(){e=E("table"),c&&c.c(),t=j(),l=E("thead"),a=E("tr");for(let u=0;u<i.length;u+=1)i[u].c();h=j(),f=E("tbody");for(let u=0;u<s.length;u+=1)s[u].c();y(a,"class","border-b dark:border-gray-700 divide-x dark:divide-gray-700 text-left"),y(l,"class","sticky top-0 left-0 right-0 bg-white shadow-sm z-10"),y(f,"class","overflow-y-scroll"),y(e,"class","table-auto font-mono w-full text-gray-900 text-sm transition-opacity overflow-hidden"),D(e,"opacity-40",r[14])},m(u,p){R(u,e,p),c&&c.m(e,null),T(e,t),T(e,l),T(l,a);for(let M=0;M<i.length;M+=1)i[M].m(a,null);T(e,h),T(e,f);for(let M=0;M<s.length;M+=1)s[M].m(f,null);w=!0},p(u,p){u[1]&&u[1].length!==0?c?c.p(u,p):(c=He(u),c.c(),c.m(e,t)):c&&(c.d(1),c=null),p[0]&3718400&&(b=u[8],ie(),i=se(i,p,o,1,u,b,_,a,ue,Re,null,Ee),fe()),p[0]&460481&&(v=u[9],ie(),s=se(s,p,S,1,u,v,g,f,ue,Se,null,Me),fe()),p[0]&16384&&D(e,"opacity-40",u[14])},i(u){if(!w){for(let p=0;p<b.length;p+=1)J(i[p]);for(let p=0;p<v.length;p+=1)J(s[p]);w=!0}},o(u){for(let p=0;p<i.length;p+=1)P(i[p]);for(let p=0;p<s.length;p+=1)P(s[p]);w=!1},d(u){u&&B(e),c&&c.d();for(let p=0;p<i.length;p+=1)i[p].d();for(let p=0;p<s.length;p+=1)s[p].d()}}}function ze(r){let e,t,l=r[3][1]==="dynamic"&&Ne(r),a=r[2][1]==="dynamic"&&Oe(r);return{c(){e=E("div"),l&&l.c(),t=j(),a&&a.c(),y(e,"class","flex justify-end space-x-1 pt-2 text-gray-800")},m(i,_){R(i,e,_),l&&l.m(e,null),T(e,t),a&&a.m(e,null)},p(i,_){i[3][1]==="dynamic"?l?l.p(i,_):(l=Ne(i),l.c(),l.m(e,t)):l&&(l.d(1),l=null),i[2][1]==="dynamic"?a?a.p(i,_):(a=Oe(i),a.c(),a.m(e,null)):a&&(a.d(1),a=null)},d(i){i&&B(e),l&&l.d(),a&&a.d()}}}function Ne(r){let e,t,l;return{c(){e=E("button"),e.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="mr-1 group-hover:text-orange-500" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path fill="currentColor" d="M24.59 16.59L17 24.17V4h-2v20.17l-7.59-7.58L6 18l10 10l10-10l-1.41-1.41z"></path></svg>New row',y(e,"class","!flex-none gr-button group")},m(a,i){R(a,e,i),t||(l=N(e,"click",r[43]),t=!0)},p:X,d(a){a&&B(e),t=!1,l()}}}function Oe(r){let e,t,l;return{c(){e=E("button"),e.innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="mr-1 group-hover:text-orange-500" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path fill="currentColor" d="m18 6l-1.43 1.393L24.15 15H4v2h20.15l-7.58 7.573L18 26l10-10L18 6z"></path></svg>
					New column`,y(e,"class","!flex-none gr-button group")},m(a,i){R(a,e,i),t||(l=N(e,"click",r[23]),t=!0)},p:X,d(a){a&&B(e),t=!1,l()}}}function pt(r){let e,t,l,a,i,_,h,f,s,g=r[1]&&r[1].length!==0&&Ce(r);function w(o){r[41](o)}let c={flex:!1,center:!1,boundedheight:!1,click:!1,$$slots:{default:[mt]},$$scope:{ctx:r}};r[14]!==void 0&&(c.dragging=r[14]),a=new ot({props:c}),V.push(()=>x(a,"dragging",w)),a.$on("load",r[42]);let b=r[4]&&ze(r);return{c(){e=E("div"),g&&g.c(),t=j(),l=E("div"),Z(a.$$.fragment),_=j(),b&&b.c(),y(l,"class","scroll-hide overflow-hidden rounded-lg relative border transition-colors overflow-x-scroll"),D(l,"border-green-400",r[14]),D(l,"whitespace-nowrap",!r[5]),D(e,"mt-6",r[1]&&r[1].length!==0)},m(o,v){R(o,e,v),g&&g.m(e,null),T(e,t),T(e,l),G(a,l,null),T(e,_),b&&b.m(e,null),h=!0,f||(s=[N(window,"click",r[24]),N(window,"touchstart",r[24])],f=!0)},p(o,v){o[1]&&o[1].length!==0?g?g.p(o,v):(g=Ce(o),g.c(),g.m(e,t)):g&&(g.d(1),g=null);const S={};v[0]&32707|v[1]&536870912&&(S.$$scope={dirty:v,ctx:o}),!i&&v[0]&16384&&(i=!0,S.dragging=o[14],$(()=>i=!1)),a.$set(S),v[0]&16384&&D(l,"border-green-400",o[14]),v[0]&32&&D(l,"whitespace-nowrap",!o[5]),o[4]?b?b.p(o,v):(b=ze(o),b.c(),b.m(e,null)):b&&(b.d(1),b=null),v[0]&2&&D(e,"mt-6",o[1]&&o[1].length!==0)},i(o){h||(J(a.$$.fragment,o),h=!0)},o(o){P(a.$$.fragment,o),h=!1},d(o){o&&B(e),g&&g.d(),I(a),b&&b.d(),f=!1,ge(s)}}}function kt(r,e){return e.filter(t);function t(l){var a=-1;return r.split(`
`).every(i);function i(_){if(!_)return!0;var h=_.split(l).length;return a<0&&(a=h),a===h&&h>1}}}function wt(r){const e=atob(r.split(",")[1]),t=r.split(",")[0].split(":")[1].split(";")[0],l=new ArrayBuffer(e.length),a=new Uint8Array(l);for(let i=0;i<e.length;i++)a[i]=e.charCodeAt(i);return new Blob([l],{type:t})}function yt(r,e,t){let{datatype:l}=e,{label:a=null}=e,{headers:i=[]}=e,{values:_=[[]]}=e,{col_count:h}=e,{row_count:f}=e,{editable:s=!0}=e,{wrap:g=!1}=e;const w=qe();let c=!1,b=!1,o={};function v(n){let d=n||[];if(h[1]==="fixed"&&d.length<h[0]){const k=Array(h[0]-d.length).fill("").map((A,L)=>`${L+d.length}`);d=d.concat(k)}return!d||d.length===0?Array(h[0]).fill(0).map((k,A)=>{const L=`h-${A}`;return t(10,o[L]={cell:null,input:null},o),{id:L,value:JSON.stringify(A+1)}}):d.map((k,A)=>{const L=`h-${A}`;return t(10,o[L]={cell:null,input:null},o),{id:L,value:k??""}})}function S(n){const d=n.length>0?n.length:f[0];return Array(f[1]==="fixed"||d<f[0]?f[0]:d).fill(0).map((k,A)=>Array(h[1]==="fixed"?h[0]:n[0].length).fill(0).map((L,q)=>{const K=`${A}-${q}`;return t(10,o[K]={input:null,cell:null},o),{value:n?.[A]?.[q]??"",id:K}}))}let u=v(i),p;async function M(){typeof c=="string"?(await U(),o[c]?.input?.focus()):typeof b=="string"&&(await U(),o[b]?.input?.focus())}let m=[[]],H;function F(n,d,k){if(!d)return"none";if(i[d]===n){if(k==="asc")return"ascending";if(k==="des")return"descending"}}function z(n){return m.reduce((d,k,A)=>{const L=k.reduce((q,K,re)=>n===K.id?re:q,-1);return L===-1?d:[A,L]},[-1,-1])}async function C(n,d){if(!s||c===n)return;if(d){const[A,L]=z(n);t(9,m[A][L].value="",m)}t(6,c=n),await U();const{input:k}=o[n];k?.focus()}async function Y(n,d,k,A){let L;switch(n.key){case"ArrowRight":if(c)break;n.preventDefault(),L=m[d][k+1],t(7,b=L?L.id:b);break;case"ArrowLeft":if(c)break;n.preventDefault(),L=m[d][k-1],t(7,b=L?L.id:b);break;case"ArrowDown":if(c)break;n.preventDefault(),L=m[d+1],t(7,b=L?L[k].id:b);break;case"ArrowUp":if(c)break;n.preventDefault(),L=m[d-1],t(7,b=L?L[k].id:b);break;case"Escape":if(!s)break;n.preventDefault(),t(7,b=c),t(6,c=!1);break;case"Enter":if(!s)break;if(n.preventDefault(),n.shiftKey){le(d),await U();const[nt]=z(A);t(7,b=m[nt+1][k].id)}else c===A?t(6,c=!1):C(A);break;case"Backspace":if(!s)break;c||(n.preventDefault(),t(9,m[d][k].value="",m));break;case"Delete":if(!s)break;c||(n.preventDefault(),t(9,m[d][k].value="",m));break;case"Tab":let q=n.shiftKey?-1:1,K=m[d][k+q],re=m?.[d+q]?.[q>0?0:u.length-1],ae=K||re;ae&&(n.preventDefault(),t(7,b=ae?ae.id:b)),t(6,c=!1);break;default:(!c||c&&c!==A)&&n.key.length===1&&C(A,!0);break}}async function be(n){c!==n&&b!==n&&(t(6,c=!1),t(7,b=n))}async function me(n,d){if(d==="edit"&&typeof n=="string"&&(await U(),o[n].input?.focus()),d==="edit"&&typeof n=="boolean"&&typeof b=="string"){let k=o[b]?.cell;await U(),k?.focus()}if(d==="select"&&typeof n=="string"){const{cell:k}=o[n];await U(),k?.focus()}}let Q,W;function Ue(n,d){d==="asc"?t(9,m=m.sort((k,A)=>k[n].value<A[n].value?-1:1)):d==="des"&&t(9,m=m.sort((k,A)=>k[n].value>A[n].value?-1:1))}function pe(n){typeof W!="number"||W!==n?(t(11,Q="asc"),t(12,W=n)):Q==="asc"?t(11,Q="des"):Q==="des"&&t(11,Q="asc"),Ue(n,Q)}let O;function ke(){if(typeof b=="string"){const n=o[b].input?.value;if(u.find(d=>d.id===b)){let d=u.find(k=>k.id===b);n&&(d.value=n)}else n&&u.push({id:b,value:n})}}async function te(n,d){!s||h[1]!=="dynamic"||c===n||(t(13,O=n),await U(),o[n].input?.focus(),d&&o[n].input?.select())}function je(n){if(!!s)switch(n.key){case"Escape":case"Enter":case"Tab":n.preventDefault(),t(7,b=O),t(13,O=!1),ke();break}}function le(n){f[1]==="dynamic"&&(m.splice(n?n+1:m.length,0,Array(m[0].length).fill(0).map((d,k)=>{const A=`${m.length}-${k}`;return t(10,o[A]={cell:null,input:null},o),{id:A,value:""}})),t(9,m),t(27,_),t(29,H),t(26,i))}async function Ke(){if(h[1]!=="dynamic")return;for(let d=0;d<m.length;d++){const k=`${d}-${m[d].length}`;t(10,o[k]={cell:null,input:null},o),m[d].push({id:k,value:""})}const n=`h-${u.length}`;t(10,o[n]={cell:null,input:null},o),u.push({id:n,value:`Header ${u.length+1}`}),t(9,m),t(27,_),t(29,H),t(26,i),t(8,u),t(26,i),t(28,p),t(27,_),await U(),te(n,!0)}function Je(n){typeof c=="string"&&o[c]&&o[c].cell!==n.target&&!o[c].cell?.contains(n?.target)&&t(6,c=!1),typeof O=="string"&&o[O]&&o[O].cell!==n.target&&!o[O].cell?.contains(n.target)&&(t(7,b=O),t(13,O=!1),ke(),t(13,O=!1))}function we(n){const d=new FileReader;function k(A){if(!A?.target?.result||typeof A.target.result!="string")return;const[L]=kt(A.target.result,[",","	"]),[q,...K]=ct(L).parseRows(A.target.result);t(8,u=v(h[1]==="fixed"?q.slice(0,h[0]):q)),t(27,_=K),d.removeEventListener("loadend",k)}d.addEventListener("loadend",k),d.readAsText(n)}let ne=!1;function Pe(n,d){r.$$.not_equal(o[d].input,n)&&(o[d].input=n,t(10,o))}const Ye=n=>te(n),Qe=n=>pe(n);function Ve(n,d){V[n?"unshift":"push"](()=>{o[d].cell=n,t(10,o)})}function Ze(n,d,k,A){k[A].value=n,t(9,m),t(27,_),t(29,H),t(26,i)}function Ge(n,d){r.$$.not_equal(o[d].input,n)&&(o[d].input=n,t(10,o))}function Ie(n,d){V[n?"unshift":"push"](()=>{o[d].cell=n,t(10,o)})}const We=n=>C(n),Xe=n=>be(n),xe=n=>C(n),$e=(n,d,k,A)=>Y(A,n,d,k);function et(n){ne=n,t(14,ne)}const tt=n=>we(wt(n.detail.data)),lt=()=>le();return r.$$set=n=>{"datatype"in n&&t(0,l=n.datatype),"label"in n&&t(1,a=n.label),"headers"in n&&t(26,i=n.headers),"values"in n&&t(27,_=n.values),"col_count"in n&&t(2,h=n.col_count),"row_count"in n&&t(3,f=n.row_count),"editable"in n&&t(4,s=n.editable),"wrap"in n&&t(5,g=n.wrap)},r.$$.update=()=>{r.$$.dirty[0]&201326592&&(_&&!Array.isArray(_)?(t(26,i=_.headers),t(27,_=_.data.length===0?[Array(i.length).fill("")]:_.data)):_===null?t(27,_=[Array(i.length).fill("")]):(t(27,_),t(26,i))),r.$$.dirty[0]&335544320&&(ee(i,p)||(t(8,u=v(i)),t(28,p=i),M())),r.$$.dirty[0]&671088640&&(ee(_,H)||(t(9,m=S(_)),t(29,H=_),M())),r.$$.dirty[0]&768&&u&&w("change",{data:m.map(n=>n.map(({value:d})=>d)),headers:u.map(n=>n.value)}),r.$$.dirty[0]&64&&me(c,"edit"),r.$$.dirty[0]&128&&me(b,"select")},[l,a,h,f,s,g,c,b,u,m,o,Q,W,O,ne,F,C,Y,be,pe,te,je,le,Ke,Je,we,i,_,p,H,Pe,Ye,Qe,Ve,Ze,Ge,Ie,We,Xe,xe,$e,et,tt,lt]}class At extends oe{constructor(e){super(),ce(this,e,yt,pt,de,{datatype:0,label:1,headers:26,values:27,col_count:2,row_count:3,editable:4,wrap:5},null,[-1,-1])}}function vt(r){let e,t,l,a,i;const _=[r[10]];let h={};for(let f=0;f<_.length;f+=1)h=it(h,_[f]);return t=new st({props:h}),a=new At({props:{label:r[7],row_count:r[6],col_count:r[5],values:r[0],headers:r[1],editable:r[4]==="dynamic",wrap:r[8],datatype:r[9]}}),a.$on("change",r[12]),{c(){e=E("div"),Z(t.$$.fragment),l=j(),Z(a.$$.fragment),y(e,"id",r[2]),y(e,"class","relative overflow-hidden"),D(e,"!hidden",!r[3])},m(f,s){R(f,e,s),G(t,e,null),T(e,l),G(a,e,null),i=!0},p(f,[s]){const g=s&1024?ut(_,[ft(f[10])]):{};t.$set(g);const w={};s&128&&(w.label=f[7]),s&64&&(w.row_count=f[6]),s&32&&(w.col_count=f[5]),s&1&&(w.values=f[0]),s&2&&(w.headers=f[1]),s&16&&(w.editable=f[4]==="dynamic"),s&256&&(w.wrap=f[8]),s&512&&(w.datatype=f[9]),a.$set(w),(!i||s&4)&&y(e,"id",f[2]),s&8&&D(e,"!hidden",!f[3])},i(f){i||(J(t.$$.fragment,f),J(a.$$.fragment,f),i=!0)},o(f){P(t.$$.fragment,f),P(a.$$.fragment,f),i=!1},d(f){f&&B(e),I(t),I(a)}}}function Dt(r,e,t){let{headers:l=[]}=e,{elem_id:a=""}=e,{visible:i=!0}=e,{value:_={data:[["","",""]],headers:["1","2","3"]}}=e,{mode:h}=e,{col_count:f}=e,{row_count:s}=e,{label:g=null}=e,{wrap:w}=e,{datatype:c}=e;const b=qe();let{loading_status:o}=e;async function v(u){t(0,_=u),await U(),b("change",u)}const S=({detail:u})=>v(u);return r.$$set=u=>{"headers"in u&&t(1,l=u.headers),"elem_id"in u&&t(2,a=u.elem_id),"visible"in u&&t(3,i=u.visible),"value"in u&&t(0,_=u.value),"mode"in u&&t(4,h=u.mode),"col_count"in u&&t(5,f=u.col_count),"row_count"in u&&t(6,s=u.row_count),"label"in u&&t(7,g=u.label),"wrap"in u&&t(8,w=u.wrap),"datatype"in u&&t(9,c=u.datatype),"loading_status"in u&&t(10,o=u.loading_status)},[_,l,a,i,h,f,s,g,w,c,o,v,S]}class Lt extends oe{constructor(e){super(),ce(this,e,Dt,vt,de,{headers:1,elem_id:2,visible:3,value:0,mode:4,col_count:5,row_count:6,label:7,wrap:8,datatype:9,loading_status:10})}}var Ct=Lt;const Ht=["static","dynamic"];export{Ct as Component,Ht as modes};

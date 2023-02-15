import{S as de,i as pe,s as ke,ab as le,c as H,m as I,l as S,j as w,k as A,o as N,P as ve,Q as we,a as L,A as ye,f as C,R as je,T as ze,C as q,D as M,n as G,a7 as Be,H as Y,e as v,b as g,L as R,Y as F,d as B,g as y,t as te,h as ne,B as ie,z as Ae,ae as Ce,w as E}from"./index.9828d028.js";import{B as Ge}from"./Block.fae874df.js";import{B as De}from"./BlockLabel.9871a187.js";import{M as Le}from"./ModifyUpload.e0ee2bd9.js";import{n as J}from"./utils.27234e1d.js";import{g as Re}from"./styles.ed3b21b5.js";import{I as U}from"./Image.565da8ba.js";function K(t,e,l){const i=t.slice();return i[29]=e[l][0],i[30]=e[l][1],i[32]=l,i}function O(t,e,l){const i=t.slice();return i[29]=e[l],i[33]=e,i[32]=l,i}function W(t){let e,l;return e=new De({props:{show_label:t[1],Icon:U,label:t[2]||"Gallery",disable:typeof t[6].container=="boolean"&&!t[6].container}}),{c(){H(e.$$.fragment)},m(i,o){I(e,i,o),l=!0},p(i,o){const n={};o[0]&2&&(n.show_label=i[1]),o[0]&4&&(n.label=i[2]||"Gallery"),o[0]&64&&(n.disable=typeof i[6].container=="boolean"&&!i[6].container),e.$set(n)},i(i){l||(w(e.$$.fragment,i),l=!0)},o(i){A(e.$$.fragment,i),l=!1},d(i){N(e,i)}}}function He(t){let e,l,i,o,n,r,a=t[7]!==null&&X(t);const m=[Se,Ne],d=[];function _(u,h){return u[10].length===0?0:1}return i=_(t),o=d[i]=m[i](t),{c(){a&&a.c(),e=L(),l=v("div"),o.c(),g(l,"class","overflow-y-auto h-full p-2"),le(()=>t[26].call(l)),B(l,"min-h-[350px]",t[6].height!=="auto"),B(l,"max-h-[55vh]",t[6].height!=="auto"),B(l,"xl:min-h-[450px]",t[6].height!=="auto")},m(u,h){a&&a.m(u,h),C(u,e,h),C(u,l,h),d[i].m(l,null),n=Ce(l,t[26].bind(l)),r=!0},p(u,h){u[7]!==null?a?(a.p(u,h),h[0]&128&&w(a,1)):(a=X(u),a.c(),w(a,1),a.m(e.parentNode,e)):a&&(q(),A(a,1,1,()=>{a=null}),M());let j=i;i=_(u),i===j?d[i].p(u,h):(q(),A(d[j],1,1,()=>{d[j]=null}),M(),o=d[i],o?o.p(u,h):(o=d[i]=m[i](u),o.c()),w(o,1),o.m(l,null)),h[0]&64&&B(l,"min-h-[350px]",u[6].height!=="auto"),h[0]&64&&B(l,"max-h-[55vh]",u[6].height!=="auto"),h[0]&64&&B(l,"xl:min-h-[450px]",u[6].height!=="auto")},i(u){r||(w(a),w(o),r=!0)},o(u){A(a),A(o),r=!1},d(u){a&&a.d(u),u&&G(e),u&&G(l),d[i].d(),n()}}}function Ie(t){let e,l,i,o;return i=new U({}),{c(){e=v("div"),l=v("div"),H(i.$$.fragment),g(l,"class","h-5 dark:text-white opacity-50"),g(e,"class","h-full min-h-[15rem] flex justify-center items-center")},m(n,r){C(n,e,r),y(e,l),I(i,l,null),o=!0},p:E,i(n){o||(w(i.$$.fragment,n),o=!0)},o(n){A(i.$$.fragment,n),o=!1},d(n){n&&G(e),N(i)}}}function X(t){let e,l,i,o,n,r,a,m,d,_,u,h,j;l=new Le({}),l.$on("clear",t[20]);let s=t[10][t[7]][1]&&Z(t),b=t[10],k=[];for(let f=0;f<b.length;f+=1)k[f]=$(O(t,b,f));return{c(){e=v("div"),H(l.$$.fragment),i=L(),o=v("img"),m=L(),s&&s.c(),d=L(),_=v("div");for(let f=0;f<k.length;f+=1)k[f].c();g(o,"class","w-full object-contain h-[calc(100%-50px)"),R(o.src,n=t[10][t[7]][0].data)||g(o,"src",n),g(o,"alt",r=t[10][t[7]][1]||""),g(o,"title",a=t[10][t[7]][1]||null),F(o,"height","calc(100% - "+(t[10][t[7]][1]?"80px":"60px")+")"),g(_,"class","absolute h-[60px] overflow-x-scroll scroll-hide w-full bottom-0 flex gap-1.5 items-center py-2 text-sm px-3 justify-center"),g(e,"class","absolute group inset-0 z-10 flex flex-col bg-white/90 dark:bg-gray-900 backdrop-blur h-full"),B(e,"min-h-[350px]",t[6].height!=="auto"),B(e,"max-h-[55vh]",t[6].height!=="auto"),B(e,"xl:min-h-[450px]",t[6].height!=="auto")},m(f,z){C(f,e,z),I(l,e,null),y(e,i),y(e,o),y(e,m),s&&s.m(e,null),y(e,d),y(e,_);for(let p=0;p<k.length;p+=1)k[p].m(_,null);t[24](_),u=!0,h||(j=[S(o,"click",t[21]),S(e,"keydown",t[16])],h=!0)},p(f,z){if((!u||z[0]&1152&&!R(o.src,n=f[10][f[7]][0].data))&&g(o,"src",n),(!u||z[0]&1152&&r!==(r=f[10][f[7]][1]||""))&&g(o,"alt",r),(!u||z[0]&1152&&a!==(a=f[10][f[7]][1]||null))&&g(o,"title",a),(!u||z[0]&1152)&&F(o,"height","calc(100% - "+(f[10][f[7]][1]?"80px":"60px")+")"),f[10][f[7]][1]?s?s.p(f,z):(s=Z(f),s.c(),s.m(e,d)):s&&(s.d(1),s=null),z[0]&3200){b=f[10];let p;for(p=0;p<b.length;p+=1){const D=O(f,b,p);k[p]?k[p].p(D,z):(k[p]=$(D),k[p].c(),k[p].m(_,null))}for(;p<k.length;p+=1)k[p].d(1);k.length=b.length}z[0]&64&&B(e,"min-h-[350px]",f[6].height!=="auto"),z[0]&64&&B(e,"max-h-[55vh]",f[6].height!=="auto"),z[0]&64&&B(e,"xl:min-h-[450px]",f[6].height!=="auto")},i(f){u||(w(l.$$.fragment,f),u=!0)},o(f){A(l.$$.fragment,f),u=!1},d(f){f&&G(e),N(l),s&&s.d(),ie(k,f),t[24](null),h=!1,Ae(j)}}}function Z(t){let e,l,i=t[10][t[7]][1]+"",o;return{c(){e=v("div"),l=v("div"),o=te(i),g(l,"class","dark:text-gray-200 font-semibold px-3 py-1 max-w-full truncate"),g(e,"class","bottom-[50px] absolute z-[5] flex justify-center w-full")},m(n,r){C(n,e,r),y(e,l),y(l,o)},p(n,r){r[0]&1152&&i!==(i=n[10][n[7]][1]+"")&&ne(o,i)},d(n){n&&G(e)}}}function $(t){let e,l,i,o,n,r,a,m=t[32],d,_;const u=()=>t[22](e,m),h=()=>t[22](null,m);function j(){return t[23](t[32])}return{c(){e=v("button"),l=v("img"),r=L(),g(l,"class","h-full w-full overflow-hidden object-contain"),R(l.src,i=t[29][0].data)||g(l,"src",i),g(l,"title",o=t[29][1]||null),g(l,"alt",n=t[29][1]||null),g(e,"class",a="gallery-item !flex-none !h-9 !w-9 transition-all duration-75 "+(t[7]===t[32]?"!ring-2 !ring-orange-500 hover:!ring-orange-500":"scale-90 transform")+" svelte-1g9btlg")},m(s,b){C(s,e,b),y(e,l),y(e,r),u(),d||(_=S(e,"click",j),d=!0)},p(s,b){t=s,b[0]&1024&&!R(l.src,i=t[29][0].data)&&g(l,"src",i),b[0]&1024&&o!==(o=t[29][1]||null)&&g(l,"title",o),b[0]&1024&&n!==(n=t[29][1]||null)&&g(l,"alt",n),b[0]&128&&a!==(a="gallery-item !flex-none !h-9 !w-9 transition-all duration-75 "+(t[7]===t[32]?"!ring-2 !ring-orange-500 hover:!ring-orange-500":"scale-90 transform")+" svelte-1g9btlg")&&g(e,"class",a),m!==t[32]&&(h(),m=t[32],u())},d(s){s&&G(e),h(),d=!1,_()}}}function Ne(t){let e,l,i=t[10],o=[];for(let n=0;n<i.length;n+=1)o[n]=ee(K(t,i,n));return{c(){e=v("div");for(let n=0;n<o.length;n+=1)o[n].c();g(e,"class",l="grid gap-2 "+t[13]+" svelte-1g9btlg"),B(e,"pt-6",t[1])},m(n,r){C(n,e,r);for(let a=0;a<o.length;a+=1)o[a].m(e,null)},p(n,r){if(r[0]&17536){i=n[10];let a;for(a=0;a<i.length;a+=1){const m=K(n,i,a);o[a]?o[a].p(m,r):(o[a]=ee(m),o[a].c(),o[a].m(e,null))}for(;a<o.length;a+=1)o[a].d(1);o.length=i.length}r[0]&8192&&l!==(l="grid gap-2 "+n[13]+" svelte-1g9btlg")&&g(e,"class",l),r[0]&8194&&B(e,"pt-6",n[1])},i:E,o:E,d(n){n&&G(e),ie(o,n)}}}function Se(t){let e,l,i,o;return i=new U({}),{c(){e=v("div"),l=v("div"),H(i.$$.fragment),g(l,"class","h-5 dark:text-white opacity-50"),g(e,"class","h-full min-h-[15rem] flex justify-center items-center")},m(n,r){C(n,e,r),y(e,l),I(i,l,null),o=!0},p:E,i(n){o||(w(i.$$.fragment,n),o=!0)},o(n){A(i.$$.fragment,n),o=!1},d(n){n&&G(e),N(i)}}}function x(t){let e,l,i=t[30]+"",o;return{c(){e=v("div"),l=v("div"),o=te(i),g(l,"class","bg-gray-50 dark:bg-gray-700 dark:text-gray-200 text-xs border-t border-l dark:border-gray-600 font-semibold px-3 py-1 rounded-tl-lg group-hover:opacity-50 max-w-full truncate"),g(e,"class","bottom-0 absolute z-[5] flex justify-end w-full")},m(n,r){C(n,e,r),y(e,l),y(l,o)},p(n,r){r[0]&1024&&i!==(i=n[30]+"")&&ne(o,i)},d(n){n&&G(e)}}}function ee(t){let e,l,i,o,n,r,a,m=t[30]&&x(t);function d(){return t[25](t[32])}return{c(){e=v("button"),l=v("img"),o=L(),m&&m.c(),n=L(),g(l,"alt",""),g(l,"class","h-full w-full overflow-hidden object-contain"),R(l.src,i=typeof t[29]=="string"?t[29]:t[29].data)||g(l,"src",i),g(e,"class","gallery-item group svelte-1g9btlg")},m(_,u){C(_,e,u),y(e,l),y(e,o),m&&m.m(e,null),y(e,n),r||(a=S(e,"click",d),r=!0)},p(_,u){t=_,u[0]&1024&&!R(l.src,i=typeof t[29]=="string"?t[29]:t[29].data)&&g(l,"src",i),t[30]?m?m.p(t,u):(m=x(t),m.c(),m.m(e,n)):m&&(m.d(1),m=null)},d(_){_&&G(e),m&&m.d(),r=!1,a()}}}function Te(t){let e,l,i,o,n,r,a;const m=[t[0]];let d={};for(let s=0;s<m.length;s+=1)d=ve(d,m[s]);e=new we({props:d});let _=t[1]&&W(t);const u=[Ie,He],h=[];function j(s,b){return s[5]===null||s[10]===null?0:1}return o=j(t),n=h[o]=u[o](t),{c(){H(e.$$.fragment),l=L(),_&&_.c(),i=L(),n.c(),r=ye()},m(s,b){I(e,s,b),C(s,l,b),_&&_.m(s,b),C(s,i,b),h[o].m(s,b),C(s,r,b),a=!0},p(s,b){const k=b[0]&1?je(m,[ze(s[0])]):{};e.$set(k),s[1]?_?(_.p(s,b),b[0]&2&&w(_,1)):(_=W(s),_.c(),w(_,1),_.m(i.parentNode,i)):_&&(q(),A(_,1,1,()=>{_=null}),M());let f=o;o=j(s),o===f?h[o].p(s,b):(q(),A(h[f],1,1,()=>{h[f]=null}),M(),n=h[o],n?n.p(s,b):(n=h[o]=u[o](s),n.c()),w(n,1),n.m(r.parentNode,r))},i(s){a||(w(e.$$.fragment,s),w(_),w(n),a=!0)},o(s){A(e.$$.fragment,s),A(_),A(n),a=!1},d(s){N(e,s),s&&G(l),_&&_.d(s),s&&G(i),h[o].d(s),s&&G(r)}}}function qe(t){let e,l,i,o;return le(t[19]),e=new Ge({props:{visible:t[4],variant:"solid",color:"grey",padding:!1,elem_id:t[3],disable:typeof t[6].container=="boolean"&&!t[6].container,$$slots:{default:[Te]},$$scope:{ctx:t}}}),{c(){H(e.$$.fragment)},m(n,r){I(e,n,r),l=!0,i||(o=S(window,"resize",t[19]),i=!0)},p(n,r){const a={};r[0]&16&&(a.visible=n[4]),r[0]&8&&(a.elem_id=n[3]),r[0]&64&&(a.disable=typeof n[6].container=="boolean"&&!n[6].container),r[0]&64999|r[1]&8&&(a.$$scope={dirty:r,ctx:n}),e.$set(a)},i(n){l||(w(e.$$.fragment,n),l=!0)},o(n){A(e.$$.fragment,n),l=!1},d(n){N(e,n),i=!1,o()}}}function Me(t,e,l){let i,o,n,r,a,{loading_status:m}=e,{show_label:d}=e,{label:_}=e,{root:u}=e,{elem_id:h=""}=e,{visible:j=!0}=e,{value:s=null}=e,{style:b={}}=e,k=null,f=null;function z(c){switch(c.code){case"Escape":c.preventDefault(),l(7,f=null);break;case"ArrowLeft":c.preventDefault(),l(7,f=o);break;case"ArrowRight":c.preventDefault(),l(7,f=n);break}}let p=[],D;async function oe(c){if(typeof c!="number")return;await Be(),p[c].focus();const{left:Q,width:ge}=D.getBoundingClientRect(),{left:he,width:be}=p[c].getBoundingClientRect(),V=he-Q+be/2-ge/2+D.scrollLeft;D.scrollTo({left:V<0?0:V,behavior:"smooth"})}let T=0,P=0;function ae(){l(9,P=window.innerHeight)}const se=()=>l(7,f=null),re=()=>l(7,f=n);function fe(c,Q){Y[c?"unshift":"push"](()=>{p[Q]=c,l(11,p)})}const ue=c=>l(7,f=c);function _e(c){Y[c?"unshift":"push"](()=>{D=c,l(12,D)})}const ce=c=>l(7,f=r?c:f);function me(){T=this.clientHeight,l(8,T)}return t.$$set=c=>{"loading_status"in c&&l(0,m=c.loading_status),"show_label"in c&&l(1,d=c.show_label),"label"in c&&l(2,_=c.label),"root"in c&&l(17,u=c.root),"elem_id"in c&&l(3,h=c.elem_id),"visible"in c&&l(4,j=c.visible),"value"in c&&l(5,s=c.value),"style"in c&&l(6,b=c.style)},t.$$.update=()=>{t.$$.dirty[0]&131104&&l(10,i=s===null?null:s.map(c=>Array.isArray(c)?[J(c[0],u),c[1]]:[J(c,u),null])),t.$$.dirty[0]&262176&&k!==s&&(l(7,f=null),l(18,k=s)),t.$$.dirty[0]&1152&&(o=((f??0)+(i?.length??0)-1)%(i?.length??0)),t.$$.dirty[0]&1152&&l(15,n=((f??0)+1)%(i?.length??0)),t.$$.dirty[0]&128&&oe(f),t.$$.dirty[0]&768&&l(14,r=P>=T),t.$$.dirty[0]&64&&l(13,{classes:a}=Re(b,["grid"]),a)},[m,d,_,h,j,s,b,f,T,P,i,p,D,a,r,n,z,u,k,ae,se,re,fe,ue,_e,ce,me]}class Ee extends de{constructor(e){super(),pe(this,e,Me,qe,ke,{loading_status:0,show_label:1,label:2,root:17,elem_id:3,visible:4,value:5,style:6},null,[-1,-1])}}var Oe=Ee;const We=["static"];export{Oe as Component,We as modes};

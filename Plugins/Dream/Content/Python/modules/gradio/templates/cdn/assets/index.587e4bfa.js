import{S as d,i as f,s as _,e as h,b as o,Y as g,d as c,f as w,w as m,n as k,E as v,c as M,m as y,j as C,k as E,o as H,J as L}from"./index.62d61aa4.js";function S(t){let e;return{c(){e=h("div"),o(e,"id",t[0]),o(e,"class","output-markdown gr-prose"),g(e,"max-width","100%"),c(e,"hidden",!t[1])},m(i,n){w(i,e,n),e.innerHTML=t[2]},p(i,[n]){n&4&&(e.innerHTML=i[2]),n&1&&o(e,"id",i[0]),n&2&&c(e,"hidden",!i[1])},i:m,o:m,d(i){i&&k(e)}}}function T(t,e,i){let{elem_id:n=""}=e,{visible:a=!0}=e,{value:l}=e;const r=v();return t.$$set=u=>{"elem_id"in u&&i(0,n=u.elem_id),"visible"in u&&i(1,a=u.visible),"value"in u&&i(2,l=u.value)},t.$$.update=()=>{t.$$.dirty&4&&r("change")},[n,a,l]}class j extends d{constructor(e){super(),f(this,e,T,S,_,{elem_id:0,visible:1,value:2})}}function q(t){let e,i;return e=new j({props:{value:t[2],elem_id:t[0],visible:t[1]}}),e.$on("change",t[4]),{c(){M(e.$$.fragment)},m(n,a){y(e,n,a),i=!0},p(n,[a]){const l={};a&4&&(l.value=n[2]),a&1&&(l.elem_id=n[0]),a&2&&(l.visible=n[1]),e.$set(l)},i(n){i||(C(e.$$.fragment,n),i=!0)},o(n){E(e.$$.fragment,n),i=!1},d(n){H(e,n)}}}function D(t,e,i){let{label:n}=e,{elem_id:a=""}=e,{visible:l=!0}=e,{value:r=""}=e;const u=v();function b(s){L.call(this,t,s)}return t.$$set=s=>{"label"in s&&i(3,n=s.label),"elem_id"in s&&i(0,a=s.elem_id),"visible"in s&&i(1,l=s.visible),"value"in s&&i(2,r=s.value)},t.$$.update=()=>{t.$$.dirty&8&&u("change")},[a,l,r,n,b]}class J extends d{constructor(e){super(),f(this,e,D,q,_,{label:3,elem_id:0,visible:1,value:2})}}var z=J;const A=["static"];export{z as Component,A as modes};
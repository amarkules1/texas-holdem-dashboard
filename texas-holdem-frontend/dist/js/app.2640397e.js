(function(){var s={5912:function(s,t,e){"use strict";var a=e(5688),r=e(6768);function n(s,t,e,a,n,i){const o=(0,r.g2)("HeaderComponent"),c=(0,r.g2)("CardStatsContainer");return(0,r.uX)(),(0,r.CE)(r.FK,null,[(0,r.bF)(o),(0,r.bF)(c)],64)}var i=e(5187);const o={class:"container"},c={class:"row"},d={class:"col-4"},u={class:"col-4"},l={class:"playerCtInput"},p=["value"],g={class:"col-4"},v={key:0,class:"cardSelectionHolder"};function m(s,t,e,n,m,f){const h=(0,r.g2)("SelectedCards"),k=(0,r.g2)("StatsDisplay"),_=(0,r.g2)("CardSelector");return(0,r.uX)(),(0,r.CE)(r.FK,null,[(0,r.Lk)("div",o,[(0,r.Lk)("div",c,[(0,r.Lk)("div",d,[(0,r.Lk)("button",{onClick:t[0]||(t[0]=(...s)=>f.backButton&&f.backButton(...s)),class:"btn btn-info back-btn"},"Back")]),(0,r.Lk)("div",u,[(0,r.Lk)("div",l,[t[5]||(t[5]=(0,r.Lk)("label",{for:"playerCount"},"Player Count: ",-1)),(0,r.bo)((0,r.Lk)("select",{"onUpdate:modelValue":t[1]||(t[1]=s=>m.playerCount=s),onChange:t[2]||(t[2]=(...s)=>f.getHandPerformance&&f.getHandPerformance(...s)),class:"form-select playerCtSelect"},[((0,r.uX)(),(0,r.CE)(r.FK,null,(0,r.pI)([2,3,4,5,6,7,8,9,10,11,12],(s=>(0,r.Lk)("option",{key:s,value:s},(0,i.v_)(s),9,p))),64))],544),[[a.u1,m.playerCount]])])]),(0,r.Lk)("div",g,[(0,r.Lk)("button",{onClick:t[3]||(t[3]=(...s)=>f.reset&&f.reset(...s)),class:"btn btn-warning reset-btn"},"Reset")])])]),(0,r.Lk)("div",null,[(0,r.bF)(h,{holeCards:m.holeCards,communityCards:m.communityCards},null,8,["holeCards","communityCards"]),(0,r.Lk)("div",null,[(0,r.bF)(k,{perf:m.perf,"card-count":m.cards.length},null,8,["perf","card-count"])]),m.cards.length<7?((0,r.uX)(),(0,r.CE)("div",v,[(0,r.bF)(_,{cardToSelect:f.getCardName(),disabledCards:m.cards,onSelectCard:t[4]||(t[4]=(s,t)=>f.selectCard(s,t))},null,8,["cardToSelect","disabledCards"])])):(0,r.Q3)("",!0)])],64)}e(4114);const f={class:"cardSelector"},h=["onClick"],k=["src"];function _(s,t,a,n,o,c){return(0,r.uX)(),(0,r.CE)("div",f,[(0,r.Lk)("h3",null,"Select the "+(0,i.v_)(a.cardToSelect),1),((0,r.uX)(!0),(0,r.CE)(r.FK,null,(0,r.pI)(o.suits,(s=>((0,r.uX)(),(0,r.CE)("div",{key:s,class:"suitRow"},[((0,r.uX)(!0),(0,r.CE)(r.FK,null,(0,r.pI)(o.ranks,(t=>((0,r.uX)(),(0,r.CE)("div",{key:t,class:(0,i.C4)({card:!0,disabled:a.disabledCards.some((e=>e.rank==t&&e.suit==s))}),onClick:e=>c.selectCard(t,s)},[(0,r.Lk)("img",{class:"cardImage",src:e(87)(`./${s}_${t}.svg`),alt:"card"},null,8,k)],10,h)))),128))])))),128))])}var C={name:"CardSelector",data(){return{rank:"",suit:"",ranks:["2","3","4","5","6","7","8","9","10","jack","queen","king","ace"],suits:["clubs","diamonds","hearts","spades"]}},props:{disabledCards:{type:Array,default:()=>[]},cardToSelect:{type:String,default:""}},methods:{selectCard(s,t){this.disabledCards.some((e=>e.rank==s&&e.suit==t))||(this.rank=s,this.suit=t,this.$emit("selectCard",s,t))}},emits:["selectCard"]},b=e(1241);const y=(0,b.A)(C,[["render",_],["__scopeId","data-v-6ea9ed08"]]);var x=y;const L={class:"cardsDisplay"},w={class:"cards"},S={class:"holeCards"},F={key:0,class:"noshow"},E=["src"],j={key:1,class:"noshow"},X=["src"],T={class:"communityCards"},I={key:0,class:"noshow"},O=["src"],$={key:1},A=["src"];function N(s,t,a,n,i,o){return(0,r.uX)(),(0,r.CE)("div",L,[(0,r.Lk)("div",w,[(0,r.Lk)("div",S,[t[0]||(t[0]=(0,r.Lk)("h4",null,"Hole Cards",-1)),((0,r.uX)(),(0,r.CE)(r.FK,null,(0,r.pI)([0,1],(s=>(0,r.Lk)("div",{key:s,class:"playingCard"},[s<a.holeCards.length?((0,r.uX)(),(0,r.CE)("div",F,[(0,r.Lk)("img",{class:"cardImage",src:e(87)(`./${a.holeCards[s].suit}_${a.holeCards[s].rank}.svg`),alt:"card"},null,8,E)])):((0,r.uX)(),(0,r.CE)("div",j,[(0,r.Lk)("img",{class:"cardImage",src:e(515),alt:"card"},null,8,X)]))]))),64))]),(0,r.Lk)("div",T,[t[1]||(t[1]=(0,r.Lk)("h4",null,"Community Cards",-1)),((0,r.uX)(),(0,r.CE)(r.FK,null,(0,r.pI)([0,1,2,3,4],(s=>(0,r.Lk)("div",{key:s,class:"playingCard"},[s<a.communityCards.length?((0,r.uX)(),(0,r.CE)("div",I,[(0,r.Lk)("img",{class:"cardImage",src:e(87)(`./${a.communityCards[s].suit}_${a.communityCards[s].rank}.svg`),alt:"card"},null,8,O)])):((0,r.uX)(),(0,r.CE)("div",$,[(0,r.Lk)("img",{class:"cardImage",src:e(515),alt:"card"},null,8,A)]))]))),64))])])])}var H={name:"SelectedCards",props:{holeCards:{type:Array,default:()=>[]},communityCards:{type:Array,default:()=>[]}}};const K=(0,b.A)(H,[["render",N],["__scopeId","data-v-a8fcf52a"]]);var P=K;const R={class:"statsDisplay"},B={class:"stats"},q={class:"container statsContainer"},D={key:0},M={class:"row"},U={class:"col-sm"},Q={class:"col-sm"},W={class:"col-sm"},z={key:0,class:"row"},G={class:"col-sm"},V={class:"col-sm"};function Y(s,t,e,a,n,o){return(0,r.uX)(),(0,r.CE)("div",R,[(0,r.Lk)("div",B,[(0,r.Lk)("div",q,[e.perf&&e.perf.current_win_rate?((0,r.uX)(),(0,r.CE)("div",D,[(0,r.Lk)("div",null,[(0,r.Lk)("div",M,[(0,r.Lk)("div",U,[(0,r.Lk)("h5",null,"Current Win Rate: "+(0,i.v_)(e.perf.current_win_rate?e.perf.current_win_rate.toFixed(3):"N/A"),1)]),(0,r.Lk)("div",Q,[(0,r.Lk)("h5",null,"Kelly Criterion: "+(0,i.v_)(e.perf.ideal_kelly_max>0?(100*e.perf.ideal_kelly_max).toFixed(3):0)+"%",1)]),(0,r.Lk)("div",W,[(0,r.Lk)("h5",null,"Percentile: "+(0,i.v_)(e.perf.percentile?e.perf.percentile.toFixed(3):"N/A")+"%",1)])])]),(0,r.Lk)("div",null,[e.cardCount<5?((0,r.uX)(),(0,r.CE)("div",z,[(0,r.Lk)("div",G,[(0,r.Lk)("h5",null,"Sklansky Rank: "+(0,i.v_)(e.perf.sklansky),1)]),t[0]||(t[0]=(0,r.Lk)("div",{class:"col-sm"},null,-1)),(0,r.Lk)("div",V,[(0,r.Lk)("h5",null,"Sklansky Playability: "+(0,i.v_)(e.perf.sklansky_position),1)])])):(0,r.Q3)("",!0)])])):(0,r.Q3)("",!0)])])])}var J={name:"StatsDisplay",props:{perf:Object,cardCount:Number}};const Z=(0,b.A)(J,[["render",Y],["__scopeId","data-v-54286c0b"]]);var ss=Z,ts=e(4373),es={name:"CardStatsContainer",components:{CardSelector:x,SelectedCards:P,StatsDisplay:ss},data(){return{holeCards:[],communityCards:[],cards:[],playerCount:2,perf:null,selections:["First Hole Card","Second Hole Card","First Flop Card","Second Flop Card","Third Flop Card","Turn Card","River Card"]}},methods:{selectCard(s,t){this.holeCards.length<2?this.holeCards.push({rank:s,suit:t}):this.communityCards.length<5&&this.communityCards.push({rank:s,suit:t}),this.cards.push({rank:s,suit:t}),this.getHandPerformance()},getCardName(){return this.selections[this.cards.length]},backButton(){this.cards.length>0&&this.cards.pop(),this.communityCards.length>0?this.communityCards.pop():this.holeCards.length>0&&this.holeCards.pop(),this.perf=null,this.getHandPerformance()},reset(){this.cards=[],this.holeCards=[],this.communityCards=[],this.perf=null},async getHandPerformance(){if(this.cards.length<2)return;let s="/card-stats?";s+=`card1=${this.getCardNameForBackend(this.cards[0].rank,this.cards[0].suit)}`,s+=`&card2=${this.getCardNameForBackend(this.cards[1].rank,this.cards[1].suit)}`,this.communityCards.length>2&&(s+=`&flop1=${this.getCardNameForBackend(this.communityCards[0].rank,this.communityCards[0].suit)}`,s+=`&flop2=${this.getCardNameForBackend(this.communityCards[1].rank,this.communityCards[1].suit)}`,s+=`&flop3=${this.getCardNameForBackend(this.communityCards[2].rank,this.communityCards[2].suit)}`),this.communityCards.length>3&&(s+=`&turn=${this.getCardNameForBackend(this.communityCards[3].rank,this.communityCards[3].suit)}`),this.communityCards.length>4&&(s+=`&river=${this.getCardNameForBackend(this.communityCards[4].rank,this.communityCards[4].suit)}`),s+=`&player_count=${this.playerCount}`;const t=await ts.A.get(s);this.perf=t.data},getCardNameForBackend(s,t){let e=s;e.length>2&&(e=e[0].toUpperCase());let a=t.charAt(0).toUpperCase()+t.slice(1);return`${e} of ${a}`}}};const as=(0,b.A)(es,[["render",m],["__scopeId","data-v-a12d98ea"]]);var rs=as,ns=e(1798),is=e(8249),os=e(2353);const cs={class:"header"},ds={class:"container"},us={class:"row"},ls={class:"col-sm-2"},ps={class:"buttons"},gs={key:0,class:"info-bg"},vs={class:"info-container"};var ms={__name:"HeaderComponent",setup(s){const t=(0,ns.KR)(!1);return(s,e)=>((0,r.uX)(),(0,r.CE)(r.FK,null,[(0,r.Lk)("div",cs,[(0,r.Lk)("div",ds,[(0,r.Lk)("div",us,[e[2]||(e[2]=(0,r.Lk)("div",{class:"col-sm-2"},null,-1)),e[3]||(e[3]=(0,r.Lk)("div",{class:"col-sm-8"},[(0,r.Lk)("h1",null,"Texas Hold'em Dashboard")],-1)),(0,r.Lk)("div",ls,[(0,r.Lk)("div",ps,[(0,r.bF)((0,ns.R1)(is.gc),{icon:(0,ns.R1)(os.iW_),size:"2x",onClick:e[0]||(e[0]=s=>t.value=!t.value)},null,8,["icon"])])])])])]),t.value?((0,r.uX)(),(0,r.CE)("div",gs,[(0,r.Lk)("div",vs,[(0,r.Lk)("div",{class:"info-close",onClick:e[1]||(e[1]=s=>t.value=!t.value)},[(0,r.bF)((0,ns.R1)(is.gc),{icon:(0,ns.R1)(os.GRI),size:"lg"},null,8,["icon"])]),e[4]||(e[4]=(0,r.Fv)('<div class="info-text" data-v-f5678006><h3 data-v-f5678006>Instructions</h3><p data-v-f5678006>Welcome to Texas Hold&#39;em! This dashboard provides statistics about your poker hand at any point in the game. <br data-v-f5678006> To see stats about a particular scenario, select your hole (hand) cards and any known community cards. The following statistics will be displayed:</p><ul class="info-descriptions list-group" data-v-f5678006><li class="list-group-item" data-v-f5678006><strong data-v-f5678006>Current Win Rate:</strong> Expected win rate against (as a proportion) random hands, based on the number of players, your hand, and any known community cards. This win rate assumes other players have a random hand, which may become a less accurate estimate as the game progresses and players with worse hands fold, but it still gives you an idea of the relative strength of your hand. </li><li class="list-group-item" data-v-f5678006><strong data-v-f5678006>Kelly Criterion:</strong> The percentage of your chips that you should bet based on the strength of your hand. The <a href="https://en.wikipedia.org/wiki/Kelly_criterion" data-v-f5678006>Kelly Criterion</a> is based on the number of players and the current win rate, so the same caveats apply. You may find that a smaller amount (e.g. 1/2 or 1/3 of the Kelly Criterion) is a better bet. </li><li class="list-group-item" data-v-f5678006><strong data-v-f5678006>Percentile:</strong> Relative ranking (as a percentile) against all other hands at the current point. </li><li class="list-group-item" data-v-f5678006><strong data-v-f5678006>Sklansky Rank:</strong> Number from 1 to 9 indicating the strength of your hand pre-flop, based on <a href="https://en.wikipedia.org/wiki/Texas_hold_%27em_starting_hands#Sklansky_hand_groups" data-v-f5678006>Sklansky Hand Groups</a>. </li><li class="list-group-item" data-v-f5678006><strong data-v-f5678006>Sklansky Position:</strong> Description of the Sklansky hand rank, the position and scenario in which you should play it. </li></ul><br data-v-f5678006><p data-v-f5678006>Author: <a href="http://marqless.xyz" data-v-f5678006>Alex Markules</a></p></div>',1))])])):(0,r.Q3)("",!0)],64))}};const fs=(0,b.A)(ms,[["__scopeId","data-v-f5678006"]]);var hs=fs,ks={name:"App",components:{CardStatsContainer:rs,HeaderComponent:hs}};const _s=(0,b.A)(ks,[["render",n]]);var Cs=_s;e(9313);(0,a.Ef)(Cs).mount("#app")},87:function(s,t,e){var a={"./clubs_10.svg":7283,"./clubs_2.svg":3586,"./clubs_3.svg":6227,"./clubs_4.svg":2188,"./clubs_5.svg":1901,"./clubs_6.svg":2782,"./clubs_7.svg":3887,"./clubs_8.svg":1e3,"./clubs_9.svg":5865,"./clubs_ace.svg":3181,"./clubs_jack.svg":1121,"./clubs_king.svg":3677,"./clubs_queen.svg":8742,"./diamonds_10.svg":4879,"./diamonds_2.svg":9318,"./diamonds_3.svg":6439,"./diamonds_4.svg":2984,"./diamonds_5.svg":905,"./diamonds_6.svg":154,"./diamonds_7.svg":4347,"./diamonds_8.svg":6732,"./diamonds_9.svg":7357,"./diamonds_ace.svg":2281,"./diamonds_jack.svg":5933,"./diamonds_king.svg":9942,"./diamonds_queen.svg":5578,"./hearts_10.svg":2299,"./hearts_2.svg":8362,"./hearts_3.svg":7419,"./hearts_4.svg":5268,"./hearts_5.svg":9989,"./hearts_6.svg":854,"./hearts_7.svg":8391,"./hearts_8.svg":2912,"./hearts_9.svg":5713,"./hearts_ace.svg":7301,"./hearts_jack.svg":5769,"./hearts_king.svg":2469,"./hearts_queen.svg":830,"./joker_black.svg":5299,"./joker_red.svg":4303,"./spades_10.svg":8324,"./spades_2.svg":8543,"./spades_3.svg":3902,"./spades_4.svg":5457,"./spades_5.svg":7424,"./spades_6.svg":2083,"./spades_7.svg":8354,"./spades_8.svg":6053,"./spades_9.svg":8804,"./spades_ace.svg":9688,"./spades_jack.svg":1238,"./spades_king.svg":8322,"./spades_queen.svg":4659};function r(s){var t=n(s);return e(t)}function n(s){if(!e.o(a,s)){var t=new Error("Cannot find module '"+s+"'");throw t.code="MODULE_NOT_FOUND",t}return a[s]}r.keys=function(){return Object.keys(a)},r.resolve=n,s.exports=r,r.id=87},7283:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_10.f825a315.svg"},3586:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_2.9c66a404.svg"},6227:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_3.4e06bb90.svg"},2188:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_4.f137529e.svg"},1901:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_5.280b524d.svg"},2782:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_6.db1f3824.svg"},3887:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_7.03987df1.svg"},1e3:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_8.0bf09550.svg"},5865:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_9.eb52831f.svg"},3181:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_ace.7461a163.svg"},1121:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_jack.7e7da317.svg"},3677:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_king.6c7a9d26.svg"},8742:function(s,t,e){"use strict";s.exports=e.p+"img/clubs_queen.5977106e.svg"},4879:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_10.13069658.svg"},9318:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_2.e91129bd.svg"},6439:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_3.48fbd9cb.svg"},2984:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_4.1d08cf6f.svg"},905:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_5.a1b332cb.svg"},154:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_6.2f8c4ff6.svg"},4347:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_7.7f375746.svg"},6732:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_8.6e2f4549.svg"},7357:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_9.7ea82b7f.svg"},2281:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_ace.1e70c463.svg"},5933:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_jack.e0e28e41.svg"},9942:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_king.68f132cc.svg"},5578:function(s,t,e){"use strict";s.exports=e.p+"img/diamonds_queen.7e3be289.svg"},515:function(s,t,e){"use strict";s.exports=e.p+"img/gray.d46eee60.svg"},2299:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_10.9da4c145.svg"},8362:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_2.d48a1419.svg"},7419:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_3.3cfe8223.svg"},5268:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_4.601c1a77.svg"},9989:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_5.0dab2dcd.svg"},854:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_6.2e19dc5e.svg"},8391:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_7.c01af87a.svg"},2912:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_8.d2143873.svg"},5713:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_9.bfdd503b.svg"},7301:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_ace.88603754.svg"},5769:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_jack.beb608aa.svg"},2469:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_king.b36cefe2.svg"},830:function(s,t,e){"use strict";s.exports=e.p+"img/hearts_queen.f9348cb6.svg"},5299:function(s,t,e){"use strict";s.exports=e.p+"img/joker_black.a6a560af.svg"},4303:function(s,t,e){"use strict";s.exports=e.p+"img/joker_red.88be2e1a.svg"},8324:function(s,t,e){"use strict";s.exports=e.p+"img/spades_10.fab4ad29.svg"},8543:function(s,t,e){"use strict";s.exports=e.p+"img/spades_2.2983d8d7.svg"},3902:function(s,t,e){"use strict";s.exports=e.p+"img/spades_3.07360a9c.svg"},5457:function(s,t,e){"use strict";s.exports=e.p+"img/spades_4.eaa27366.svg"},7424:function(s,t,e){"use strict";s.exports=e.p+"img/spades_5.79ab65fc.svg"},2083:function(s,t,e){"use strict";s.exports=e.p+"img/spades_6.e68c8ff0.svg"},8354:function(s,t,e){"use strict";s.exports=e.p+"img/spades_7.206535b1.svg"},6053:function(s,t,e){"use strict";s.exports=e.p+"img/spades_8.fdff4def.svg"},8804:function(s,t,e){"use strict";s.exports=e.p+"img/spades_9.5ad5b13a.svg"},9688:function(s,t,e){"use strict";s.exports=e.p+"img/spades_ace.07f12791.svg"},1238:function(s,t,e){"use strict";s.exports=e.p+"img/spades_jack.b4395b81.svg"},8322:function(s,t,e){"use strict";s.exports=e.p+"img/spades_king.0e16698f.svg"},4659:function(s,t,e){"use strict";s.exports=e.p+"img/spades_queen.70277069.svg"}},t={};function e(a){var r=t[a];if(void 0!==r)return r.exports;var n=t[a]={exports:{}};return s[a].call(n.exports,n,n.exports,e),n.exports}e.m=s,function(){var s=[];e.O=function(t,a,r,n){if(!a){var i=1/0;for(u=0;u<s.length;u++){a=s[u][0],r=s[u][1],n=s[u][2];for(var o=!0,c=0;c<a.length;c++)(!1&n||i>=n)&&Object.keys(e.O).every((function(s){return e.O[s](a[c])}))?a.splice(c--,1):(o=!1,n<i&&(i=n));if(o){s.splice(u--,1);var d=r();void 0!==d&&(t=d)}}return t}n=n||0;for(var u=s.length;u>0&&s[u-1][2]>n;u--)s[u]=s[u-1];s[u]=[a,r,n]}}(),function(){e.n=function(s){var t=s&&s.__esModule?function(){return s["default"]}:function(){return s};return e.d(t,{a:t}),t}}(),function(){e.d=function(s,t){for(var a in t)e.o(t,a)&&!e.o(s,a)&&Object.defineProperty(s,a,{enumerable:!0,get:t[a]})}}(),function(){e.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(s){if("object"===typeof window)return window}}()}(),function(){e.o=function(s,t){return Object.prototype.hasOwnProperty.call(s,t)}}(),function(){e.r=function(s){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(s,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(s,"__esModule",{value:!0})}}(),function(){e.p="/"}(),function(){var s={524:0};e.O.j=function(t){return 0===s[t]};var t=function(t,a){var r,n,i=a[0],o=a[1],c=a[2],d=0;if(i.some((function(t){return 0!==s[t]}))){for(r in o)e.o(o,r)&&(e.m[r]=o[r]);if(c)var u=c(e)}for(t&&t(a);d<i.length;d++)n=i[d],e.o(s,n)&&s[n]&&s[n][0](),s[n]=0;return e.O(u)},a=self["webpackChunktexas_holdem_frontend"]=self["webpackChunktexas_holdem_frontend"]||[];a.forEach(t.bind(null,0)),a.push=t.bind(null,a.push.bind(a))}();var a=e.O(void 0,[504],(function(){return e(5912)}));a=e.O(a)})();
//# sourceMappingURL=app.2640397e.js.map
#  Scroll Convert Plugin
#
#  Copyright (C) 2016 Noah Greenstein 
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Based on:
#  Convert Special Plugin, Copyright - (C) 2012 Marco Crippa

from gi.repository import GObject, Gtk, Gedit, PeasGtk, Gio

# settings

lset = [
    ["ascii",True], 
    ["hexa",False], 
    ["dec",False], 
    ["html",True], 
    ["latex",False]
]

actions = ["sconvert", "<Alt>v", "Language Scroll"]  # %

d = [ 

    ['"', "&#x22;", "&#34;", "&quot;", ""],
    ["$", "&#x24;", "&#36;", "&#36;", "\$"],
    ["%", "&#x25;", "&#37;", "&#37;", "\%"],
    ["&", "&#x26;", "&#38;", "&amp;", "\&"],
    ["<", "&#x3c;", "&#60;", "&lt;", "\\textless"],
    [">", "&#x3e;", "&#62;", "&gt;", "\\textgreater"],
    ["?", "&#x3f;", "&#63;", "&#63;", ""],
    ["@", "&#x40;", "&#64;", "&#64;", ""],
    ["[", "&#x5b;", "&#91;", "&#91;", ""],
    ["\\", "&#x5c;", "&#92;", "&#92;", "\\backslash"],
    ["]", "&#x5d;", "&#93;", "&#93;", ""],
    ["^", "&#x5e;", "&#94;", "&#94;", "\^{}"],
    ["_", "&#x5f;", "&#95;", "&#95;", "\_{}"],
    ["`", "&#x60;", "&#96;", "&#96;", ""],

    ["{", "&#x7b;", "&#123;", "&#123;", "\{"],
    ["|", "&#x7c;", "&#124;", "&#124;", "\\textbar"],
    ["}", "&#x7d;", "&#125;", "&#125;", "\}"],
    ["~", "&#x7e;", "&#126;", "&tilde;", "\~{}"],

    [" ", "&#xa0;", "&#160;", "&nbsp;", "~"],
    ["¡", "&#xa1;", "&#161;", "&iexcl;", "\\textexclamdown"],
    ["¢", "&#xa2;", "&#162;", "&cent;", "\\textcent"],
    ["£", "&#xa3;", "&#163;", "&pound;", "\pounds"],
    ["¤", "&#xa4;", "&#164;", "&curren;", "\currency"],
    ["¥", "&#xa5;", "&#165;", "&yen;", "\yen"],
    ["¦", "&#xa6;", "&#166;", "&brvbar;", ""],
    ["§", "&#xa7;", "&#167;", "&sect;", "\S"],
    ["¨", "&#xa8;", "&#168;", "&uml;", "\\\"{}"],
    ["©", "&#xa9;", "&#169;", "&copy;", "\copyright"],
    ["ª", "&#xaa;", "&#170;", "&ordf;", "\\textordfeminine"],
    ["«", "&#xab;", "&#171;", "&laquo;", "\guillemotleft"],
    ["¬", "&#xac;", "&#172;", "&not;", "\\neg"],
    ["®", "&#xae;", "&#174;", "&reg;", "\\textregistered"],
    ["¯", "&#xaf;", "&#175;", "&macr;", "\\bar"],
    ["°", "&#xb0;", "&#176;", "&deg;", "\\textdegree"],
    ["±", "&#xb1;", "&#177;", "&plusmn;", "\pm"],
    ["²", "&#xb2;", "&#178;", "&sup2;", "^{2}"],
    ["³", "&#xb3;", "&#179;", "&sup3;", "^{3}"],
    ["´", "&#xb4;", "&#180;", "&acute;", "'"],
    ["µ", "&#xb5;", "&#181;", "&micro;", "\Micro"],
    ["¶", "&#xb6;", "&#182;", "&para;", "\P"],
    ["·", "&#xb7;", "&#183;", "&middot;", "\cdot"],
    ["¸", "&#xb8;", "&#184;", "&cedil;", "\c{}"],
    ["¹", "&#xb9;", "&#185;", "&sup1;", "^{1}"],
    ["º", "&#xba;", "&#186;", "&ordm;", "\\textordmasculine"],
    ["»", "&#xbb;", "&#187;", "&raquo;", "\guillemotright"],
    ["¼", "&#xbc;", "&#188;", "&frac14;", "\\frac{1}{4}"],
    ["½", "&#xbd;", "&#189;", "&frac12;", "\\frac{1}{2}"],
    ["¾", "&#xbe;", "&#190;", "&frac34;", "\\frac{3}{4}"],
    ["¿", "&#xbf;", "&#191;", "&iquest;", "\\textquestiondown"],
    ["À", "&#xc0;", "&#192;", "&Agrave;", "\`A"],
    ["Á", "&#xc1;", "&#193;", "&Aacute;", "\\'A"],
    ["Â", "&#xc2;", "&#194;", "&Acirc;", "\^{A}"],
    ["Ã", "&#xc3;", "&#195;", "&Atilde;", "\~{A}"],
    ["Ä", "&#xc4;", "&#196;", "&Auml;", "\\\"{A}"],
    ["Å", "&#xc5;", "&#197;", "&Aring;", "\\r{A}"],
    ["Æ", "&#xc6;", "&#198;", "&AElig;", "\AE"],
    ["Ç", "&#xc7;", "&#199;", "&Ccedil;", "\c{C}"],
    ["È", "&#xc8;", "&#200;", "&Egrave;", "\`{E}"],
    ["É", "&#xc9;", "&#201;", "&Eacute;", "\\'{E}"],
    ["Ê", "&#xca;", "&#202;", "&Ecirc;", "\^{E}"],
    ["Ë", "&#xcb;", "&#203;", "&Euml;", "\\\"{E}"],
    ["Ì", "&#xcc;", "&#204;", "&Igrave;", "\`{I}"],
    ["Í", "&#xcd;", "&#205;", "&Iacute;", "\\'{I}"],
    ["Î", "&#xce;", "&#206;", "&Icirc;", "\^{I}"],
    ["Ï", "&#xcf;", "&#207;", "&Iuml;", "\\\"{I}"],
    ["Ð", "&#xd0;", "&#208;", "&ETH;", "\eth"],
    ["Ñ", "&#xd1;", "&#209;", "&Ntilde;", "\~{N}"],
    ["Ò", "&#xd2;", "&#210;", "&Ograve;", "\`{O}"],
    ["Ó", "&#xd3;", "&#211;", "&Oacute;", "\\'{O}"],
    ["Ô", "&#xd4;", "&#212;", "&Ocirc;", "\^{O}"],
    ["Õ", "&#xd5;", "&#213;", "&Otilde;", "\~{O}"],
    ["Ö", "&#xd6;", "&#214;", "&Ouml;", "\\\"{O}"],
    ["×", "&#xd7;", "&#215;", "&times;", "\\times"],
    ["Ø", "&#xd8;", "&#216;", "&Oslash;", "{\O}"],
    ["Ù", "&#xd9;", "&#217;", "&Ugrave;", "\`{U}"],
    ["Ú", "&#xda;", "&#218;", "&Uacute;", "\\'{U}"],
    ["Û", "&#xdb;", "&#219;", "&Ucirc;", "\^{U}"],
    ["Ü", "&#xdc;", "&#220;", "&Uuml;", "\\\"{U}"],
    ["Ý", "&#xdd;", "&#221;", "&Yacute;", "\\'{Y}"],
    ["Þ", "&#xde;", "&#222;", "&THORN;", "\TH"],
    ["ß", "&#xdf;", "&#223;", "&szlig;", "\ss"],
    ["à", "&#xe0;", "&#224;", "&agrave;", "\`{a}"],
    ["á", "&#xe1;", "&#225;", "&aacute;", "\\'{a}"],
    ["â", "&#xe2;", "&#226;", "&acirc;", "\^{a}"],
    ["ã", "&#xe3;", "&#227;", "&atilde;", "\~{a}"],
    ["ä", "&#xe4;", "&#228;", "&auml;", "\\\"{a}"],
    ["å", "&#xe5;", "&#229;", "&aring;", "\\r{a}"],
    ["æ", "&#xe6;", "&#230;", "&aelig;", "\\ae"],
    ["ç", "&#xe7;", "&#231;", "&ccedil;", "\c{c}"],
    ["è", "&#xe8;", "&#232;", "&egrave;", "\`{e}"],
    ["é", "&#xe9;", "&#233;", "&eacute;", "\\'{e}"],
    ["ê", "&#xea;", "&#234;", "&ecirc;", "\^{e}"],
    ["ë", "&#xeb;", "&#235;", "&euml;", "\\\"{e}"],
    ["ì", "&#xec;", "&#236;", "&igrave;", "\`{i}"],
    ["í", "&#xed;", "&#237;", "&iacute;", "\\'{i}"],
    ["î", "&#xee;", "&#238;", "&icirc;", "\^{i}"],
    ["ï", "&#xef;", "&#239;", "&iuml;", "\\\"{i}"],
    ["ð", "&#xf0;", "&#240;", "&eth;", "\eth"],
    ["ñ", "&#xf1;", "&#241;", "&ntilde;", "\~{n}"],
    ["ò", "&#xf2;", "&#242;", "&ograve;", "\`{o}"],
    ["ó", "&#xf3;", "&#243;", "&oacute;", "\\'{o}"],
    ["ô", "&#xf4;", "&#244;", "&ocirc;", "\^{o}"],
    ["õ", "&#xf5;", "&#245;", "&otilde;", "\~{o}"],
    ["ö", "&#xf6;", "&#246;", "&ouml;", "\\\"{o}"],
    ["÷", "&#xf7;", "&#247;", "&divide;", "\\textdiv"],
    ["ø", "&#xf8;", "&#248;", "&oslash;", "{\o}"],
    ["ù", "&#xf9;", "&#249;", "&ugrave;", "\`{u}"],
    ["ú", "&#xfa;", "&#250;", "&uacute;", "\\'{u}"],
    ["û", "&#xfb;", "&#251;", "&ucirc;", "\^{u}"],
    ["ü", "&#xfc;", "&#252;", "&uuml;", "\\\"{u}"],
    ["ý", "&#xfd;", "&#253;", "&yacute;", "\\'{y}"],
    ["þ", "&#xfe;", "&#254;", "&thorn;", "\\th"],
    ["ÿ", "&#xff;", "&#255;", "&yuml;", "\\\"{y}"],
    ["Ā", "&#x100;", "&#256;", "&#256;", "\={A}"],
    ["ā", "&#x101;", "&#257;", "&#257;", "\={a}"],
    ["Ă", "&#x102;", "&#258;", "&#258;", "\\u{A}"],
    ["ă", "&#x103;", "&#259;", "&#259;", "\\u{a}"],
    ["Ą", "&#x104;", "&#260;", "&#260;", "\k{A}"],
    ["ą", "&#x105;", "&#261;", "&#261;", "\k{a}"],
    ["Ć", "&#x106;", "&#262;", "&#262;", "\\'{C}"],
    ["ć", "&#x107;", "&#263;", "&#263;", "\\'{c}"],
    ["Ĉ", "&#x108;", "&#264;", "&#264;", "\^{C}"],
    ["ĉ", "&#x109;", "&#265;", "&#265;", "\^{c}"],
    ["Ċ", "&#x10a;", "&#266;", "&#266;", "\.{C}"],
    ["ċ", "&#x10b;", "&#267;", "&#267;", "\.{c}"],
    ["Č", "&#x10c;", "&#268;", "&#268;", "\\v{C}"],
    ["č", "&#x10d;", "&#269;", "&#269;", "\\v{c}"],
    ["Ď", "&#x10e;", "&#270;", "&#270;", "\\v{D}"],
    ["ď", "&#x10f;", "&#271;", "&#271;", "\\v{d}"],
    ["Đ", "&#x110;", "&#272;", "&#272;", "\DJ"],
    ["đ", "&#x111;", "&#273;", "&#273;", "\dj"],
    ["Ē", "&#x112;", "&#274;", "&#274;", "\={E}"],
    ["ē", "&#x113;", "&#275;", "&#275;", "\={e}"],
    ["Ĕ", "&#x114;", "&#276;", "&#276;", "\\u{E}"],
    ["ĕ", "&#x115;", "&#277;", "&#277;", "\\u{e}"],
    ["Ė", "&#x116;", "&#278;", "&#278;", "\.{E}"],
    ["ė", "&#x117;", "&#279;", "&#279;", "\.{e}"],
    ["Ę", "&#x118;", "&#280;", "&#280;", "\k{E}"],
    ["ę", "&#x119;", "&#281;", "&#281;", "\k{e}"],
    ["Ě", "&#x11a;", "&#282;", "&#282;", "\\v{E}"],
    ["ě", "&#x11b;", "&#283;", "&#283;", "\\v{e}"],
    ["Ĝ", "&#x11c;", "&#284;", "&#284;", "\^{G}"],
    ["ĝ", "&#x11d;", "&#285;", "&#285;", "\^{g}"],
    ["Ğ", "&#x11e;", "&#286;", "&#286;", "\\u{G}"],
    ["ğ", "&#x11f;", "&#287;", "&#287;", "\\u{g}"],
    ["Ġ", "&#x120;", "&#288;", "&#288;", "\.{G}"],
    ["ġ", "&#x121;", "&#289;", "&#289;", "\.{g}"],
    ["Ģ", "&#x122;", "&#290;", "&#290;", "\c{G}"],
    ["ģ", "&#x123;", "&#291;", "&#291;", "\c{g}"],
    ["Ĥ", "&#x124;", "&#292;", "&#292;", "\^{H}"],
    ["ĥ", "&#x125;", "&#293;", "&#293;", "\^{h}"],
    ["Ħ", "&#x126;", "&#294;", "&#294;", "\B{H}"],
    ["ħ", "&#x127;", "&#295;", "&#295;", "\B{h}"],
    ["Ĩ", "&#x128;", "&#296;", "&#296;", "\~{I}"],
    ["ĩ", "&#x129;", "&#297;", "&#297;", "\~{i}"],
    ["Ī", "&#x12a;", "&#298;", "&#298;", "\={I}"],
    ["ī", "&#x12b;", "&#299;", "&#299;", "\={i}"],
    ["Į", "&#x12c;", "&#300;", "&#300;", "\\u{I}"],
    ["ĭ", "&#x12d;", "&#301;", "&#301;", "\\u{i}"],
    ["Į", "&#x12e;", "&#302;", "&#302;", "\k{I}"],
    ["į", "&#x12f;", "&#303;", "&#303;", "\k{i}"],
    ["İ", "&#x130;", "&#304;", "&#304;", "\.{I}"],
    ["ı", "&#x131;", "&#305;", "&#305;", "\i"],
    ["IJ", "&#x132;", "&#306;", "&#306;", "\IJ"],
    ["ij", "&#x133;", "&#307;", "&#307;", "\ij"],
    ["Ĵ", "&#x134;", "&#308;", "&#308;", "\^{J}"],
    ["ĵ", "&#x135;", "&#309;", "&#309;", "\^{j}"],
    ["Ķ", "&#x136;", "&#310;", "&#310;", "\c{K}"],
    ["ķ", "&#x137;", "&#311;", "&#311;", "\c{k}"],
    ["Ĺ", "&#x139;", "&#313;", "&#313;", "\\'{L}"],
    ["ĺ", "&#x13a;", "&#314;", "&#314;", "\\'{l}"],
    ["Ļ", "&#x13b;", "&#315;", "&#315;", "\c{L}"],
    ["ļ", "&#x13c;", "&#316;", "&#316;", "\c{l}"],
    ["Ľ", "&#x13d;", "&#317;", "&#317;", "\\v{L}"],
    ["ľ", "&#x13e;", "&#318;", "&#318;", "\\v{l}"],
    ["L·", "&#x13f;", "&#319;", "&#319;", "\.{L}"],
    ["l·", "&#x140;", "&#320;", "&#320;", "\.{l}"],
    ["Ł", "&#x141;", "&#321;", "&#321;", "\L"],
    ["ł", "&#x142;", "&#322;", "&#322;", "\l"],
    ["Ń", "&#x143;", "&#323;", "&#323;", "\\'{N}"],
    ["ń", "&#x144;", "&#324;", "&#324;", "\\'{n}"],
    ["Ņ", "&#x145;", "&#325;", "&#325;", "\c{N}"],
    ["ņ", "&#x146;", "&#326;", "&#326;", "\c{n}"],
    ["Ň", "&#x147;", "&#327;", "&#327;", "\\v{N}"],
    ["ň", "&#x148;", "&#328;", "&#328;", "\\v{n}"],
    ["ʼn", "&#x14;9", "&#329;", "&#329;", "'n"],
    ["Ŋ", "&#x14a;", "&#330;", "&#330;", "\\NG"],
    ["ŋ", "&#x14b;", "&#331;", "&#331;", "\\ng"],
    ["Ō", "&#x14c;", "&#332;", "&#332;", "\={O}"],
    ["ō", "&#x14d;", "&#333;", "&#333;", "\={o}"],
    ["Ŏ", "&#x14e;", "&#334;", "&#334;", "\\u{O}"],
    ["ŏ", "&#x14f;", "&#335;", "&#335;", "\\u{o}"],
    ["Ő", "&#x150;", "&#336;", "&#336;", "\H{O}"],
    ["ő", "&#x151;", "&#337;", "&#337;", "\H{o}"],
    ["Œ", "&#x152;", "&#338;", "&OElig;", "\OE"],
    ["œ", "&#x153;", "&#339;", "&oelig;", "\oe"],
    ["Ŕ", "&#x154;", "&#340;", "&#340;", "\\'{R}"],
    ["ŕ", "&#x155;", "&#341;", "&#341;", "\\'{r}"],
    ["Ŗ", "&#x156;", "&#342;", "&#342;", "\c{R}"],
    ["ŗ", "&#x157;", "&#343;", "&#343;", "\c{r}"],
    ["Ř", "&#x158;", "&#344;", "&#344;", "\\v{R}"],
    ["ř", "&#x159;", "&#345;", "&#345;", "\\v{r}"],
    ["Ś", "&#x15a;", "&#346;", "&#346;", "\\'{S}"],
    ["ś", "&#x15b;", "&#347;", "&#347;", "\\'{s}"],
    ["Ŝ", "&#x15c;", "&#348;", "&#348;", "\^{S}"],
    ["ŝ", "&#x15d;", "&#349;", "&#349;", "\^{s}"],
    ["Ş", "&#x15e;", "&#350;", "&#350;", "\c{S}"],
    ["ş", "&#x15f;", "&#351;", "&#351;", "\c{s}"],
    ["Š", "&#x160;", "&#352;", "&Scaron;", "\\v{S}"],
    ["š", "&#x161;", "&#353;", "&scaron;", "\\v{s}"],
    ["Ţ", "&#x162;", "&#354;", "&#354;", "\c{T}"],
    ["ţ", "&#x163;", "&#355;", "&#355;", "\c{t}"],
    ["Ť", "&#x164;", "&#356;", "&#356;", "\\v{T}"],
    ["ť", "&#x165;", "&#357;", "&#357;", "\\v{t}"],
    ["Ŧ", "&#x166;", "&#358;", "&#358;", "\B{T}"],
    ["ŧ", "&#x167;", "&#359;", "&#359;", "\B{t}"],
    ["Ũ", "&#x168;", "&#360;", "&#360;", "\~{U}"],
    ["ũ", "&#x169;", "&#361;", "&#361;", "\~{u}"],
    ["Ū", "&#x16a;", "&#362;", "&#362;", "\={U}"],
    ["ū", "&#x16b;", "&#363;", "&#363;", "\={u}"],
    ["Ŭ", "&#x16c;", "&#364;", "&#364;", "\\u{U}"],
    ["ŭ", "&#x16d;", "&#365;", "&#365;", "\\u{u}"],
    ["Ů", "&#x16e;", "&#366;", "&#366;", "\\r{U}"],
    ["ů", "&#x16f;", "&#367;", "&#367;", "\\r{u}"],
    ["Ű", "&#x170;", "&#368;", "&#368;", "\H{U}"],
    ["ű", "&#x171;", "&#369;", "&#369;", "\H{u}"],
    ["Ų", "&#x172;", "&#370;", "&#370;", "\k{U}"],
    ["ų", "&#x173;", "&#371;", "&#371;", "\k{u}"],
    ["Ŵ", "&#x174;", "&#372;", "&#372;", "\^{W}"],
    ["ŵ", "&#x175;", "&#373;", "&#373;", "\^{w}"],
    ["Ŷ", "&#x176;", "&#374;", "&#374;", "\^{Y}"],
    ["ŷ", "&#x177;", "&#375;", "&#375;", "\^{y}"],
    ["Ÿ", "&#x178;", "&#376;", "&Yuml;", "\\\"{Y}"],
    ["Ź", "&#x179;", "&#377;", "&#377;", "\\'{Z}"],
    ["ź", "&#x17a;", "&#378;", "&#378;", "\\'{z}"],
    ["Ż", "&#x17b;", "&#379;", "&#379;", "\.{Z}"],
    ["ż", "&#x17c;", "&#380;", "&#380;", "\.{z}"],
    ["Ž", "&#x17d;", "&#381;", "&#381;", "\\v{Z}"],
    ["ž", "&#x17e;", "&#382;", "&#382;", "\\v{z}"],

    ["ƒ", "&#x192;", "&#402;", "&fnof;", "\m{f}"],

    ["ˆ", "&#x2c6;", "&#710;", "&circ;", "\^{}"],
    ["˜", "&#x2dc;", "&#732;", "&tilde;", "\~{}"],

    ["Α", "&#x391;", "&#913;", "&Alpha;", "\Alpha"],
    ["Β", "&#x392;", "&#914;", "&Beta;", "\Beta"],
    ["Γ", "&#x393;", "&#915;", "&Gamma;", "\Gamma"],
    ["Δ", "&#x394;", "&#916;", "&Delta;", "\Delta"],
    ["Ε", "&#x395;", "&#917;", "&Epsilon;", "\Epsilon"],
    ["Ζ", "&#x396;", "&#918;", "&Zeta;", "\Zeta"],
    ["Η", "&#x397;", "&#919;", "&Eta;", "\Eta"],
    ["Θ", "&#x398;", "&#920;", "&Theta;", "\Theta"],
    ["Ι", "&#x399;", "&#921;", "&Iota;", "\Iota"],
    ["Κ", "&#x39a;", "&#922;", "&Kappa;", "\Kappa"],
    ["Λ", "&#x39b;", "&#923;", "&Lambda;", "\Lambda"],
    ["Μ", "&#x39c;", "&#924;", "&Mu;", "\Mu"],
    ["Ν", "&#x39d;", "&#925;", "&Nu;", "\\Nu"],
    ["Ξ", "&#x39e;", "&#926;", "&Xi;", "\Xi"],
    ["Ο", "&#x39f;", "&#927;", "&Omicron;", "\Omicron"],
    ["Π", "&#x3a0;", "&#928;", "&Pi;", "\Pi"],
    ["Ρ", "&#x3a1;", "&#929;", "&Rho;", "\Rho"],
    ["Σ", "&#x3a3;", "&#931;", "&Sigma;", "\Sigma"],
    ["Τ", "&#x3a4;", "&#932;", "&Tau;", "\Tau"],
    ["Υ", "&#x3a5;", "&#933;", "&Upsilon;", "\\Upsilon"],
    ["Φ", "&#x3a6;", "&#934;", "&Phi;", "\Phi"],
    ["Χ", "&#x3a7;", "&#935;", "&Chi;", "\Chi"],
    ["Ψ", "&#x3a8;", "&#936;", "&Psi;", "\Psi"],
    ["Ω", "&#x3a9;", "&#937;", "&Omega;", "\Omega"],
    ["α", "&#x3b1;", "&#945;", "&alpha;", "\\alpha"],
    ["β", "&#x3b2;", "&#946;", "&beta;", "\\beta"],
    ["γ", "&#x3b3;", "&#947;", "&gamma;", "\gamma"],
    ["δ", "&#x3b4;", "&#948;", "&delta;", "\delta"],
    ["ε", "&#x3b5;", "&#949;", "&epsilon;", "\epsilon"],
    ["ζ", "&#x3b6;", "&#950;", "&zeta;", "\zeta"],
    ["η", "&#x3b7;", "&#951;", "&eta;", "\eta"],
    ["θ", "&#x3b8;", "&#952;", "&theta;", "\\theta"],
    ["ι", "&#x3b9;", "&#953;", "&iota;", "\iota"],
    ["κ", "&#x3ba;", "&#954;", "&kappa;", "\kappa"],
    ["λ", "&#x3bb;", "&#955;", "&lambda;", "\lambda"],
    ["μ", "&#x3bc;", "&#956;", "&mu;", "\mu"],
    ["ν", "&#x3bd;", "&#957;", "&nu;", "\\nu"],
    ["ξ", "&#x3be;", "&#958;", "&xi;", "\\xi"],
    ["ο", "&#x3bf;", "&#959;", "&omicron;", "\omicron"],
    ["π", "&#x3c0;", "&#960;", "&pi;", "\pi"],
    ["ρ", "&#x3c1;", "&#961;", "&rho;", "\\rho"],
    ["ς", "&#x3c2;", "&#962;", "&sigmaf;", "\\varsigma"],
    ["σ", "&#x3c3;", "&#963;", "&sigma;", "\sigma"],
    ["τ", "&#x3c4;", "&#964;", "&tau;", "\\tau"],
    ["υ", "&#x3c5;", "&#965;", "&upsilon;", "\\upsilon"],
    ["φ", "&#x3c6;", "&#966;", "&phi;", "\phi"],
    ["χ", "&#x3c7;", "&#967;", "&chi;", "\chi"],
    ["ψ", "&#x3c8;", "&#968;", "&psi;", "\psi"],
    ["ω", "&#x3c9;", "&#969;", "&omega;", "\omega"],
    ["ϑ", "&#x3d1;", "&#977;", "&thetasym;", "\\vartheta"],
    ["ϒ", "&#x3d2;", "&#978;", "&upsih;", "\\Upsilon"],
    ["ϖ", "&#x3d6;", "&#982;", "&piv;", "\\varpi"],

    ["–", "&#x2013;", "&#8211;", "&ndash;", "\\textendash"],
    ["—", "&#x2014;", "&#8212;", "&mdash;", "\\textemdash"],
    ["‘", "&#x2018;", "&#8216;", "&lsquo;", "`"],
    ["’", "&#x2019;", "&#8217;", "&rsquo;", "'"],
    ["‚", "&#x201a;", "&#8218;", "&sbquo;", "", ""],
    ["“", "&#x201c;", "&#8220;", "&ldquo;", "``"],
    ["”", "&#x201d;", "&#8221;", "&rdquo;", "''"],
    ["„", "&#x201e;", "&#8222;", "&bdquo;", "", "", ""],
    ["†", "&#x2020;", "&#8224;", "&dagger;", "\dagger"],
    ["‡", "&#x2021;", "&#8225;", "&Dagger;", "\ddagger"],
    ["•", "&#x2022;", "&#8226;", "&bull;", "\\bullet"],
    ["…", "&#x2026;", "&#8230;", "&hellip;", "\ldots"],
    ["‰", "&#x2030;", "&#8240;", "&permil;", "\permil"],
    ["′", "&#x2032;", "&#8242;", "&prime;", "'"],
    ["″", "&#x2033;", "&#8243;", "&Prime;", "''"],
    ["‹", "&#x2039;", "&#8249;", "&lsaquo;", "\guilsinglleft"],
    ["›", "&#x203a;", "&#8250;", "&rsaquo;", "\guilsinglright"],
    ["‾", "&#x203e;", "&#8254;", "&oline;", "\overline{\mbox{<text>}}"],

    ["€", "&#x20ac;", "&#8364;", "&euro;", "\\texteuro"],

    ["№", "&#x2116;", "&#8470;", "&#8470;", "\\textnumero"],
    ["™", "&#x2122;", "&#8482;", "&trade;", "\\texttrademark"],

    ["←", "&#x2190;", "&#8592;", "&larr;", "\leftarrow"],
    ["↑", "&#x2191;", "&#8593;", "&uarr;", "\\uparrow"],
    ["→", "&#x2192;", "&#8594;", "&rarr;", "\\rightarrow"],
    ["↓", "&#x2193;", "&#8595;", "&darr;", "\downarrow"],
    ["↔", "&#x2194;", "&#8596;", "&harr;", "\leftrightarrow"],

    ["↵", "&#x21b5;", "&#8629;", "&crarr;", "\\textdlsh"],

    ["∀", "&#x2200;", "&#8704;", "&forall;", "\\forall"],
    ["∂", "&#x2202;", "&#8706;", "&part;", "\partial"],
    ["∃", "&#x2203;", "&#8707;", "&exists;", "\exists"],
    ["∅", "&#x2205;", "&#8709;", "&empty;", "\emptyset"],
    ["∇", "&#x2207;", "&#8711;", "&nabla;", "\\nabla"],
    ["∈", "&#x2208;", "&#8712;", "&isin;", "\in"],
    ["∉", "&#x2209;", "&#8713;", "&notin;", "\\notin"],
    ["∋", "&#x220b;", "&#8715;", "&ni;", "\\ni"],
    ["∏", "&#x220f;", "&#8719;", "&prod;", "\prod"],
    ["∑", "&#x2211;", "&#8721;", "&sum;", "\sum"],
    ["−", "&#x2212;", "&#8722;", "&minus;", "-"],
    ["∗", "&#x2217;", "&#8727;", "&lowast;", "\\ast"],
    ["√", "&#x221a;", "&#8730;", "&radic;", "\sqrt{}"],
    ["∝", "&#x221d;", "&#8733;", "&prop;", "\propto"],
    ["∞", "&#x221e;", "&#8734;", "&infin;", "\infty"],
    ["∠", "&#x2220;", "&#8736;", "&ang;", "\\angle"],
    ["∧", "&#x2227;", "&#8743;", "&and;", "\wedge"],
    ["∨", "&#x2228;", "&#8744;", "&or;", "\\vee"],
    ["∩", "&#x2229;", "&#8745;", "&cap;", "\cap"],
    ["∪", "&#x222a;", "&#8746;", "&cup;", "\cup"],
    ["∫", "&#x222b;", "&#8747;", "&int;", "\int"],
    ["∴", "&#x2234;", "&#8756;", "&there4;", "\\therefore"],
    ["∼", "&#x223c;", "&#8764;", "&sim;", "\sim"],
    ["≅", "&#x2245;", "&#8773;", "&cong;", "\cong"],
    ["≈", "&#x2248;", "&#8776;", "&asymp;", "\\approx"],

    ["≠", "&#x2260;", "&#8800;", "&ne;", "\\neq"],
    ["≡", "&#x2261;", "&#8801;", "&equiv;", "\equiv"],
    ["≤", "&#x2264;", "&#8804;", "&le;", "\le"],
    ["≥", "&#x2265;", "&#8805;", "&ge;", "\ge"],
    ["⊂", "&#x2282;", "&#8834;", "&sub;", "\subset"],
    ["⊃", "&#x2283;", "&#8835;", "&sup;", "\supset"],
    ["⊄", "&#x2284;", "&#8836;", "&nsub;", "\\not\subset"],
    ["⊆", "&#x2286;", "&#8838;", "&sube;", "\subseteq"],
    ["⊇", "&#x2287;", "&#8839;", "&supe;", "\supseteq"],
    ["⊕", "&#x2295;", "&#8853;", "&oplus;", "\oplus"],
    ["⊗", "&#x2297;", "&#8855;", "&otimes;", "\otimes"],
    ["⊥", "&#x22a5;", "&#8869;", "&perp;", "\perp"],

    ["⋅", "&#x22c5;", "&#8901;", "&sdot;", "\cdot"],
    ["⌈", "&#x2308;", "&#8968;", "&lceil;", "\lceil"],
    ["⌉", "&#x2309;", "&#8969;", "&rceil;", "\\rceil"],
    ["⌊", "&#x230a;", "&#8970;", "&lfloor;", "\lfloor"],
    ["⌋", "&#x230b;", "&#8971;", "&rfloor;", "\\rfloor"],

    ["◊", "&#x25ca;", "&#9674;", "&loz;", "\lozenge"], #\Diamond ?

    ["♠", "&#x2660;", "&#9824;", "&spades;", "\spadesuit"],
    ["♣", "&#x2663;", "&#9827;", "&clubs;", "\clubsuit"],
    ["♥", "&#x2665;", "&#9829;", "&hearts;", "\\varheartsuit"],
    ["♦", "&#x2666;", "&#9830;", "&diams;", "\\vardiamondsuit"]
]


class ScrollConvertPluginAppActivatable(GObject.Object, Gedit.AppActivatable, PeasGtk.Configurable):
    app = GObject.property(type=Gedit.App)
        
    def do_activate(self):
        #self.app.add_accelerator(actions[1], "win."+actions[0], None)
        self.app.set_accels_for_action("win."+actions[0], [actions[1]]) 
        #print( self.app.get_accels_for_action( "win."+actions[0]))
        pass

    def do_deactivate(self):
        self.app.set_accels_for_action("win."+actions[0], [])
#        self.app.remove_accelerator("win." + actions[0], None) # %
        #pass
    
    def do_create_configure_widget(self):
        grid = Gtk.Grid()
        button1 = Gtk.CheckButton(label="Ascii")
        button2 = Gtk.CheckButton(label="Hexadecimal")
        button3 = Gtk.CheckButton(label="Decimal")
        button4 = Gtk.CheckButton(label="Html Name")
        button5 = Gtk.CheckButton(label="Latex")
        button1.set_border_width(3)
        button2.set_border_width(3)
        button3.set_border_width(3)
        button4.set_border_width(3)
        button5.set_border_width(3)

        button1.set_active(lset[0][1])
        button2.set_active(lset[1][1])
        button3.set_active(lset[2][1])
        button4.set_active(lset[3][1])
        button5.set_active(lset[4][1])

        button1.connect("toggled", self.on_button_toggled, "ascii") 
        button2.connect("toggled", self.on_button_toggled, "hexa")
        button3.connect("toggled", self.on_button_toggled, "dec")
        button4.connect("toggled", self.on_button_toggled, "html")
        button5.connect("toggled", self.on_button_toggled, "latex")

        accel0 = Gtk.ComboBoxText()
        mod0 = ["","<Alt>","<Ctrl>","<Shift>"]
        for x in mod0:
            accel0.append_text(x)
        accel1 = Gtk.ComboBoxText()
        mod1 = ["<Alt>","<Ctrl>","<Shift>"]
        for x in mod1:
            accel1.append_text(x)
        accel2 = Gtk.ComboBoxText()
        mod2 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", 
            "w", "x", "y", "z"]
        for x in mod2:
            accel2.append_text(x)

        if actions[1].count('<')>1:
            i = actions[1].index("<", 2)
            accel0.set_active(mod0.index(actions[1][:i]))
            accel1.set_active(mod1.index(actions[1][i:-1]))
            accel2.set_active(mod2.index(actions[1][-1:]))
        else:
            accel0.set_active(0)
            accel1.set_active(mod1.index(actions[1][:-1]))
            accel2.set_active(mod2.index(actions[1][-1:]))

        accel0.connect("changed", self.on_shortcut_changed, 0)
        accel1.connect("changed", self.on_shortcut_changed, 1)
        accel2.connect("changed", self.on_shortcut_changed, 2)

        grid.attach(Gtk.Label("   Please choose at least one language.   "), 0, 0, 3, 1)
        grid.attach(button1, 0, 1, 3, 1)
        grid.attach(button2, 0, 2, 3, 1)
        grid.attach(button3, 0, 3, 3, 1)
        grid.attach(button4, 0, 4, 3, 1)
        grid.attach(button5, 0, 5, 3, 1)
        grid.attach(Gtk.Label("Choose shortcut key:"), 0, 6, 3, 1)
        grid.attach(accel0, 0, 7, 1, 1)
        grid.attach(accel1, 1, 7, 1, 1)
        grid.attach(accel2, 2, 7, 1, 1)
        return (grid)

    def on_button_toggled(self, button, name):
        # it toggles the check then does:  %
        for x in lset:
            if name == x[0]: 
                lset[lset.index(x)][1] = button.get_active()

    def on_shortcut_changed(self, button, num):
        #self.do_update_state()
        if num == 2:
            actions[1] = actions[1][:-1] + button.get_active_text()
        elif num == 1:
            if actions[1].count('<')>1:
                i = actions[1].index("<", 2)
                actions[1] = actions[1][:i] + button.get_active_text() + actions[1][-1:]
            else:
                actions[1] = button.get_active_text() + actions[1][-1:]
        elif num == 0:
            if actions[1].count('<')>1:
                i = actions[1].index("<", 2)
                actions[1] = button.get_active_text() + actions[1][i:]
            else:
                actions[1] = button.get_active_text() + actions[1]
        print(actions[1])
        #pass
        #self.app.set_accels_for_action("win."+actions[0], []) 
        #self.app.set_accels_for_action("win."+actions[0], actions[1])

class ScrollConvertPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = 'ScrollConvert'
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        action = Gio.SimpleAction(name=actions[0])
        action.connect('activate', getattr(self, actions[0]))#  %
        self.window.add_action(action)

    def do_deactivate(self):
        self.window.remove_action(actions[0])

    def sconvert(self, action, thingy):

        ## get word
        doc = self.window.get_active_document()
        #startloc = doc.get_insert();
        bounds = doc.get_selection_bounds()
        if not bounds: return
        term = doc.get_text(bounds[0], bounds[1], False)

        ## determine original language
        if len(term) == 1:   # ascii
            orig=0
        elif term[:3]=="&#x":# hexadecimal 
            orig=1
        elif term[:2]=="&#": # dec number
            orig=2
        elif term[:1]=="&":  # html name
            orig=3
        elif term[:1]=="\\": # latex
            orig=4
        else:
            return

        ## scroll through next available language
        ## double list so all values hit even if starting in the middle
        dlangs = [lset[y][1] for y in range(len(lset))] * 2
        val = ""
        for x in d:
            if x[orig]==term:
                for y in range(orig+1,len(dlangs)):
                    if dlangs[y]:
                        val = d[d.index(x)][y%len(lset)]
                        ## account for missing/ duplicate/ default values
                        if len(val) == 0:
                            if (y%len(lset)) == 4: 
                                val = d[d.index(x)][0] ## latex to ascii
                            if (y%len(lset)) == 3: 
                                val = d[d.index(x)][2] ## html name to decimal
                        if len(val)==0 or val == term:
                            continue ## skip if duplicate or blank
                        break
                break

        #for a in range (0,len(d)):
        #    text=text.replace(d[a][0], d[a][1])
        if len(val)==0 or val == term: return
        doc.begin_user_action()
        doc.delete(*bounds)
        doc.insert_at_cursor(val)
        #endloc = doc.get_iter_at_mark (doc.get_insert());
        #doc.select_range(doc.get_iter_at_mark (startloc), endloc)# %
        doc.end_user_action()

    def do_update_state(self):
        pass # print("updating")



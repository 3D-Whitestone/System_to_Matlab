	x0 = m2.*s2.^2;
	x1 = cos(q20);
	x2 = sin(q10);
	x3 = cos(q30);
	x4 = s3.*x3;
	x5 = sin(q20);
	x6 = l2.*x5;
	x7 = -x2.*x4 - x2.*x6;
	x8 = cos(q10);
	x9 = x4.*x8;
	x10 = x6.*x8;
	x11 = x10 + x9;
	x12 = x11.*x8;
	x13 = x12 - x2.*x7;
	x14 = x5.^2;
	x15 = x7.*x8;
	x16 = x15.*x3;
	x17 = x11.*x2;
	x18 = x17.*x3;
	x19 = x16 + x18;
	x20 = sin(q30);
	x21 = -x15.*x20 - x17.*x20;
	x22 = x3.^2;
	x23 = x20.^2;
	x24 = AS2.*x1.^2 + AS3.*x23 + BM1.*iG1.^2 + BS1 + BS2.*x14 + BS3.*x22 + m3.*x13.^2 + m3.*x19.^2 + m3.*x21.^2 + x0.*x14;
	x25 = 1./x24;
	x26 = x2.^2;
	x27 = l2.*x1;
	x28 = x26.*x27;
	x29 = x28.*x3;
	x30 = x20.*x6;
	x31 = x8.^2;
	x32 = x27.*x3;
	x33 = x31.*x32;
	x34 = x29 - x30 + x33;
	x35 = m3.*x34;
	x36 = x27.*x31;
	x37 = x3.*x6;
	x38 = -x20.*x28 - x20.*x36 - x37;
	x39 = m3.*x38;
	x40 = x19.*x35 + x21.*x39;
	x41 = x40.^2;
	x42 = CM2.*iG2.^2 + CS2 + m3.*x34.^2 + m3.*x38.^2 + x0 - x25.*x41;
	x43 = 1./x42;
	x44 = s3.*x22;
	x45 = s3.*x23;
	x46 = x26.*x45 + x31.*x45 + x44;
	x47 = m3.*x46;
	x48 = s3.*x20;
	x49 = x31.*x48;
	x50 = x3.*x49;
	x51 = x3.*x48;
	x52 = x26.*x48;
	x53 = x3.*x52;
	x54 = -x50 + x51 - x53;
	x55 = m3.*x19;
	x56 = x21.*x47 + x54.*x55;
	x57 = x25.*x56;
	x58 = x35.*x54 + x38.*x47 - x40.*x57;
	x59 = x58.^2;
	x60 = x43.*x59;
	x61 = x56.^2;
	x62 = CM3.*iG3.^2 + CS3 + m3.*x46.^2 + m3.*x54.^2 - x25.*x61 - x60;
	x63 = 1./x62;
	x64 = -x10 - x9;
	x65 = x64.*x8;
	x66 = x12.*x3 + x3.*x65;
	x67 = -x12.*x20 - x20.*x65;
	x68 = x35.*x66 + x39.*x67;
	x69 = x25.*x68;
	x70 = 2*x40;
	x71 = x24.^(-2);
	x72 = m3.*x21;
	x73 = 2*x72;
	x74 = 2*x55;
	x75 = 2*m3.*x13;
	x76 = x71.*(x66.*x74 + x67.*x73 + x75.*(-x17 - x2.*x64));
	x77 = x41.*x76 - x69.*x70;
	x78 = x42.^(-2);
	x79 = x59.*x78;
	x80 = x77.*x79;
	x81 = x43.*x58;
	x82 = x56.*x76;
	x83 = m3.*x54;
	x84 = x47.*x67 + x66.*x83;
	x85 = x25.*x40;
	x86 = x40.*x82 - x57.*x68 - x84.*x85;
	x87 = 2*x86;
	x88 = 2*x57;
	x89 = x61.*x76 + x80 - x81.*x87 - x84.*x88;
	x90 = x62.^(-2);
	x91 = x60.*x90;
	x92 = x58.*x63;
	x93 = x43.*x92;
	x94 = -x63.*x80 + x87.*x93 - x89.*x91;
	x95 = x40.*x43;
	x96 = x60.*x63 + 1;
	x97 = x43.*x68;
	x98 = x63.*x84;
	x99 = x56.*x63;
	x100 = x43.*x99;
	x101 = x58.*x78;
	x102 = x101.*x99;
	x103 = x78.*x96;
	x104 = x40.*x77;
	x105 = x56.*x90;
	x106 = x105.*x89;
	x107 = g.*m3;
	x108 = x107.*x23;
	x109 = x107.*x22;
	x110 = g.*m2.*s2;
	x111 = -M20.*iG2 - x108.*x6 - x109.*x6 - x110.*x5;
	x112 = x111.*x25;
	x113 = x81.*x99 - x95.*x96;
	x114 = x111.*x113;
	x115 = x63.*x86;
	x116 = x58.*x90;
	x117 = x116.*x95;
	x118 = x78.*x92;
	x119 = s3.*x107;
	x120 = -M30.*iG3 + x107.*x3.*x45 + x119.*x3.^3;
	x121 = x120.*x25;
	x122 = -x57 + x81.*x85;
	x123 = x122.*x63;
	x124 = -x123.*x58 - x85;
	x125 = x58.*x95;
	x126 = x43.*x85;
	x127 = x101.*x85;
	x128 = -x125.*x76 + x126.*x86 - x127.*x77 - x25.*x84 + x69.*x81 + x82;
	x129 = x122.*x90;
	x130 = x129.*x58;
	x131 = -x123.*x86 - x128.*x92 + x130.*x89 + x40.*x76 - x69;
	x132 = x124.*x78;
	x133 = M10.*iG1;
	x134 = x133.*x25;
	x135 = x133.*(-x122.*x99 - x124.*x95 + 1);
	x136 = x92.*x95 - x99;
	x137 = x120.*x136;
	x138 = 2*x1.*x5;
	x139 = x71.*(-AS2.*x138 + BS2.*x138 + x0.*x138 + x75.*(x28 + x36));
	x140 = -x20.*x27 - x26.*x37 - x31.*x37;
	x141 = x26.*x30 + x30.*x31 - x32;
	x142 = x140.*x55 + x141.*x72;
	x143 = x124.*x43;
	x144 = x142.*x25;
	x145 = 2*x39;
	x146 = 2*x35;
	x147 = x139.*x41 + x140.*x146 + x141.*x145 - x144.*x70;
	x148 = x139.*x40;
	x149 = x140.*x83 + x141.*x47 - x144.*x56 + x148.*x56;
	x150 = x149.*x43;
	x151 = -x127.*x147 + x139.*x56 + x144.*x81 - x148.*x81 + x150.*x85;
	x152 = x147.*x79;
	x153 = 2*x81;
	x154 = x139.*x61 - x149.*x153 + x152;
	x155 = x105.*x154;
	x156 = -x123.*x149 + x130.*x154 - x144 + x148 - x151.*x92;
	x157 = x147.*x40;
	x158 = x149.*x63;
	x159 = x43.*x96;
	x160 = 2*x93;
	x161 = x149.*x160 - x152.*x63 - x154.*x91;
	x162 = -x1.*x110 - x108.*x27 - x109.*x27;
	x163 = 2*x20.*x3;
	x164 = -x16 - x18;
	x165 = x71.*(AS3.*x163 - BS3.*x163 + x164.*x73 + x21.*x74 + x75.*(-x49 - x52));
	x166 = -x26.*x44 - x31.*x44 - x45 + x46;
	x167 = 2*x50 - 2*x51 + 2*x53;
	x168 = x164.*x47 + x166.*x55 + x167.*x72 + x54.*x72;
	x169 = -x29 + x30 - x33;
	x170 = x164.*x39 + x169.*x72 + x19.*x39 + x21.*x35;
	x171 = x145.*x169 + x146.*x38 + x165.*x41 - 2*x170.*x85;
	x172 = x171.*x79;
	x173 = x165.*x40;
	x174 = x166.*x35 + x167.*x39 - x168.*x85 + x169.*x47 - x170.*x57 + x173.*x56 + x39.*x54;
	x175 = -x153.*x174 + x165.*x61 + 2*x166.*x83 + 2*x167.*x47 - x168.*x88 + x172;
	x176 = x105.*x175;
	x177 = x168.*x63;
	x178 = x170.*x25;
	x179 = x101.*x171;
	x180 = -x125.*x165 + x126.*x174 + x165.*x56 - x168.*x25 + x178.*x81 - x179.*x85;
	x181 = -x123.*x174 + x130.*x175 + x173 - x178 - x180.*x92;
	x182 = x132.*x171;
	x183 = x103.*x171;
	x184 = x160.*x174 - x172.*x63 - x175.*x91;
	x185 = -x107.*x20.*x44 - x119.*x20.^3;
	x186 = x174.*x63;
	x187 = x132.*x133;
	x188 = x103.*x111;
	x189 = x120.*x43;
	x190 = x120.*x90;
	x191 = x190.*x89;
	x192 = x111.*x43;
	x193 = x118.*x120;
	x194 = x133.*x43;
	x195 = x154.*x190;
	x196 = x175.*x190;
	x197 = x185.*x63;
	x198 = x133.*x63;
	x199 = x116.*x192;
	x200 = x111.*x118;
	x201 = x129.*x133;

	A = [0 0 0 1 0 0; 0 0 0 0 1 0; 0 0 0 0 0 1; -x112.*(x100.*x86 - x102.*x77 + x103.*x104 - x106.*x81 + x81.*x98 - x94.*x95 - x96.*x97) + x114.*x76 - x121.*(-x104.*x118 + x106 + x115.*x95 - x117.*x89 + x92.*x97 - x98) + x134.*(x104.*x132 + x106.*x122 - x122.*x98 - x124.*x97 - x128.*x99 - x131.*x95) - x135.*x76 + x137.*x76 -x112.*(-x102.*x147 + x103.*x157 - x142.*x159 + x150.*x99 - x155.*x81 - x161.*x95) - x113.*x162.*x25 + x114.*x139 - x121.*(-x117.*x154 - x118.*x157 + x142.*x93 + x155 + x158.*x95) + x134.*(x122.*x155 + x132.*x157 - x142.*x143 - x151.*x99 - x156.*x95) - x135.*x139 + x137.*x139 -x112.*(x100.*x174 - x159.*x170 - x176.*x81 + x177.*x81 - x179.*x99 + x183.*x40 - x184.*x95) + x114.*x165 - x121.*(-x117.*x175 - x118.*x171.*x40 + x170.*x93 + x176 - x177 + x186.*x95) + x134.*(x122.*x176 - x122.*x177 - x143.*x170 - x180.*x99 - x181.*x95 + x182.*x40) - x135.*x165 - x136.*x185.*x25 + x137.*x165 0 0 0; x115.*x189 + x131.*x194 - x187.*x77 + x188.*x77 - x191.*x81 - x192.*x94 - x193.*x77 -x147.*x187 + x147.*x188 - x147.*x193 + x156.*x194 + x158.*x189 - x159.*x162 - x161.*x192 - x195.*x81 x111.*x183 - x133.*x182 - x171.*x193 + x181.*x194 - x184.*x192 + x186.*x189 - x196.*x81 + x197.*x81 0 0 0; x115.*x192 + x128.*x198 + x191 - x199.*x89 - x200.*x77 - x201.*x89 -x147.*x200 + x151.*x198 - x154.*x199 - x154.*x201 + x158.*x192 + x162.*x93 + x195 -x171.*x200 - x175.*x199 - x175.*x201 + x180.*x198 + x186.*x192 + x196 - x197 0 0 0];

	clear x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35 x36 x37 x38 x39 x40 x41 x42 x43 x44 x45 x46 x47 x48 x49 x50 x51 x52 x53 x54 x55 x56 x57 x58 x59 x60 x61 x62 x63 x64 x65 x66 x67 x68 x69 x70 x71 x72 x73 x74 x75 x76 x77 x78 x79 x80 x81 x82 x83 x84 x85 x86 x87 x88 x89 x90 x91 x92 x93 x94 x95 x96 x97 x98 x99 x100 x101 x102 x103 x104 x105 x106 x107 x108 x109 x110 x111 x112 x113 x114 x115 x116 x117 x118 x119 x120 x121 x122 x123 x124 x125 x126 x127 x128 x129 x130 x131 x132 x133 x134 x135 x136 x137 x138 x139 x140 x141 x142 x143 x144 x145 x146 x147 x148 x149 x150 x151 x152 x153 x154 x155 x156 x157 x158 x159 x160 x161 x162 x163 x164 x165 x166 x167 x168 x169 x170 x171 x172 x173 x174 x175 x176 x177 x178 x179 x180 x181 x182 x183 x184 x185 x186 x187 x188 x189 x190 x191 x192 x193 x194 x195 x196 x197 x198 x199 x200 x201;
	x0 = sin(q10);
	x1 = sin(q20);
	x2 = l2.*x1;
	x3 = cos(q30);
	x4 = s3.*x3;
	x5 = -x0.*x2 - x0.*x4;
	x6 = cos(q10);
	x7 = x3.*x6;
	x8 = s3.*x7 + x2.*x6;
	x9 = cos(q20);
	x10 = x1.^2;
	x11 = m2.*s2.^2;
	x12 = x0.*x8;
	x13 = x12.*x3 + x5.*x7;
	x14 = x3.^2;
	x15 = sin(q30);
	x16 = -x12.*x15 - x15.*x5.*x6;
	x17 = x15.^2;
	x18 = 1./(AS2.*x9.^2 + AS3.*x17 + BM1.*iG1.^2 + BS1 + BS2.*x10 + BS3.*x14 + m3.*x13.^2 + m3.*x16.^2 + m3.*(-x0.*x5 + x6.*x8).^2 + x10.*x11);
	x19 = x0.^2;
	x20 = l2.*x9;
	x21 = x19.*x20;
	x22 = x6.^2;
	x23 = x20.*x22;
	x24 = -x15.*x21 - x15.*x23 - x2.*x3;
	x25 = m3.*x24;
	x26 = -x15.*x2 + x21.*x3 + x23.*x3;
	x27 = m3.*x13;
	x28 = x16.*x25 + x26.*x27;
	x29 = 1./(CM2.*iG2.^2 + CS2 + m3.*x24.^2 + m3.*x26.^2 + x11 - x18.*x28.^2);
	x30 = x18.*x28;
	x31 = s3.*x17;
	x32 = s3.*x14 + x19.*x31 + x22.*x31;
	x33 = x15.*x4;
	x34 = -x19.*x33 - x22.*x33 + x33;
	x35 = m3.*x16.*x32 + x27.*x34;
	x36 = m3.*x26.*x34 + x25.*x32 - x30.*x35;
	x37 = x29.*x36.^2;
	x38 = 1./(CM3.*iG3.^2 + CS3 + m3.*x32.^2 + m3.*x34.^2 - x18.*x35.^2 - x37);
	x39 = x29.*x36;
	x40 = -x18.*x35 + x30.*x39;
	x41 = x38.*x40;
	x42 = x29.*(-x30 - x36.*x41);
	x43 = x35.*x38;
	x44 = x29.*(x37.*x38 + 1);
	x45 = x38.*x39;
	x46 = iG3.*x38;

	B = [0 0 0; 0 0 0; 0 0 0; iG1.*x18.*(-x28.*x42 - x40.*x43 + 1) iG2.*x18.*(-x28.*x44 + x39.*x43) iG3.*x18.*(x28.*x45 - x43); iG1.*x42 iG2.*x44 -x39.*x46; iG1.*x41 -iG2.*x45 x46];

	clear x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35 x36 x37 x38 x39 x40 x41 x42 x43 x44 x45 x46;

	C = [1 0 0 0 0 0; 0 1 0 0 0 0; 0 0 1 0 0 0; 0 0 0 1 0 0; 0 0 0 0 1 0; 0 0 0 0 0 1];

	

	D = [0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0];

	
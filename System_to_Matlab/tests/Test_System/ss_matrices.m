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
	x28 = x27.*x3;
	x29 = x26.*x28;
	x30 = x20.*x6;
	x31 = x8.^2;
	x32 = x28.*x31;
	x33 = x29 - x30 + x32;
	x34 = m3.*x33;
	x35 = x20.*x27;
	x36 = x27.*x31;
	x37 = x3.*x6;
	x38 = -x20.*x36 - x26.*x35 - x37;
	x39 = m3.*x21;
	x40 = x19.*x34 + x38.*x39;
	x41 = x40.^2;
	x42 = CM2.*iG2.^2 + CS2 + m3.*x33.^2 + m3.*x38.^2 + x0 - x25.*x41;
	x43 = 1./x42;
	x44 = s3.*x22;
	x45 = s3.*x23;
	x46 = x26.*x45 + x31.*x45 + x44;
	x47 = m3.*x46;
	x48 = s3.*x20;
	x49 = x31.*x48;
	x50 = x3.*x48;
	x51 = x26.*x48;
	x52 = -x3.*x49 - x3.*x51 + x50;
	x53 = m3.*x52;
	x54 = x19.*x53 + x39.*x46;
	x55 = x25.*x54;
	x56 = x34.*x52 + x38.*x47 - x40.*x55;
	x57 = x56.^2;
	x58 = x43.*x57;
	x59 = x54.^2;
	x60 = CM3.*iG3.^2 + CS3 + m3.*x46.^2 + m3.*x52.^2 - x25.*x59 - x58;
	x61 = 1./x60;
	x62 = -x10 - x9;
	x63 = x62.*x8;
	x64 = x12.*x3 + x3.*x63;
	x65 = m3.*(-x12.*x20 - x20.*x63);
	x66 = x34.*x64 + x38.*x65;
	x67 = x25.*x66;
	x68 = 2*x40;
	x69 = m3.*x19;
	x70 = 2*m3.*x13;
	x71 = x24.^(-2);
	x72 = x71.*(2*x21.*x65 + 2*x64.*x69 + x70.*(-x17 - x2.*x62));
	x73 = x41.*x72 - x67.*x68;
	x74 = x42.^(-2);
	x75 = x57.*x74;
	x76 = x73.*x75;
	x77 = x60.^(-2);
	x78 = 2*x56;
	x79 = x54.*x72;
	x80 = x46.*x65 + x53.*x64;
	x81 = x25.*x80;
	x82 = x40.*x79 - x40.*x81 - x55.*x66;
	x83 = x43.*x82;
	x84 = 2*x55;
	x85 = x59.*x72 + x76 - x78.*x83 - x80.*x84;
	x86 = x77.*x85;
	x87 = x56.*x61;
	x88 = x43.*x87;
	x89 = 2*x88;
	x90 = -x58.*x86 - x61.*x76 + x82.*x89;
	x91 = x40.*x43;
	x92 = x58.*x61 + 1;
	x93 = x43.*x92;
	x94 = x61.*x80;
	x95 = x43.*x56;
	x96 = x54.*x61;
	x97 = x73.*x74;
	x98 = x56.*x96;
	x99 = x40.*x92;
	x100 = x54.*x77;
	x101 = x100.*x85;
	x102 = g.*m3;
	x103 = x102.*x6;
	x104 = g.*m2.*s2;
	x105 = -M20.*iG2 - x103.*x22 - x103.*x23 - x104.*x5;
	x106 = x105.*x25;
	x107 = -x40.*x93 + x95.*x96;
	x108 = x105.*x107;
	x109 = x61.*x91;
	x110 = x56.*x91;
	x111 = x40.*x87;
	x112 = s3.*x102;
	x113 = -M30.*iG3 + x102.*x3.*x45 + x112.*x3.^3;
	x114 = x113.*x25;
	x115 = x25.*x40;
	x116 = x115.*x95 - x55;
	x117 = x116.*x61;
	x118 = -x115 - x117.*x56;
	x119 = x118.*x43;
	x120 = x115.*x56;
	x121 = -x110.*x72 + x115.*x83 - x120.*x97 + x67.*x95 + x79 - x81;
	x122 = x116.*x56;
	x123 = -x117.*x82 - x121.*x87 + x122.*x86 + x40.*x72 - x67;
	x124 = x118.*x40;
	x125 = iG1.*x25;
	x126 = M10.*x125;
	x127 = -x116.*x96 - x119.*x40 + 1;
	x128 = M10.*iG1;
	x129 = x127.*x128;
	x130 = x87.*x91 - x96;
	x131 = x113.*x130;
	x132 = 2*x1.*x5;
	x133 = x71.*(-AS2.*x132 + BS2.*x132 + x0.*x132 + x70.*(x26.*x27 + x36));
	x134 = -x26.*x37 - x31.*x37 - x35;
	x135 = x26.*x30 - x28 + x30.*x31;
	x136 = x134.*x69 + x135.*x39;
	x137 = m3.*x38;
	x138 = 2*x137;
	x139 = 2*x34;
	x140 = -2*x115.*x136 + x133.*x41 + x134.*x139 + x135.*x138;
	x141 = x140.*x74;
	x142 = x133.*x54;
	x143 = x134.*x53 + x135.*x47 - x136.*x55 + x142.*x40;
	x144 = x143.*x43;
	x145 = x136.*x25;
	x146 = -x110.*x133 + x115.*x144 - x120.*x141 + x142 + x145.*x95;
	x147 = x140.*x75;
	x148 = x133.*x59 - x144.*x78 + x147;
	x149 = x100.*x148;
	x150 = x148.*x77;
	x151 = -x117.*x143 + x122.*x150 + x133.*x40 - x145 - x146.*x87;
	x152 = x143.*x89 - x147.*x61 - x150.*x58;
	x153 = x102.*x27;
	x154 = -x1.*x104 - x153.*x22 - x153.*x23;
	x155 = x107.*x25;
	x156 = 2*x3;
	x157 = x156.*x20;
	x158 = -x16 - x18;
	x159 = 2*x39;
	x160 = x71.*(AS3.*x157 - BS3.*x157 + x158.*x159 + x159.*x19 + x70.*(-x49 - x51));
	x161 = -x26.*x44 - x31.*x44 - x45 + x46;
	x162 = x156.*x49 + x156.*x51 - 2*x50;
	x163 = x158.*x47 + x161.*x69 + x162.*x39 + x21.*x53;
	x164 = -x29 + x30 - x32;
	x165 = x137.*x158 + x164.*x39 + x21.*x34 + x38.*x69;
	x166 = x165.*x25;
	x167 = x138.*x164 + x139.*x38 + x160.*x41 - x166.*x68;
	x168 = x167.*x75;
	x169 = x163.*x25;
	x170 = x160.*x40;
	x171 = x137.*x162 + x161.*x34 + x164.*x47 - x165.*x55 - x169.*x40 + x170.*x54 + x38.*x53;
	x172 = x171.*x43;
	x173 = x160.*x59 + 2*x161.*x53 + 2*x162.*x47 - x163.*x84 + x168 - x172.*x78;
	x174 = x100.*x173;
	x175 = x163.*x61;
	x176 = x167.*x74;
	x177 = x115.*x172 - x120.*x176 + x160.*x54 + x166.*x95 - x169 - x170.*x95;
	x178 = x173.*x77;
	x179 = -x117.*x171 + x122.*x178 - x166 + x170 - x177.*x87;
	x180 = -x168.*x61 + 2*x172.*x87 - x178.*x58;
	x181 = -x102.*x20.*x44 - x112.*x20.^3;
	x182 = x130.*x25;
	x183 = x171.*x61;
	x184 = x118.*x128;
	x185 = x105.*x92;
	x186 = x113.*x61;
	x187 = x113.*x77;
	x188 = x187.*x85;
	x189 = x105.*x43;
	x190 = x113.*x87;
	x191 = x128.*x43;
	x192 = x148.*x187;
	x193 = x173.*x187;
	x194 = x181.*x61;
	x195 = x128.*x61;
	x196 = x189.*x56;
	x197 = x105.*x87;
	x198 = x189.*x61;
	x199 = x116.*x128;
	x200 = iG3.*x61;

	A = [0 0 0 1 0 0; 0 0 0 0 1 0; 0 0 0 0 0 1; -x106.*(-x101.*x95 - x66.*x93 + x83.*x96 - x90.*x91 + x94.*x95 - x97.*x98 + x97.*x99) + x108.*x72 - x114.*(x101 + x109.*x82 - x110.*x86 - x111.*x97 + x66.*x88 - x94) + x126.*(x101.*x116 - x116.*x94 - x119.*x66 - x121.*x96 - x123.*x91 + x124.*x97) - x129.*x72 + x131.*x72 -x106.*(-x136.*x93 - x141.*x98 + x141.*x99 + x144.*x96 - x149.*x95 - x152.*x91) + x108.*x133 - x114.*(x109.*x143 - x110.*x150 - x111.*x141 + x136.*x88 + x149) + x126.*(x116.*x149 - x119.*x136 + x124.*x141 - x146.*x96 - x151.*x91) - x129.*x133 + x131.*x133 - x154.*x155 -x106.*(-x165.*x93 + x172.*x96 - x174.*x95 + x175.*x95 - x176.*x98 + x176.*x99 - x180.*x91) + x108.*x160 - x114.*(-x110.*x178 - x111.*x176 + x165.*x88 + x174 - x175 + x183.*x91) + x126.*(x116.*x174 - x116.*x175 - x119.*x165 + x124.*x176 - x177.*x96 - x179.*x91) - x129.*x160 + x131.*x160 - x181.*x182 0 0 0; x123.*x191 - x184.*x97 + x185.*x97 + x186.*x83 - x188.*x95 - x189.*x90 - x190.*x97 -x141.*x184 + x141.*x185 - x141.*x190 + x144.*x186 + x151.*x191 - x152.*x189 - x154.*x93 - x192.*x95 x172.*x186 - x176.*x184 + x176.*x185 - x176.*x190 + x179.*x191 - x180.*x189 - x193.*x95 + x194.*x95 0 0 0; x121.*x195 + x188 - x196.*x86 - x197.*x97 + x198.*x82 - x199.*x86 -x141.*x197 + x143.*x198 + x146.*x195 - x150.*x196 - x150.*x199 + x154.*x88 + x192 -x176.*x197 + x177.*x195 - x178.*x196 - x178.*x199 + x183.*x189 + x193 - x194 0 0 0];
	clear x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35 x36 x37 x38 x39 x40 x41 x42 x43 x44 x45 x46 x47 x48 x49 x50 x51 x52 x53 x54 x55 x56 x57 x58 x59 x60 x61 x62 x63 x64 x65 x66 x67 x68 x69 x70 x71 x72 x73 x74 x75 x76 x77 x78 x79 x80 x81 x82 x83 x84 x85 x86 x87 x88 x89 x90 x91 x92 x93 x94 x95 x96 x97 x98 x99 x100 x101 x102 x103 x104 x105 x106 x107 x108 x109 x110 x111 x112 x113 x114 x115 x116 x117 x118 x119 x120 x121 x122 x123 x124 x125 x126 x127 x128 x129 x130 x131 x132 x133 x134 x135 x136 x137 x138 x139 x140 x141 x142 x143 x144 x145 x146 x147 x148 x149 x150 x151 x152 x153 x154 x155 x156 x157 x158 x159 x160 x161 x162 x163 x164 x165 x166 x167 x168 x169 x170 x171 x172 x173 x174 x175 x176 x177 x178 x179 x180 x181 x182 x183 x184 x185 x186 x187 x188 x189 x190 x191 x192 x193 x194 x195 x196 x197 x198 x199 x200;
	B = [0 0 0; 0 0 0; 0 0 0; x125.*x127 iG2.*x155 iG3.*x182; iG1.*x119 iG2.*x93 -x200.*x95; iG1.*x117 -iG2.*x88 x200];
	clear x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35 x36 x37 x38 x39 x40 x41 x42 x43 x44 x45 x46 x47 x48 x49 x50 x51 x52 x53 x54 x55 x56 x57 x58 x59 x60 x61 x62 x63 x64 x65 x66 x67 x68 x69 x70 x71 x72 x73 x74 x75 x76 x77 x78 x79 x80 x81 x82 x83 x84 x85 x86 x87 x88 x89 x90 x91 x92 x93 x94 x95 x96 x97 x98 x99 x100 x101 x102 x103 x104 x105 x106 x107 x108 x109 x110 x111 x112 x113 x114 x115 x116 x117 x118 x119 x120 x121 x122 x123 x124 x125 x126 x127 x128 x129 x130 x131 x132 x133 x134 x135 x136 x137 x138 x139 x140 x141 x142 x143 x144 x145 x146 x147 x148 x149 x150 x151 x152 x153 x154 x155 x156 x157 x158 x159 x160 x161 x162 x163 x164 x165 x166 x167 x168 x169 x170 x171 x172 x173 x174 x175 x176 x177 x178 x179 x180 x181 x182 x183 x184 x185 x186 x187 x188 x189 x190 x191 x192 x193 x194 x195 x196 x197 x198 x199 x200;
	C = [1 0 0 0 0 0; 0 1 0 0 0 0; 0 0 1 0 0 0; 0 0 0 1 0 0; 0 0 0 0 1 0; 0 0 0 0 0 1];
	clear x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35 x36 x37 x38 x39 x40 x41 x42 x43 x44 x45 x46 x47 x48 x49 x50 x51 x52 x53 x54 x55 x56 x57 x58 x59 x60 x61 x62 x63 x64 x65 x66 x67 x68 x69 x70 x71 x72 x73 x74 x75 x76 x77 x78 x79 x80 x81 x82 x83 x84 x85 x86 x87 x88 x89 x90 x91 x92 x93 x94 x95 x96 x97 x98 x99 x100 x101 x102 x103 x104 x105 x106 x107 x108 x109 x110 x111 x112 x113 x114 x115 x116 x117 x118 x119 x120 x121 x122 x123 x124 x125 x126 x127 x128 x129 x130 x131 x132 x133 x134 x135 x136 x137 x138 x139 x140 x141 x142 x143 x144 x145 x146 x147 x148 x149 x150 x151 x152 x153 x154 x155 x156 x157 x158 x159 x160 x161 x162 x163 x164 x165 x166 x167 x168 x169 x170 x171 x172 x173 x174 x175 x176 x177 x178 x179 x180 x181 x182 x183 x184 x185 x186 x187 x188 x189 x190 x191 x192 x193 x194 x195 x196 x197 x198 x199 x200;
	D = [0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0];
	clear x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35 x36 x37 x38 x39 x40 x41 x42 x43 x44 x45 x46 x47 x48 x49 x50 x51 x52 x53 x54 x55 x56 x57 x58 x59 x60 x61 x62 x63 x64 x65 x66 x67 x68 x69 x70 x71 x72 x73 x74 x75 x76 x77 x78 x79 x80 x81 x82 x83 x84 x85 x86 x87 x88 x89 x90 x91 x92 x93 x94 x95 x96 x97 x98 x99 x100 x101 x102 x103 x104 x105 x106 x107 x108 x109 x110 x111 x112 x113 x114 x115 x116 x117 x118 x119 x120 x121 x122 x123 x124 x125 x126 x127 x128 x129 x130 x131 x132 x133 x134 x135 x136 x137 x138 x139 x140 x141 x142 x143 x144 x145 x146 x147 x148 x149 x150 x151 x152 x153 x154 x155 x156 x157 x158 x159 x160 x161 x162 x163 x164 x165 x166 x167 x168 x169 x170 x171 x172 x173 x174 x175 x176 x177 x178 x179 x180 x181 x182 x183 x184 x185 x186 x187 x188 x189 x190 x191 x192 x193 x194 x195 x196 x197 x198 x199 x200;
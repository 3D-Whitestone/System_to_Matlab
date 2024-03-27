function [output, out2] = test_MFunction(input) 
	x0 = input.^2;
	x1 = input + x0;
	x2 = x1.^2;
	x3 = x0 + x2;

	in1 = input;
	x = x1;
	out1 = x3;
	z = x2;
	out2 = [x3; x2];
	output = x3;
end
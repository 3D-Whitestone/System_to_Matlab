function [output, out2] = test_MFunction(input, input2, input3) 
	in1 = input;
	in2 = input2(1);
	in3 = input2(2);
	in1 = input3(1,1);
	in2 = input3(1,2);
	in3 = input3(2,1);
	in1 = input3(2,2);
	x0 = in2.^2 + in3;
	x1 = x0.^2;
	x2 = in1.^2 + x1;

	x = x0;
	out1 = x2;
	z = x1;
	out2 = [x2; x1];
	output = x2;
end
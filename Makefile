prbs7: prbs7.v prbs7_tb.v
	iverilog -o ./build/tb.vvp prbs7_tb.v
	vvp -n ./build/tb.vvp
	gtkwave ./build/wave.vcd

build:
	mkdir build
clean:
	rmdir /s/q build
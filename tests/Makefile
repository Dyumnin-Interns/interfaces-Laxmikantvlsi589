SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/../hdl/dut.v
VERILOG_SOURCES += $(PWD)/../hdl/FIFO1.v
VERILOG_SOURCES += $(PWD)/../hdl/FIFO2.v

TOPLEVEL = dut
MODULE = dut_test

# Enable waveform dump and specify filename
export COCOTB_SIM=1
export DUMPFILE=fifo.vcd

# Set WAVES=1 to trigger dump logic in cocotb for Icarus
WAVES ?= 1

include $(shell cocotb-config --makefiles)/Makefile.sim

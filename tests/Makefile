SIM ?= icarus
TOPLEVEL_LANG ?= verilog

# Source files
VERILOG_SOURCES += $(PWD)/../hdl/dut.v
VERILOG_SOURCES += $(PWD)/../hdl/FIFO1.v
VERILOG_SOURCES += $(PWD)/../hdl/FIFO2.v

# Top-level DUT module
TOPLEVEL = dut

# Python test module (filename without .py)
MODULE = dut_test

# Generate VCD waveform
WAVES ?= 1
DUMPFILE ?= fifo.vcd

# Propagate environment vars to cocotb
export COCOTB_SIM=1
export WAVES
export DUMPFILE

# Cocotb build system
include $(shell cocotb-config --makefiles)/Makefile.sim

SIM ?= verilator
TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

VERILOG_SOURCES := $(PWD)/../src/arbiter.sv

TOPLEVEL := arbiter
MODULE  := test_arbiter

EXTRA_ARGS += --sv -CFLAGS "-std=c++17"
BUILD_ARGS += CXXFLAGS+=" -std=c++17"

EXTRA_ARGS += --trace --trace-fst
SIM_ARGS += -wave $(TOPLEVEL).fsd


# Make that waveform for me plz
TRACE_FILE ?= dump.fst

SIM_ARGS += --trace --trace-file $(TRACE_FILE) --log-cli-level=INFO

COCOTB_LOG_FILE ?= sim.log
COCOTB_LOG_LEVEL ?= INFO

include $(shell cocotb-config --makefiles)/Makefile.sim
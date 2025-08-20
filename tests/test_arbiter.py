from queue import Queue
import queue
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from collections import deque
import logging
import random

@cocotb.test()
async def arbiter_basic_test(dut):
    log = logger = logging.getLogger(__name__)

    inserted = [queue.Queue() for _ in range(4)]

    # Start clock
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    dut.rst.value = 1;

    await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0;
    await ClockCycles(dut.clk, 10)

    dut.req.value = 0b1011
    await ClockCycles(dut.clk, 20)

    await RisingEdge(dut.clk)



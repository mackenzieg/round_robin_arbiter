from queue import Queue
import queue
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from collections import deque
import logging
import random

class ArbiterScoreboard:
    def __init__(self, dut):
        self.dut = dut
        self.expected_grants = [queue.Queue() for _ in range(4)]

        for i in range(random.randomint(15)):
            self.expected_grants[random.randomint(0, 3)].append(1)

        cocotb.start_soon(self.req_inserter(dut))
        
    async def req_inserter(self, dut):
        while (True):
            have_entries = False
            for i in range(4):
                if (not self.expected_grants[i].empty()):
                    have_entries = True

            if (have_entries):
                value = 0
                for i in range(4):
                    if (not self.expected_grants[i].empty()):
                        value |= (1 << i)

            await RisingEdge(dut.clk)

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



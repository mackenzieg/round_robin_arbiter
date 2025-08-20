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
        self.log = logging.getLogger(__name__)

        for i in range(random.randint(6, 10)):
            self.expected_grants[random.randint(0, 3)].put(1)

        cocotb.start_soon(self.req_inserter(dut))
        cocotb.start_soon(self.grant_polling(dut))
        
    async def req_inserter(self, dut):
        while (True):
            have_entries = False
            for i in range(4):
                if (not self.expected_grants[i].empty()):
                    have_entries = True

            value = 0
            if (have_entries):
                for i in range(4):
                    if (not self.expected_grants[i].empty()):
                        value |= (1 << i)

            self.dut.req.value = value

            await RisingEdge(dut.clk)

    async def grant_polling(self, dut):
        while (True):
            value = self.dut.grant.value

            for i in range(4):
                if ((value >> i) & 1):
                    self.expected_grants[i].get()

            await RisingEdge(dut.clk)


@cocotb.test()
async def arbiter_basic_test(dut):
    log = logger = logging.getLogger(__name__)

    inserted = [queue.Queue() for _ in range(4)]

    arbiter_scoreboard = ArbiterScoreboard(dut)

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



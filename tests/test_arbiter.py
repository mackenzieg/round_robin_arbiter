from queue import Queue
import queue
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from collections import deque
import logging
import random

class ArbiterScoreboard:
    def __init__(self, dut, log):
        self.dut = dut
        self.log = log
        self.expected_grants = [queue.Queue() for _ in range(4)]
        self.log = logging.getLogger(__name__)

        for i in range(10):
            self.expected_grants[random.randint(0, 1) * 3].put(1)

        for i in range(4):
            self.log.info(f"Inserted {self.expected_grants[i].qsize()} in index: {i}")

        cocotb.start_soon(self.req_inserter(dut))
        cocotb.start_soon(self.grant_polling(dut))

    
    def is_complete(self):
        return all(ee.empty() for ee in self.expected_grants)
        
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
                    if (not self.expected_grants[i].empty()):
                        self.expected_grants[i].get()

            await RisingEdge(dut.clk)


@cocotb.test()
async def arbiter_basic_test(dut):
    log = logger = logging.getLogger(__name__)

    # Start clock
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)

    dut.rst.value = 0
    await ClockCycles(dut.clk, 10)

    arbiter_scoreboard = ArbiterScoreboard(dut, log)
    await RisingEdge(dut.clk)

    await ClockCycles(dut.clk, 100)






#import cocotb
#from cocotb.triggers import Timer


#@cocotb.test()
#async def dut_test(dut):
 #   assert 0, "Test not Implemented"



import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb_coverage.coverage import CoverPoint, CoverCross, coverage_db
import os
import random


class InputDriver:
    def __init__(self, dut, name, addr, clk):
        self.dut = dut
        self.addr = addr
        self.clk = clk
        self.name = name

    async def send(self, data):
        self.dut.write_en.value = 1
        self.dut.write_address.value = self.addr
        self.dut.write_data.value = data
        await RisingEdge(self.clk)
        self.dut.write_en.value = 0
        await Timer(1, units='ns')


class OutputMonitor:
    def __init__(self, dut, clk, read_addr, status_addr, callback):
        self.dut = dut
        self.clk = clk
        self.read_addr = read_addr
        self.status_addr = status_addr
        self.callback = callback

    async def run(self):
        while True:
            # Check if output FIFO is not empty
            self.dut.read_en.value = 1
            self.dut.read_address.value = self.status_addr
            await RisingEdge(self.clk)
            self.dut.read_en.value = 0
            await Timer(1, units='ns')

            if self.dut.read_data.value == 1:  # Not empty
                self.dut.read_en.value = 1
                self.dut.read_address.value = self.read_addr
                await RisingEdge(self.clk)
                await Timer(1, units='ns')
                val = self.dut.read_data.value.integer
                self.callback(val)
                self.dut.read_en.value = 0

            await Timer(2, units='ns')


class Scoreboard:
    def __init__(self):
        self.expected = []

    def push(self, val):
        self.expected.append(val)

    def check(self, actual):
        expected = self.expected.pop(0)
        assert expected == actual, f"Scoreboard mismatch: expected {expected}, got {actual}"


@CoverPoint("input.a", xf=lambda a, b: a, bins=[0, 1])
@CoverPoint("input.b", xf=lambda a, b: b, bins=[0, 1])
@CoverCross("input.cross.ab", items=["input.a", "input.b"])
def ab_cover(a, b):
    pass


@cocotb.test()
async def dut_test(dut):
    clk = dut.CLK
    clock = Clock(clk, 10, units="ns") 
    cocotb.start_soon(clock.start())    
    sb = Scoreboard()
    adrv = InputDriver(dut, "a", addr=4, clk=clk)
    bdrv = InputDriver(dut, "b", addr=5, clk=clk)
    mon = OutputMonitor(dut, clk, read_addr=3, status_addr=2, callback=sb.check)

    # Reset
    dut.RST_N.value = 1
    await Timer(2, units="ns")
    dut.RST_N.value = 0
    await RisingEdge(clk)
    dut.RST_N.value = 1
    await RisingEdge(clk)

    cocotb.start_soon(mon.run())

    for _ in range(20):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        sb.push(a | b)
        ab_cover(a, b)

        await adrv.send(a)
        await bdrv.send(b)

        await Timer(5, units='ns')

    while sb.expected:
        await Timer(10, units='ns')

    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_db.export_to_xml(filename=os.path.join(os.getenv("RESULT_PATH", "."), "coverage.xml"))

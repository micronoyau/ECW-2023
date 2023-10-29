import curses
import sys

def decode(instr):
    if instr & 0x80 == 0x80:
        reg = (instr & 0x07) + 1
        imm = (instr >> 3) & 0x0f
        return 'seti r{}, 0x{:02x}'.format(reg, imm)

    if instr in [0x00, 0x14, 0x15, 0x16, 0x17]:
        return 'nop'

    if instr == 0x01:
        return 'syscall'

    if instr == 0x02:
        return 'call'

    if instr == 0x03:
        return 'ret'

    if instr == 0x04:
        return 'xcg'

    if instr == 0x11:
        return 'jmp'

    if instr == 0x12:
        return 'jz'

    if instr == 0x13:
        return 'jnz'

    if instr & 0xf8 == 0x18:
        shift = instr & 0x07
        return 'shr r1, {}'.format(shift)

    if instr & 0xf8 == 0x20:
        shift = instr & 0x07
        return 'shl r1, {}'.format(shift)

    if instr & 0xf8 == 0x28:
        reg = (instr & 0x07) + 1
        return 'not r{}'.format(reg)

    if instr & 0xf8 == 0x30:
        reg = (instr & 0x07) + 1
        return 'or r1, r{}'.format(reg)

    if instr & 0xf8 == 0x38:
        reg = (instr & 0x07) + 1
        return 'and r1, r{}'.format(reg)

    if instr & 0xf8 == 0x40:
        reg = (instr & 0x07) + 1
        return 'xor r1, r{}'.format(reg)

    if instr & 0xf8 == 0x48:
        reg = (instr & 0x07) + 1
        return 'sub r1, r{}'.format(reg)

    if instr & 0xf8 == 0x50:
        reg = (instr & 0x07) + 1
        return 'add r1, r{}'.format(reg)

    if instr & 0xf8 == 0x58:
        reg = (instr & 0x07) + 1
        return 'cmp r1, r{}'.format(reg)

    if instr & 0xf8 == 0x60:
        reg = (instr & 0x07) + 1
        return 'ld r{}'.format(reg)

    if instr & 0xf8 == 0x68:
        reg = (instr & 0x07) + 1
        return 'st r{}'.format(reg)

    if instr & 0xf8 == 0x70:
        reg = (instr & 0x07) + 1
        return 'mov r{}, r1'.format(reg)

    if instr & 0xf8 == 0x78:
        reg = (instr & 0x07) + 1
        return 'mov r1, r{}'.format(reg)

    else:
        return "? : {:#010b}".format(instr)


def disas(filename):
    with open(filename, "rb") as f:
        ip = 0

        while True:
            instr = f.read(1)
            if not instr:
                break

            print("0x{:02x} : {}".format(ip, decode(instr[0])))
            ip += 1


class Debug:

    def __init__(self, filename, breakpoints=None):
        self.regs = [0,0,0,0,0,0,0,0]
        self.ip = 0
        self.callstack = []
        self.flags = {'Z':0, 'GT':0, 'LT':0}
        self.mem = [0x00] * 0xffff

        self.breakpoints = []
        if breakpoints:
            self.breakpoints = list(map(lambda x: int(x, base=16), breakpoints.split(',')))

        self.stdin = open("dbg_input.txt", "rb")

        # Load program in memory
        with open(filename, "rb") as f:
            cnt = 0
            while True:
                instr = f.read(1)
                if not instr:
                    break
                self.mem[cnt] = instr[0]
                cnt += 1

    def addr_pointer(self):
        return (self.regs[6]<<8) | self.regs[7]

    def brk(self):
        self.breakpoints.append(self.ip)

    def cont(self):
        ret = self.step()
        while (self.ip not in self.breakpoints) and (ret != -1):
            ret = self.step()

    def step(self):
        instr = self.mem[self.ip]

        if instr & 0x80 == 0x80:
            reg = (instr & 0x07)
            imm = (instr >> 3) & 0x0f
            self.regs[reg] = imm

        elif instr in [0x00, 0x14, 0x15, 0x16, 0x17]:
            pass

        # SYSCALL
        elif instr == 0x01:
            self.ip += 1
            ret_str = "mem[r7:r8] = {}".format(self.mem[self.addr_pointer()])

            # Read
            if self.regs[0] == 0x01:
                self.regs[0] = self.stdin.read(1)[0]
                return "READ : {}, r1 = {}".format(ret_str, chr(self.regs[0]))

            elif self.regs[0] == 0x02:
                return "WRITE : {} = {}".format(ret_str, chr(self.mem[self.addr_pointer()]))

            else:
                return "UNKOWN SYSCALL : {}".format(ret_str)

        elif instr == 0x02:
            self.callstack.append(self.ip)
            self.ip = (self.regs[-2]<<8) | self.regs[-1]

        elif instr == 0x03:
            self.ip = self.callstack.pop()

        elif instr == 0x04:
            self.regs[4], self.regs[5], self.regs[6], self.regs[7] = self.regs[6], self.regs[7], self.regs[4], self.regs[5]

        elif instr == 0x11:
            self.ip = (self.regs[-2]<<8) | self.regs[-1]

        elif instr == 0x12:
            if self.flags['Z'] == 1:
                self.ip = (self.regs[-2]<<8) | self.regs[-1]

        elif instr == 0x13:
            if self.flags['Z'] == 0:
                self.ip = (self.regs[-2]<<8) | self.regs[-1]

        elif instr & 0xf8 == 0x18:
            shift = instr & 0x07
            self.regs[0] >>= shift

        elif instr & 0xf8 == 0x20:
            shift = instr & 0x07
            self.regs[0] <<= shift

        elif instr & 0xf8 == 0x28:
            reg = (instr & 0x07)
            self.regs[reg] = (~self.regs[reg]) & 0xff

        elif instr & 0xf8 == 0x30:
            reg = (instr & 0x07)
            self.regs[0] |= self.regs[reg]

        elif instr & 0xf8 == 0x38:
            reg = (instr & 0x07)
            self.regs[0] &= self.regs[reg]

        elif instr & 0xf8 == 0x40:
            reg = (instr & 0x07)
            self.regs[0] ^= self.regs[reg]

        elif instr & 0xf8 == 0x48:
            reg = (instr & 0x07)
            self.regs[0] = (self.regs[0] - self.regs[reg]) & 0xff

        elif instr & 0xf8 == 0x50:
            reg = (instr & 0x07)
            self.regs[0] = (self.regs[0] + self.regs[reg]) & 0xff

        elif instr & 0xf8 == 0x58:
            reg = (instr & 0x07)
            res = (self.regs[0] - self.regs[reg]) & 0xff
            self.flags['Z'] = 1 if res == 0 else 0
            self.flags['GT'] = 1 if ((res & 0x80 == 0) and (res != 0)) else 0
            self.flags['LT'] = 1 if res & 0x80 == 0x80 else 0

        elif instr & 0xf8 == 0x60:
            reg = (instr & 0x07)
            self.regs[reg] = self.mem[(self.regs[6]<<8) | self.regs[7]]

        elif instr & 0xf8 == 0x68:
            reg = (instr & 0x07)
            self.mem[(self.regs[6]<<8) | self.regs[7]] = self.regs[reg]

        elif instr & 0xf8 == 0x70:
            reg = (instr & 0x07)
            self.regs[reg] = self.regs[0]

        elif instr & 0xf8 == 0x78:
            reg = (instr & 0x07)
            self.regs[0] = self.regs[reg]

        else:
            #print("? : {:#010b}".format(instr))
            return -1

        self.ip += 1


    def interactive(self):
        stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        stdscr.clear()
        stdscr.refresh()

        k = ''

        while (k != ord('q')):
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            if k == ord('b'):
                self.brk()
                stdscr.addstr(height-5, 10, "Breakpoint added")

            if k == ord('c'):
                self.cont()

            out_instr = None
            if k == ord('n'):
                out_instr = self.step()

            if out_instr != None:
                if type(out_instr) == str:
                    stdscr.addstr(height-5, 10, out_instr)

                elif out_instr == -1:
                    out_str = "Unkown instruction = 0x{:02x}".format(self.mem[self.ip])
                    stdscr.addstr(height-5, 10, out_str)

            flags_str = "FLAGS : ZF={} GT={} LT={}".format(self.flags['Z'], self.flags['GT'], self.flags['LT'])
            stdscr.addstr(10, 10, flags_str)

            addr_ptr = "ADDR PTR : {:04x}".format((self.regs[-2]<<8) | self.regs[-1])
            stdscr.addstr(10, 10+(width-20)//2-len(addr_ptr)//2, addr_ptr)

            ip_str = "IP : {:04x}".format(self.ip)
            stdscr.addstr(10, width-10-len(ip_str), ip_str)

            callstack_str = "CALLSTACK : {}".format(list(map(lambda elem: "0x{:04x}".format(elem), self.callstack)))
            stdscr.addstr(15, 10, callstack_str)

            PREV_INSTR = 5
            NEXT_INSTR = 5

            for i in range(PREV_INSTR):
                curr_instr_str = ""
                if self.ip - (PREV_INSTR-i) >= 0:
                    curr_instr_str = decode(self.mem[self.ip-(PREV_INSTR-i)])
                stdscr.addstr(20 + i, 10, curr_instr_str)

                if self.ip - (PREV_INSTR-i) in self.breakpoints:
                    stdscr.addstr(20 + i, 8, "*")

            curr_instr_str = "=> {}".format(decode(self.mem[self.ip]))
            stdscr.addstr(20 + PREV_INSTR, 10-3, curr_instr_str)

            for i in range(NEXT_INSTR):
                curr_instr_str = ""
                if self.ip + i <= 0xffff:
                    curr_instr_str = decode(self.mem[self.ip+i+1])
                stdscr.addstr(20 + PREV_INSTR + i + 1, 10, curr_instr_str)

                if self.ip + i in self.breakpoints:
                    stdscr.addstr(20 + PREV_INSTR + i, 8, "*")

            for i in range(8):
                reg_str = "r{} | {:02x}".format(i+1, self.regs[i])
                stdscr.addstr(20 + i * 2, width-10-len(reg_str), reg_str)

            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            k = stdscr.getch()

        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

if len(sys.argv) >= 3:
    if sys.argv[1] == 'debug':
        if len(sys.argv) == 4:
            debug = Debug(sys.argv[2], breakpoints=sys.argv[3])
        else:
            debug = Debug(sys.argv[2])
        debug.interactive()

    elif sys.argv[1] == 'disas':
        disas(sys.argv[2])

else:
    print("Usage :")
    print("{} disas FILE".format(sys.argv[0]))
    print("{} debug FILE [breakpoints, separated by commas]".format(sys.argv[0]))


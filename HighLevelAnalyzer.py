# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting


# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    # List of settings that a user can set for this High Level Analyzer.
    DisplayFormat = ChoicesSetting(
        label='Display Format',
        choices=('Auto', 'Dec', 'Hex')
    )

    ChooseServoTypes = ChoicesSetting(
        label='Protocol 1 Servo Type',
        choices=('AX Servos (default)', 'MX Servos', 'XL 320 Servos', 'X Servos')
    )
    ChooseServoTypes = ChoicesSetting(
        label='Protocol 2 Servo Type',
        choices=('X Servos (default)', 'MX Servos', 'XL 320 Servos')
    )

    ChooseRegisterPairs = ChoicesSetting(
        label='Show Register Pairs as a word',
        choices=('yes', 'no')
    )

    ChooseServoController = ChoicesSetting(
        label='Servo Type',
        choices=('AX Servos (default)', 'MX Servos', 'XL Servos')
    )

    #--------------------------------------------------------------------------
    # Define tables 
    #--------------------------------------------------------------------------
    s_cmd_names = {
        0:"Reply", 1:"Ping", 2:"Read", 3:"Write", 4:"REG_WRITE", 
        5:"Action", 6:"Reset", 8:"Reboot", 0x10:"Clear",
        0x55:"Reply", 0x82:"SRead", 0x83:"SWrite", 0x8a:"FSRead", 
        0x92:"BulkRead", 0x93:"BulkWrite", 0x9A:"FBulkRead" }

    # AX Servos
    s_ax_register_names = {
        0:{"MODEL",2},
        2:{"VER",0},
        3:{"ID",0},
        4:{"BAUD",0},
        5:{"DELAY",0},
        6:{"CWL",2},
        8:{"CCWL",2},
        11:{"LTEMP",0},
        12:{"LVOLTD",0},
        13:{"LVOLTU",0},
        14:{"MTORQUE",2},
        16:{"RLEVEL",0},
        17:{"ALED",0},
        18:{"ASHUT",0},
        # RAM
        24:{"TENABLE",0},
        25:{"LED",0},
        26:{"CWMAR",0},
        27:{"CCWMAR",0},
        28:{"CWSLOPE",0},
        29:{"CCWSLOPE",0},
        30:{"GOAL",2},
        32:{"GSPEED",2},
        34:{"TLIMIT",2},
        36:{"PPOS",2},
        38:{"PSPEED",2},
        40:{"PLOAD",2},
        42:{"PVOLT",0},
        43:{"PTEMP",0},
        44:{"RINST",0},
        46:{"MOVING",0},
        47:{"LOCK",0},
        48:{"PUNCH",2}
    }

    # MX Servos
    s_mx_register_names = [
        "MODEL", "MODEL_H", "VER","ID","BAUD","DELAY","CWL","CWL_H",
        "CCWL","CCWL_H","?","LTEMP","LVOLTD","LVOLTU","MTORQUE", "MTORQUE_H",
        "RLEVEL","ALED","ASHUT","?","MTOFSET","MTOFSET_L","RESD","?",
        #RAM AREA 
        "TENABLE","LED","DGAIN","IGAIN","PGAIN","?","GOAL","GOAL_H",
        "GSPEED","GSPEED_H","TLIMIT","TLIMIT_H","PPOS","PPOS_H","PSPEED","PSPEED_H",
        "PLOAD","PLOAD_H","PVOLT","PTEMP","RINST","?","MOVING","LOCK",
        #0x30
        "PUNCH","PUNCH_H","?","?","?","?","?","?",
        "?","?","?","?","?","?","?","?",
        #0x40
        "?","?","?","?","CURR", "CURR_H", "TCME", "GTORQ",
        "QTORQ_H","GACCEL"
    ]

    s_is_mx_register_multi_byte = [
        2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0,
        0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
        2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0,
        2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 2, 0, 0, 2, 0, 0
    ]

    # XL Servos
    s_xl_register_names = [
        "MODEL", "MODEL_H", "VER","ID","BAUD","DELAY","CWL","CWL_H",
        "CCWL","CCWL_H","?","CMODE", "LTEMP","LVOLTD","LVOLTU", "MTORQUE", 
        "MTORQUE_H", "RLEVEL", "ASHUT","?","?","?","?","?",
        # RAM AREA
        "TENABLE","LED","DGAIN","IGAIN","PGAIN","?","GOAL","GOAL_H",
        "GSPEED","GSPEED_H","?", "TLIMIT","TLIMIT_H","PPOS","PPOS_H","PSPEED",
        "PSPEED_H", "PLOAD","PLOAD_H","?", "?","PVOLT", "PTEMP","RINST",
        #0x30
        "?","MOVING","HSTAT", "PUNCH","PUNCH_H"
    ]

    s_is_xl_register_multi_byte = [
        2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
        2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0,
        0, 0, 0, 2, 
    ]

    s_x_register_names = {
        0:{"name":"MODE#", "cb":2},
        2:{"name":"MODEL", "cb":4},
        6:{"name":"VER", "cb":0},
        7:{"name":"ID", "cb":0},
        8:{"name":"BAUD", "cb":0},
        9:{"name":"DELAY", "cb":0},
        10:{"name":"DMODE", "cb":0},
        11:{"name":"OMODE", "cb":0},
        12:{"name":"S-ID", "cb":0},
        13:{"name":"PROT", "cb":0},
        20:{"name":"HOFF", "cb":4},
        24:{"name":"MOVT", "cb":4},
        31:{"name":"TLIMIT", "cb":0},
        32:{"name":"VMAX", "cb":2},
        34:{"name":"VMIN", "cb":2},
        36:{"name":"PWML", "cb":2},
        40:{"name":"ACCLL", "cb":4},
        44:{"name":"VLMT", "cb":4},
        48:{"name":"MXPOS", "cb":4},
        52:{"name":"MNPOS", "cb":4},
        60:{"name":"SCONFIG", "cb":0},
        63:{"name":"SHUTDN", "cb":0},

        64:{"name":"TENABLE", "cb":0},
        65:{"name":"LED", "cb":0},
        68:{"name":"RETL", "cb":0},
        69:{"name":"RINST", "cb":0},
        70:{"name":"HERR", "cb":0},
        76:{"name":"VIGAIN", "cb":2},
        78:{"name":"VPGAIN", "cb":2},
        80:{"name":"POSDG", "cb":2},
        82:{"name":"POSIG", "cb":2},
        84:{"name":"POSPG", "cb":2},
        88:{"name":"FF2G", "cb":2},
        90:{"name":"FF1G", "cb":2},
        98:{"name":"BWATCH", "cb":0},
        100:{"name":"GPWM", "cb":2},
        104:{"name":"GVEL", "cb":4},
        108:{"name":"GACCL", "cb":4},
        112:{"name":"PVEL", "cb":4},
        116:{"name":"GOAL", "cb":4},
        120:{"name":"RTICK", "cb":2},
        122:{"name":"MOVING", "cb":0},
        123:{"name":"MSTATUS", "cb":0},
        124:{"name":"PPWM", "cb":2},
        126:{"name":"PLOAD", "cb":2},
        128:{"name":"PVEL", "cb":4},
        132:{"name":"PPOS", "cb":4},
        136:{"name":"VELT", "cb":4},
        140:{"name":"POST", "cb":4},
        144:{"name":"PVOLT", "cb":2},
        146:{"name":"PTEMP" , "cb":0},
        147:{"name":"BACKRDY" , "cb":0}
    }

    #USB2AX - probably not needed as does not forward messages on normal AX BUSS

    #CM730(ish) controllers. 
    s_cm730_register_names = [
        "MODEL", "MODEL_H", "VER","ID","BAUD","DELAY","","",
        "","","","","LVOLTD","LVOLTU","", "",
        "RLEVEL","","","","","","","",
        #RAM AREA
        "POWER", "LPANNEL", "LHEAD", "LHEAD_H", "LEYE", "LEYE_H", "BUTTON", "",
        "D1", "D2", "D3","D4","D5","D6", "GYROZ", "GYROZ_H",
        "GYROY","GYROY_H","GYROX","GYROX_H", "ACCX", "ACCX_H","ACCY", "ACCY_H",
        "ACCZ","ACCZ_H", "ADC0","ADC1","ADC1_H", "ADC2","ADC2_H", "ADC3",
        "ADC3_H","ADC4","ADC4_H","ADC5","ADC5_H","ADC6","ADC6_H", "ADC7",
        "ADC7_H","ADC8","ADC8_H","ADC9","ADC9_H","ADC10","ADC10_H", "ADC11",
        "ADC11_H","ADC12","ADC12_H","ADC13","ADC13_H","ADC14","ADC14_H", "ADC15",
        "ADC15_H"
    ]

    s_is_cm730_register_multi_byte = [
        2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0,
        2, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2,
        0, 2, 0, 2, 0, 2, 0, 2, 0
    ]

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'simple': {
            'format': '{{data.cmd}} ID:{{data.id}}'
        },
        'DXL Write': {
            'format': '{{data.cmd}} ID:{{data.id}} R:{{data.reg}} = {{data.data}}'
        },
        'DXL Read': {
            'format': '{{data.cmd}} ID:{{data.id}} R:{{data.reg}} #:{{data.cnt}}'
        },
        'DXL Reply': {
            'format': '{{data.cmd}} ID:{{data.id}} Err:{{data.err}} R:{{data.reg}} #:{{data.cnt}}'
        },
        'dynamixel': {
            'format': 'ID:{{data.id}} {{data.cmd}} {{data.data}}'
        }
    }

    def __init__(self):

        self.base = 0 # commands choose. 
        if self.DisplayFormat == 'Hex':
            self.base = 16
        elif self.DisplayFormat == 'Dec':
            self.base = 10

        '''
        Initialize HLA.
        Settings can be accessed using the same name used above.
        '''
        self.frame_start_time = None
        self.frame_second_time = None
        self.frame_end_time = None
        self.frame_state = 0
        self.servo_id = None
        self.frame_protocol = 1
        self.frame_length = 0
        self.frame_cmd = None
        self.data_packet_save = None
        self.last_cmd = None;
        self.last_cmd_reg = None
        self.last_cmd_reg_cnt = None

        #need to see which is selected but first start hard codded. 


        print("Settings:", self.ChooseServoTypes,
              self.ChooseRegisterPairs, self.ChooseServoController)

    def generate_result_frame(self, frame, protocol):
        new_frame = None
        frame_data = {}
        frame_data['id'] = str(self.servo_id[0])
        frame_data['protocol'] = str(protocol)
        data_len = len(self.data_packet_save)

        cmd = self.frame_cmd[0]
        if cmd in self.s_cmd_names:
            frame_data['cmd'] = self.s_cmd_names[cmd]
        else:
            frame_data['cmd'] = ''.join([ '0x', hex(cmd).upper()[2:] ])

        # see if we can 
        if cmd in {0, 0x55}:
            #reply
            frame_data['err'] = self.data_packet_save[0]
            data_str = ''
            for i in range(1,len(self.data_packet_save)):
                if self.base == 10:
                    data_str +=' ' + str(self.data_packet_save[i])
                else:
                    data_str +=' ' + hex(self.data_packet_save[i])
            frame_data['data'] = data_str
            new_frame = AnalyzerFrame("DXL Reply", self.frame_start_time, frame.end_time, frame_data)


        elif cmd in {1, 5, 8}:
            #ping #action #reboot
            new_frame = AnalyzerFrame("simple", self.frame_start_time, frame.end_time, frame_data)
        # simple write/reg swrite    
        elif cmd in {3, 4}:
            reg = int.from_bytes(self.data_packet_save[:2],'little')

            if reg in self.s_x_register_names:
                reg_info = self.s_x_register_names[reg]
                frame_data['reg'] = reg_info["name"]
                cb = reg_info["cb"]
                data_index = 2
            else:                 
                frame_data['reg'] = hex(reg)
            #still want to split into chunks    
            data_str = ''
            for i in range(2,len(self.data_packet_save)):
                if self.base == 10:
                    data_str +=' ' + str(self.data_packet_save[i])
                else:
                    data_str +=' ' + hex(self.data_packet_save[i])
            frame_data['data'] = data_str
            new_frame = AnalyzerFrame("DXL Write", self.frame_start_time, frame.end_time, frame_data)
        elif cmd in {2}:
            # read operation
            reg = int.from_bytes(self.data_packet_save[:2],'little')
            reg_cnt = int.from_bytes(self.data_packet_save[2:4],'little')
            self.last_cmd_reg = reg
            self.last_cmd_reg_cnt = reg_cnt
            if reg in self.s_x_register_names:
                reg_info = self.s_x_register_names[reg]
                frame_data['reg'] = reg_info["name"]
                cb = reg_info["cb"]
                data_index = 2
            else:                 
                frame_data['reg'] = hex(reg)

            frame_data['cnt'] = hex(reg_cnt)    
            new_frame = AnalyzerFrame("DXL Read", self.frame_start_time, frame.end_time, frame_data)
        else:
            data_str = ''
            for i in range(len(self.data_packet_save)):
                if self.base == 10:
                    data_str +=' ' + str(self.data_packet_save[i])
                else:
                    data_str +=' ' + hex(self.data_packet_save[i])
            frame_data['data'] = data_str
            new_frame = AnalyzerFrame("dynamixel", self.frame_start_time, frame.end_time, frame_data)

        if cmd not in {0, 0x55}:
            self.last_cmd = cmd
        return new_frame


    def decode(self, frame: AnalyzerFrame):
        try:
            #ch = frame.data['data'].decode('ascii')
            ch = frame.data['data']
            #ch_val = ch[0]
            print("FS:", str(self.frame_state), "FT: ", frame.type, " ch: ", ch, " ", hex(ch[0]))
        except:
            # Not an ASCII character
            return


        if self.frame_state == 0: # find first 0xff
            if ch == b'\xff':
                self.frame_start_time = frame.start_time
                self.frame_state = 1 
        elif self.frame_state == 1:  # find second 0xff
            if ch == b'\xff':
                self.frame_second_time = frame.start_time
                self.frame_state = 2
            else:
                self.frame_state = 0 # not a packet                
        elif self.frame_state == 2: # ID
            if ch == b'\xff': # can not be 3 in a row...
                self.frame_start_time = self.frame_second_time
                self.frame_second_time = frame.start_time
            else:
                self.servo_id = ch
                self.frame_state = 3                 

        elif self.frame_state == 3: # Length - see if to protocol 2
            if (ch == b'\x00') and (self.servo_id == b'\xfd'):
                self.frame_protocol = 2
                self.frame_state = 20
            else:
                self.frame_protocol = 1
                self.frame_length = ch
                self.frame_state = 4
        elif self.frame_state == 4: # P1 Instruction - see if to protocol 2
            self.frame_cmd = ch
            self.frame_state = 5 # now for the data
            self.data_packet_save = bytearray()

        elif self.frame_state == 5: # P1 data
            self.data_packet_save.extend(ch)
            if ((len(self.data_packet_save)) == (self.frame_length - 2)):
                self.frame_state = 6

        elif self.frame_state == 6: # checksum
            # completed protocol 1
            self.frame_state = 0;
            #wip assume checksum valid to start
            return self.generate_result_frame(frame, 1)
        #
        # Protocol 2
        #
        elif self.frame_state == 20: # ID
            self.servo_id = ch
            self.frame_state = 21                 

        elif self.frame_state == 21: # Length1 - see if to protocol 2
            self.frame_length = int.from_bytes(ch,'big')
            self.frame_state = 22
        elif self.frame_state == 22: # Length1 - see if to protocol 2
            self.frame_length = self.frame_length + (int.from_bytes(ch,'big') * 256)
            self.frame_state = 23
        elif self.frame_state == 23: # P2 Instruction - see if to protocol 2
            self.frame_cmd = ch
            self.frame_state = 24 # now for the data
            self.data_packet_save = bytearray()

        elif self.frame_state == 24: # P2 data
            self.data_packet_save.extend(ch)
            if ((len(self.data_packet_save)) == (self.frame_length - 3)):
                self.frame_state = 25
        elif self.frame_state == 25: # checksum 1
            self.frame_state = 26
        elif self.frame_state == 26: # checksum 1
            # completed protocol 2
            self.frame_state = 0;
            return self.generate_result_frame(frame, 2)

  

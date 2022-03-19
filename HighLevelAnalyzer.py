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

    ChooseServoTypes1 = ChoicesSetting(
        label='Protocol 1 Servo Type',
        choices=('AX Servos (default)', 'MX Servos', 'XL320 Servos', 'X Servos')
    )
    ChooseServoTypes2 = ChoicesSetting(
        label='Protocol 2 Servo Type',
        choices=('X Servos (default)', 'MX Servos')
    )

    ChooseServoController = ChoicesSetting(
        label='Servo Controller',
        choices=('Unknown (default)', 'USB2AX(0xFD)', 'CM730ish(0xC8)')
    )
    ChooseRegisterPairs = ChoicesSetting(
        label='Show Register Pairs as a word',
        choices=('yes', 'no')
    )


    #--------------------------------------------------------------------------
    # Define tables 
    #--------------------------------------------------------------------------
    s_cmd_names = {
        0:"Reply", 1:"Ping", 2:"Read", 3:"Write", 4:"REG_WRITE", 
        5:"Action", 6:"Reset", 8:"Reboot", 0x10:"Clear",
        0x55:"Reply", 0x82:"SRead", 0x83:"SWrite", 0x8a:"FSRead", 
        0x92:"BulkRead", 0x93:"BulkWrite", 0x9A:"FBulkRead" }

    s_result_errors = {
        0:"", 1:"Result", 2:"Instruct", 3:"CRC", 4:"Range",
        5:"Length", 6:"Limit", 7:"Access" }    

    # AX Servos
    s_ax_register_names = {
        0:{"name":"MODEL","cb":2},
        2:{"name":"VER","cb":1},
        3:{"name":"ID","cb":1},
        4:{"name":"BAUD","cb":1},
        5:{"name":"DELAY","cb":1},
        6:{"name":"CWL","cb":2},
        8:{"name":"CCWL","cb":2},
        11:{"name":"LTEMP","cb":1},
        12:{"name":"LVOLTD","cb":1},
        13:{"name":"LVOLTU","cb":1},
        14:{"name":"MTORQUE","cb":2},
        16:{"name":"RLEVEL","cb":1},
        17:{"name":"ALED","cb":1},
        18:{"name":"ASHUT","cb":1},
        24:{"name":"TENABLE","cb":1},
        25:{"name":"LED","cb":1},
        26:{"name":"CWMAR","cb":1},
        27:{"name":"CCWMAR","cb":1},
        28:{"name":"CWSLOPE","cb":1},
        29:{"name":"CCWSLOPE","cb":1},
        30:{"name":"GOAL","cb":2},
        32:{"name":"GSPEED","cb":2},
        34:{"name":"TLIMIT","cb":2},
        36:{"name":"PPOS","cb":2},
        38:{"name":"PSPEED","cb":2},
        40:{"name":"PLOAD","cb":2},
        42:{"name":"PVOLT","cb":1},
        43:{"name":"PTEMP","cb":1},
        44:{"name":"RINST","cb":1},
        46:{"name":"MOVING","cb":1},
        47:{"name":"LOCK","cb":1},
        48:{"name":"PUNCH","cb":2}
    }

    # MX Servos
    s_mx_register_names = {
        0:{"name":"MODEL","cb":2},
        2:{"name":"VER","cb":1},
        3:{"name":"ID","cb":1},
        4:{"name":"BAUD","cb":1},
        5:{"name":"DELAY","cb":1},
        6:{"name":"CWL","cb":2},
        8:{"name":"CCWL","cb":2},
        11:{"name":"LTEMP","cb":1},
        12:{"name":"LVOLTD","cb":1},
        13:{"name":"LVOLTU","cb":1},
        14:{"name":"MTORQUE","cb":2},
        16:{"name":"RLEVEL","cb":1},
        17:{"name":"ALED","cb":1},
        18:{"name":"ASHUT","cb":1},
        20:{"name":"MTOFSET","cb":2},
        22:{"name":"RESD","cb":1},

        24:{"name":"TENABLE","cb":1},
        25:{"name":"LED","cb":1},
        26:{"name":"DGAIN","cb":1},
        27:{"name":"IGAIN","cb":1},
        28:{"name":"PGAIN","cb":1},
        30:{"name":"GOAL","cb":2},
        32:{"name":"GSPEED","cb":2},
        34:{"name":"TLIMIT","cb":2},
        36:{"name":"PPOS","cb":2},
        38:{"name":"PSPEED","cb":2},
        40:{"name":"PLOAD","cb":2},
        42:{"name":"PVOLT","cb":1},
        43:{"name":"PTEMP","cb":1},
        44:{"name":"RINST","cb":1},
        46:{"name":"MOVING","cb":1},
        47:{"name":"LOCK","cb":1},
        48:{"name":"PUNCH","cb":2},
        50:{"name":"RTIXK","cb":2},
        73:{"name":"gACCEL","cb":1}
        }

    # XL Servos
    s_xl320_register_names = {
        0:{"name":"MODEL","cb":2},
        2:{"name":"VER","cb":1},
        3:{"name":"ID","cb":1},
        4:{"name":"BAUD","cb":1},
        5:{"name":"DELAY","cb":1},
        6:{"name":"CWL","cb":2},
        8:{"name":"CCWL","cb":2},
        11:{"name":"CMODE","cb":1},
        12:{"name":"LTEMP","cb":1},
        13:{"name":"LVOLTD","cb":1},
        14:{"name":"LVOLTU","cb":1},
        15:{"name":"MTORQUE","cb":2},
        17:{"name":"RLEVEL","cb":1},
        18:{"name":"ASHUT","cb":1},
        24:{"name":"TENABLE","cb":1},
        25:{"name":"LED","cb":1},
        27:{"name":"DGAIN","cb":1},
        28:{"name":"IGAIN","cb":1},
        29:{"name":"PGAIN","cb":1},
        30:{"name":"GOAL","cb":2},
        32:{"name":"MSPEED","cb":2},
        35:{"name":"TLIMIT","cb":2},
        37:{"name":"PPOS","cb":2},
        39:{"name":"PSPEED","cb":2},
        41:{"name":"PLOAD","cb":2},
        45:{"name":"PVOLT","cb":1},
        46:{"name":"PTEMP","cb":1},
        47:{"name":"RINST","cb":1},
        49:{"name":"MOVING","cb":1},
        50:{"name":"HSTAT","cb":1},
        52:{"name":"PUNCH","cb":2}
    }
 
    s_x_register_names = {
        0:{"name":"MODE#", "cb":2},
        2:{"name":"MODEL", "cb":4},
        6:{"name":"VER", "cb":1},
        7:{"name":"ID", "cb":1},
        8:{"name":"BAUD", "cb":1},
        9:{"name":"DELAY", "cb":1},
        10:{"name":"DMODE", "cb":1},
        11:{"name":"OMODE", "cb":1},
        12:{"name":"S-ID", "cb":1},
        13:{"name":"PROT", "cb":1},
        20:{"name":"HOFF", "cb":4},
        24:{"name":"MOVT", "cb":4},
        31:{"name":"TLIMIT", "cb":1},
        32:{"name":"VMAX", "cb":2},
        34:{"name":"VMIN", "cb":2},
        36:{"name":"PWML", "cb":2},
        40:{"name":"ACCLL", "cb":4},
        44:{"name":"VLMT", "cb":4},
        48:{"name":"MXPOS", "cb":4},
        52:{"name":"MNPOS", "cb":4},
        60:{"name":"SCONFIG", "cb":1},
        63:{"name":"SHUTDN", "cb":1},

        64:{"name":"TENABLE", "cb":1},
        65:{"name":"LED", "cb":1},
        68:{"name":"RETL", "cb":1},
        69:{"name":"RINST", "cb":1},
        70:{"name":"HERR", "cb":1},
        76:{"name":"VIGAIN", "cb":2},
        78:{"name":"VPGAIN", "cb":2},
        80:{"name":"POSDG", "cb":2},
        82:{"name":"POSIG", "cb":2},
        84:{"name":"POSPG", "cb":2},
        88:{"name":"FF2G", "cb":2},
        90:{"name":"FF1G", "cb":2},
        98:{"name":"BWATCH", "cb":1},
        100:{"name":"GPWM", "cb":2},
        104:{"name":"GVEL", "cb":4},
        108:{"name":"GACCL", "cb":4},
        112:{"name":"PVEL", "cb":4},
        116:{"name":"GOAL", "cb":4},
        120:{"name":"RTICK", "cb":2},
        122:{"name":"MOVING", "cb":1},
        123:{"name":"MSTATUS", "cb":1},
        124:{"name":"PPWM", "cb":2},
        126:{"name":"PLOAD", "cb":2},
        128:{"name":"PVEL", "cb":4},
        132:{"name":"PPOS", "cb":4},
        136:{"name":"VELT", "cb":4},
        140:{"name":"POST", "cb":4},
        144:{"name":"PVOLT", "cb":2},
        146:{"name":"PTEMP" , "cb":1},
        147:{"name":"BACKRDY" , "cb":1}
    }

    #USB2AX - probably not needed as does not forward messages on normal AX BUSS
    #CM730(ish) controllers. 
    s_cm730_register_names = {
        0:{"name":"MODEL", "cb":2},
        2:{"name":"VER", "cb":1},
        3:{"name":"ID", "cb":1},
        4:{"name":"BAUD", "cb":1},
        5:{"name":"DELAY", "cb":1},
        12:{"name":"LVOLTD", "cb":1},
        13:{"name":"LVOLTU", "cb":1},
        16:{"name":"RLEVEL", "cb":1},
        24:{"name":"POWER", "cb":1},
        25:{"name":"LPANNEL", "cb":1},
        26:{"name":"LHEAD", "cb":2},
        28:{"name":"LEYE", "cb":2},
        30:{"name":"BUTTON", "cb":1},
        32:{"name":"D1", "cb":1},
        33:{"name":"D2", "cb":1},
        34:{"name":"D3", "cb":1},
        35:{"name":"D4", "cb":1},
        36:{"name":"D5", "cb":1},
        37:{"name":"D6", "cb":1},
        38:{"name":"GYROZ", "cb":2},
        40:{"name":"GYROY", "cb":2},
        42:{"name":"GYROX", "cb":2},
        44:{"name":"ACCX", "cb":2},
        46:{"name":"ACCY", "cb":2},
        48:{"name":"ACCZ", "cb":2},
        50:{"name":"ADC0", "cb":1},
        51:{"name":"ADC1", "cb":2},
        53:{"name":"ADC2", "cb":2},
        55:{"name":"ADC3", "cb":2},
        57:{"name":"ADC4", "cb":2},
        59:{"name":"ADC5", "cb":2},
        61:{"name":"ADC6", "cb":2},
        63:{"name":"ADC7", "cb":2},
        65:{"name":"ADC8", "cb":2},
        67:{"name":"ADC9", "cb":2},
        69:{"name":"ADC10", "cb":2},
        71:{"name":"ADC11", "cb":2},
        73:{"name":"ADC12", "cb":1},
        75:{"name":"ADC13", "cb":1},
        77:{"name":"ADC14", "cb":1},
        79:{"name":"ADC15", "cb":1},
    }

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'DXL Error': {'format': 'Error {{data.cmd}} ID:{{data.id}}'},
        'DXL Ping': {'format': '{{data.cmd}} ID:{{data.id}}'},
        'DXL Action': {'format': '{{data.cmd}} ID:{{data.id}}'},
        'DXL Reset': {'format': '{{data.cmd}} ID:{{data.id}}'},
        'DXL Reboot': {'format': '{{data.cmd}} ID:{{data.id}}'},
        'DXL Write': {'format': '{{data.cmd}} ID:{{data.id}} R:{{data.reg}} = {{data.data}}'},    
        'DXL SWrite': {'format': '{{data.cmd}} ID:{{data.id}} R:{{data.reg}} #{{data.cnt}} = {{data.data}}'},
        'DXL Read': {'format': '{{data.cmd}} ID:{{data.id}} R:{{data.reg}} #{{data.cnt}}'},
        'DXL Reply': {'format': '{{data.cmd}} ID:{{data.id}}'},
        'DXL ReplyE': {'format': '{{data.cmd}} ID:{{data.id}} Err:{{data.err}}'},
        'DXL ReplyD': {'format': '{{data.cmd}} ID:{{data.id}} = {{data.data}}'},
        'DXL ReplyDE': {'format': '{{data.cmd}} ID:{{data.id}} Err:{{data.err}} = {{data.data}}'},
        'DXL BulkW': { 'format': 'ID:{{data.id}} {{data.cmd}} {{data.data}}' },
        'DXL BulkR': { 'format': 'ID:{{data.id}} {{data.cmd}} {{data.data}}' },
        'dxl ???': { 'format': 'ID:{{data.id}} {{data.cmd}} {{data.data}}' }
    }


    #--------------------------------------------------------------------------
    # Class Init function 
    #--------------------------------------------------------------------------
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
        self.last_char_end_time = 0
        self.packet_timeout_char_count = 3
        self.frame_end_time = None
        self.servo_id = None
        self.frame_protocol = 1
        self.frame_length = 0
        self.checksum = 0
        self.crc = 0
        self.crcFirstByte = 0
        self.frame_cmd = None
        self.data_packet_save = None
        self.last_cmd = None
        self.last_cmd_reg = 999
        self.last_cmd_reg_cnt = None
        self.bulk_read_info = None;
        self.ServoNameTable = None
        self.frame_state = '1stFF'
        self.frame_data = {}

        #--------------------------------------------------------------------------
        # Define dispatch tables for processing differnt packets.
        #--------------------------------------------------------------------------
        self.decodeDispatch = {
            '1stFF': self.decode1stFF,
            '2ndFF': self.decode2ndFF,
            'id': self.decocodeID,
            'len1': self.decodeLen1,
            # start Protocol 1 specific
            'p1_inst': self.decodeP1_Inst,
            'p1_data': self.decodeP1_data,
            'p1_chksum': self.decodeP1_chksum,
            # start Protocol 2 specific
            'p2_id': self.decodeP2_ID,
            'p2_len1': self.decodeP2_Len1,
            'p2_len2': self.decodeP2_Len2,
            'p2_inst': self.decodeP2_Inst,
            'p2_data': self.decodeP2_data,
            'p2_crc1': self.decodeP2_crc1,
            'p2_crc2': self.decodeP2_crc2
        }

        self.processP1Packets = {
            0: self.ProcessProt1_Response,
            1: self.ProcessProt1_Ping,
            2: self.ProcessProt1_Read,
            3: self.ProcessProt1_Write,
            4: self.ProcessProt1_RegWrite,
            5: self.ProcessProt1_Action,
            6: self.ProcessProt1_FactoryReset,
            8: self.ProcessProt1_Reboot,
            0x83: self.ProcessProt1_SyncWrite,
            0x92: self.ProcessProt1_BulkRead
        }

        self.processP2Packets = {
            0x55: self.ProcessProt2_Response,
            1: self.ProcessProt2_Ping,
            2: self.ProcessProt2_Read,
            3: self.ProcessProt2_Write,
            4: self.ProcessProt2_RegWrite,
            5: self.ProcessProt2_Action,
            6: self.ProcessProt2_FactoryReset,
            8: self.ProcessProt2_Reboot,
            0x10: self.ProcessProt2_Clear,
            0x20: self.ProcessProt2_Backup,
            0x82: self.ProcessProt2_SyncRead,
            0x83: self.ProcessProt2_SyncWrite,
            #0x8A: self.ProcessProt2_FastSyncRead,
            0x92: self.ProcessProt2_BulkRead,
            0x93: self.ProcessProt2_BulkWrite,
            #0x9A: self.ProcessProt2_FastBulkRead,
        }

        print("Settings:", self.ChooseServoTypes1, self.ChooseServoTypes2,
              self.ChooseRegisterPairs, self.ChooseServoController)

    def UpdateServoNamesTable(self): 
        if self.frame_protocol == 1:
            if self.ChooseServoTypes1 == 'MX Servos':
               self.ServoNameTable = self.s_mx_register_names
            elif self.ChooseServoTypes1 == 'XL320 Servos':
                self.ServoNameTable = self.s_xl320_register_names
            else:
                self.ServoNameTable = self.s_ax_register_names
        else:
            if self.ChooseServoTypes2 == 'MX Servos':
                self.ServoNameTable = self.s_mx_register_names
            elif self.ChooseServoTypes2 == 'XL320 Servos':
                self.ServoNameTable = s_xl320_register_names
            else:
                self.ServoNameTable = self.s_x_register_names

    def generate_data_string(self, start_index, reg_count):
        reg =  self.last_cmd_reg
        i = start_index
        data_str = ''
        if reg_count > 0:
            reg_end = start_index + reg_count
            if reg_end > len(self.data_packet_save):
                reg_end = len(self.data_packet_save)
        else:    
            reg_end = len(self.data_packet_save)
        while i < reg_end:
            cb_reg = 1

            if reg in self.ServoNameTable:
                reg_info = self.ServoNameTable[reg]
                #frame_data['reg'] = reg_info["name"]
                cb_reg = reg_info["cb"]

            if cb_reg > 1:
                val = int.from_bytes(self.data_packet_save[i:i+cb_reg],'little')
                if self.base == 16:
                    data_str +=' ' + hex(val)
                else:
                    data_str +=' ' + str(val)
            else:
                if self.base == 10:
                    data_str +=' ' + str(self.data_packet_save[i])
                else:
                    data_str +=' ' + hex(self.data_packet_save[i])
            i += cb_reg
            reg += cb_reg
        return data_str

    def generate_sw_data_string(self, start_index, cnt_per_servo):
        i = start_index
        data_str = ''
        while i < len(self.data_packet_save):
            #get the servo ID
            if self.base == 10:
                data_str +=' ' + str(self.data_packet_save[i]) + ':'
            else:
                data_str +=' ' + hex(self.data_packet_save[i]) + ':'

            i += 1
            servo_byte_index = 0
            reg =  self.last_cmd_reg
            while (i < len(self.data_packet_save)) and (servo_byte_index < cnt_per_servo):
                cb_reg = 1

                if reg in self.ServoNameTable:
                    reg_info = self.ServoNameTable[reg]
                    #frame_data['reg'] = reg_info["name"]
                    cb_reg = reg_info["cb"]

                if cb_reg > 1:
                    val = int.from_bytes(self.data_packet_save[i:i+cb_reg],'little')
                    if self.base == 16:
                        data_str +=' ' + hex(val)
                    else:
                        data_str +=' ' + str(val)
                else:
                    if self.base == 10:
                        data_str +=' ' + str(self.data_packet_save[i])
                    else:
                        data_str +=' ' + hex(self.data_packet_save[i])
                i += cb_reg
                reg += cb_reg
                servo_byte_index += cb_reg
        return data_str

#================================================
# dispatch Process Protocol 1 Messages 
#================================================
    def ProcessProt1_unknown(self, frame: AnalyzerFrame, cmd):
        data_str = ''
        for i in range(len(self.data_packet_save)):
            if self.base == 10:
                data_str +=' ' + str(self.data_packet_save[i])
            else:
                data_str +=' ' + hex(self.data_packet_save[i])
        self.frame_data['data'] = data_str
        return AnalyzerFrame("dxl ???", self.frame_start_time, frame.end_time, self.frame_data)


    def ProcessProt1_Response(self, frame: AnalyzerFrame, cmd):
        err_str = ''
        if cmd == 0:
            self.frame_data['err'] = ''
        else:
            if (err & 0x01) != 0:
                err_str += 'Volt '
            if (err & 0x02) != 0:
                err_str += 'Angle '
            if (err & 0x04) != 0:
                err_str += 'Temp '
            if (err & 0x08) != 0:
                err_str += 'Range '
            if (err & 0x010) != 0:
                err_str += 'Checksum '
            if (err & 0x020) != 0:
                err_str += 'Overload '
            if (err & 0x040) != 0:
                err_str += 'Checksum '
            self.frame_data['err'] = 'Alert'
        if (len(self.data_packet_save) == 0):
            if err_str == '':
                print("  DXL Reply ID:", self.frame_data['id'])
                new_frame = AnalyzerFrame("DXL Reply", self.frame_start_time, frame.end_time, self.frame_data)
            else:
                print("  DXL Reply ID:", self.frame_data['id'], " Err:", self.frame_data['err'])
                new_frame = AnalyzerFrame("DXL ReplyE", self.frame_start_time, frame.end_time, self.frame_data)
        else:
            data_str = self.generate_data_string(0, -1)
            self.frame_data['data'] = data_str
            if err_str == '':
                print("  DXL Reply ID:", self.frame_data['id'], " Data:", data_str)
                new_frame = AnalyzerFrame("DXL ReplyD", self.frame_start_time, frame.end_time, self.frame_data)
            else:    
                print("  DXL Reply ID:", self.frame_data['id'], " Err:", self.frame_data['err'], " Data:", data_str)
                new_frame = AnalyzerFrame("DXL ReplyDE", self.frame_start_time, frame.end_time, self.frame_data)
        return new_frame

    def ProcessProt1_Ping(self, frame: AnalyzerFrame, cmd):
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("DXL Ping", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt1_Read(self, frame: AnalyzerFrame, cmd):
        if len(self.data_packet_save) < 2:
            return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)

        reg = self.data_packet_save[0]
        reg_cnt = self.data_packet_save[1]
        self.last_cmd_reg = reg
        self.last_cmd_reg_cnt = reg_cnt
        if reg in self.ServoNameTable:
            reg_info = self.ServoNameTable[reg]
            self.frame_data['reg'] = reg_info["name"]
            cb = reg_info["cb"]
        else:                 
            self.frame_data['reg'] = hex(reg)

        self.frame_data['cnt'] = hex(reg_cnt)    
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id'], " Reg:", self.frame_data['reg'], 
            " Cnt:", self.frame_data['cnt'])
        return AnalyzerFrame("DXL Read", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt1_Write(self, frame: AnalyzerFrame, cmd):
        # simple write/reg swrite
        if len(self.data_packet_save) < 1:
            return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)
        reg = self.data_packet_save[0]
        data_index = 1

        if reg in self.ServoNameTable:
            reg_info = self.ServoNameTable[reg]
            self.frame_data['reg'] = reg_info["name"]
            cb = reg_info["cb"]
        else:                 
            self.frame_data['reg'] = hex(reg)
        #still want to split into chunks    
        data_str = ''
        for i in range(data_index,len(self.data_packet_save)):
            if self.base == 10:
                data_str +=' ' + str(self.data_packet_save[i])
            else:
                data_str +=' ' + hex(self.data_packet_save[i])
        self.frame_data['data'] = data_str
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id'], " Reg:", self.frame_data['reg'], 
            " Data:", data_str)
        return AnalyzerFrame("DXL Write", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt1_RegWrite(self, frame: AnalyzerFrame, cmd):
        return self.ProcessProt1_Write(frame, cmd)

    def ProcessProt1_Action(self, frame: AnalyzerFrame, cmd):
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("DXL Action", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt1_FactoryReset(self, frame: AnalyzerFrame, cmd):
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("DXL Reset", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt1_Reboot(self, frame: AnalyzerFrame, cmd):
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("DXL Reboot", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt1_SyncWrite(self, frame: AnalyzerFrame, cmd):
        if len(self.data_packet_save) < 2:
            return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)
        reg = self.data_packet_save[0]
        reg_cnt = self.data_packet_save[1]
        self.last_cmd_reg = reg
        self.last_cmd_reg_cnt = reg_cnt

        if reg in self.ServoNameTable:
            reg_info = self.ServoNameTable[reg]
            self.frame_data['reg'] = reg_info["name"]
        else:                 
            self.frame_data['reg'] = hex(reg)
        self.frame_data['cnt'] = hex(reg_cnt)    
        data_str = self.generate_sw_data_string(2, reg_cnt)
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id'], " Reg:", self.frame_data['reg'], 
            " Cnt:", self.frame_data['cnt'])
        print("\tData: ", data_str)
        self.frame_data['data'] = data_str
        return AnalyzerFrame("DXL SWrite", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt1_BulkRead(self, frame: AnalyzerFrame, cmd):
        return self.ProcessProt1_unknown(frame, cmd)
#================================================
# dispatch Process Protocol 2 Messages 
#================================================
    def ProcessProt2_unknown(self, frame: AnalyzerFrame, cmd):
        data_str = ''
        for i in range(len(self.data_packet_save)):
            if self.base == 10:
                data_str +=' ' + str(self.data_packet_save[i])
            else:
                data_str +=' ' + hex(self.data_packet_save[i])
        self.frame_data['data'] = data_str
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("dxl ???", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_Response(self, frame: AnalyzerFrame, cmd):
        #reply
        if len(self.data_packet_save) < 1:
            return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)
        err = self.data_packet_save[0]
        if (err & 0x80) != 0:
            self.frame_data['err'] = 'Alert'
        elif err in self.s_result_errors:
            self.frame_data['err'] = self.s_result_errors[err]
        else:    
            self.frame_data['err'] = self.data_packet_save[0]

        #special case Ping commands
        data_str = ''
        if (self.last_cmd == 1) and (len(self.data_packet_save) >= 4):
            # returns 2 bytes model# and 1 byte firmware version
            model_num = int.from_bytes(self.data_packet_save[1:3],'little')
            firmware_ver = self.data_packet_save[3]
            if self.base == 10:
                data_str = 'model:' + str(model_num) + ' Ver:' + str(firmware_ver)
            else:
                data_str = 'model:' + hex(model_num) + ' Ver:' + hex(firmware_ver)
        elif self.last_cmd == 0x92:
            # bulk read response
            if self.servo_id[0] in self.bulk_read_info:
                bri = self.bulk_read_info[self.servo_id[0]]
                print(bri)
                self.last_cmd_reg = bri['reg']
                self.last_cmd_reg_cnt = bri['#']
            data_str = self.generate_data_string(1, -1)                    
        else:
            data_str = self.generate_data_string(1, -1)
        
        self.frame_data['data'] = data_str
        if (data_str == ''):
            if err == 0:
                print("  DXL Reply ID:", self.frame_data['id'])
                new_frame = AnalyzerFrame("DXL Reply", self.frame_start_time, frame.end_time, self.frame_data)
            else:
                print("  DXL Reply ID:", self.frame_data['id'], " Err:", self.frame_data['err'])
                new_frame = AnalyzerFrame("DXL ReplyE", self.frame_start_time, frame.end_time, self.frame_data)
        else:
            if err == 0:
                print("  DXL Reply ID:", self.frame_data['id'], " Data:", data_str)
                new_frame = AnalyzerFrame("DXL ReplyD", self.frame_start_time, frame.end_time, self.frame_data)
            else:    
                print("  DXL Reply ID:", self.frame_data['id'], " Err:", self.frame_data['err'], " Data:", data_str)
                new_frame = AnalyzerFrame("DXL ReplyDE", self.frame_start_time, frame.end_time, self.frame_data)
        return new_frame

    def ProcessProt2_Ping(self, frame: AnalyzerFrame, cmd):
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("DXL Ping", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_Read(self, frame: AnalyzerFrame, cmd):
        if len(self.data_packet_save) < 4:
            return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)
        reg = int.from_bytes(self.data_packet_save[:2],'little')
        reg_cnt = int.from_bytes(self.data_packet_save[2:4],'little')
        self.last_cmd_reg = reg
        self.last_cmd_reg_cnt = reg_cnt
        if reg in self.ServoNameTable:
            reg_info = self.ServoNameTable[reg]
            self.frame_data['reg'] = reg_info["name"]
            cb = reg_info["cb"]
        else:                 
            self.frame_data['reg'] = hex(reg)

        self.frame_data['cnt'] = hex(reg_cnt)    
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id'], " Reg:", self.frame_data['reg'], 
            " Cnt:", self.frame_data['cnt'])
        return AnalyzerFrame("DXL Read", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_Write(self, frame: AnalyzerFrame, cmd):
        # simple write/reg swrite
        if len(self.data_packet_save) < 2:
            return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)
        reg = int.from_bytes(self.data_packet_save[:2],'little')
        data_index = 2

        if reg in self.ServoNameTable:
            reg_info = self.ServoNameTable[reg]
            self.frame_data['reg'] = reg_info["name"]
            cb = reg_info["cb"]
        else:                 
            self.frame_data['reg'] = hex(reg)
        #still want to split into chunks    
        data_str = ''
        for i in range(data_index,len(self.data_packet_save)):
            if self.base == 10:
                data_str +=' ' + str(self.data_packet_save[i])
            else:
                data_str +=' ' + hex(self.data_packet_save[i])
        self.frame_data['data'] = data_str
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id'], " Reg:", self.frame_data['reg'], 
            " Data:", data_str)
        return AnalyzerFrame("DXL Write", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_RegWrite(self, frame: AnalyzerFrame, cmd):
        return self.ProcessProt2_Write(frame, cmd)

    def ProcessProt2_Action(self, frame: AnalyzerFrame, cmd):
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("DXL Action", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_FactoryReset(self, frame: AnalyzerFrame, cmd):
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("DXL Reset", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_Reboot(self, frame: AnalyzerFrame, cmd):
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id']) 
        return AnalyzerFrame("DXL Reboot", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_SyncWrite(self, frame: AnalyzerFrame, cmd):
        if len(self.data_packet_save) < 4:
            return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)
        reg = int.from_bytes(self.data_packet_save[:2],'little')
        reg_cnt = int.from_bytes(self.data_packet_save[2:4],'little')
        self.last_cmd_reg = reg
        self.last_cmd_reg_cnt = reg_cnt

        if reg in self.ServoNameTable:
            reg_info = self.ServoNameTable[reg]
            self.frame_data['reg'] = reg_info["name"]
        else:                 
            self.frame_data['reg'] = hex(reg)
        self.frame_data['cnt'] = hex(reg_cnt)    
        data_str = self.generate_sw_data_string(4, reg_cnt)
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id'], " Reg:", self.frame_data['reg'], 
            " Cnt:", self.frame_data['cnt'])
        print("\tData: ", data_str)
        self.frame_data['data'] = data_str
        return AnalyzerFrame("DXL SWrite", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_SyncRead(self, frame: AnalyzerFrame, cmd):
        return self.ProcessProt2_unknown(frame, cmd)

    def ProcessProt2_BulkRead(self, frame: AnalyzerFrame, cmd):
        param_index = 0
        data_len = len(self.data_packet_save)
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id'], " Reg:")
        complete_data_str = ''
        self.bulk_read_info = {}
        while param_index < data_len:
            # make sure we have enough bytes to get the initial data for servo
            if (data_len - param_index) < 5:
                return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)
            servo_id = self.data_packet_save[param_index]
            reg = int.from_bytes(self.data_packet_save[param_index+1:param_index+3],'little')
            reg_cnt = int.from_bytes(self.data_packet_save[param_index+3:param_index+5],'little')
            self.last_cmd_reg = reg
            self.last_cmd_reg_cnt = reg_cnt
            param_index += 5 # we used up those bytes

            if reg in self.ServoNameTable:
                reg_info = self.ServoNameTable[reg]
                reg_str = reg_info["name"]
            else:                 
                reg_str = hex(reg)

            print("\tID:", str(servo_id),' Reg:',reg_str, " Cnt: ",str(reg_cnt))
            complete_data_str += ' ' + str(servo_id) + '(' + reg_str + ', ' + str(reg_cnt) + '):'
            self.bulk_read_info[servo_id] = {"reg":reg, "#":reg_cnt}
        self.frame_data['data'] = complete_data_str
        return AnalyzerFrame("DXL BulkR", self.frame_start_time, frame.end_time, self.frame_data)

    def ProcessProt2_BulkWrite(self, frame: AnalyzerFrame, cmd):
        param_index = 0
        data_len = len(self.data_packet_save)
        print("DXL ", self.frame_data['cmd'], " ID:", self.frame_data['id'], " Reg:")
        complete_data_str = ''
        while param_index < data_len:
            # make sure we have enough bytes to get the initial data for servo
            if (data_len - param_index) < 5:
                return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)
            servo_id = self.data_packet_save[param_index]
            reg = int.from_bytes(self.data_packet_save[param_index+1:param_index+3],'little')
            reg_cnt = int.from_bytes(self.data_packet_save[param_index+3:param_index+5],'little')
            self.last_cmd_reg = reg
            self.last_cmd_reg_cnt = reg_cnt
            param_index += 5 # we used up those bytes
            if (data_len - param_index) < reg_cnt:
                return AnalyzerFrame("DXL Error", self.frame_start_time, frame.end_time, self.frame_data)

            if reg in self.ServoNameTable:
                reg_info = self.ServoNameTable[reg]
                reg_str = reg_info["name"]
            else:                 
                reg_str = hex(reg)
            data_str = self.generate_data_string(param_index, reg_cnt)
    
            print("\tID:", str(servo_id),' Reg:',reg_str, " Data: ",data_str)
            complete_data_str += ' ' + str(servo_id) + '(' + reg_str + '):' + data_str
            param_index += reg_cnt
        self.frame_data['data'] = complete_data_str
        return AnalyzerFrame("DXL BulkW", self.frame_start_time, frame.end_time, self.frame_data)


    def ProcessProt2_Clear(self, frame: AnalyzerFrame, cmd):
        return self.ProcessProt2_unknown(frame, cmd)

    def ProcessProt2_Backup(self, frame: AnalyzerFrame, cmd):
        return self.ProcessProt2_unknown(frame, cmd)

#================================================
# dispatch decode functions 
#================================================
    def decode1stFF(self, frame: AnalyzerFrame, ch):
        if ch == b'\xff':
            self.frame_start_time = frame.start_time
            self.frame_state = '2ndFF'
            self.crc = 0
            self.crcFirstByte = 0
            self.update_crc(ch)

    def decode2ndFF(self, frame: AnalyzerFrame, ch):
        if ch == b'\xff':
            self.update_crc(ch)
            self.frame_second_time = frame.start_time
            self.frame_state = 'id'
        else:
            self.frame_state = '1stFF' # not a packet                

    def decocodeID(self, frame: AnalyzerFrame, ch):
        if ch == b'\xff': # can not be 3 in a row...
            self.frame_start_time = self.frame_second_time
            self.frame_second_time = frame.start_time
        else:
            self.servo_id = ch
            self.frame_state = 'len1'                 
            self.checksum = ch[0]
            self.update_crc(ch)

    def decodeLen1(self, frame: AnalyzerFrame, ch):
        self.checksum += ch[0]
        if (ch == b'\x00') and (self.servo_id == b'\xfd'):
            self.frame_protocol = 2
            self.frame_state = 'p2_id'
            self.update_crc(ch)
        else:
            self.frame_protocol = 1
            self.frame_length = ch[0]
            self.frame_state = 'p1_inst'

    def decodeP1_Inst(self, frame: AnalyzerFrame, ch):
        self.frame_cmd = ch
        self.data_packet_save = bytearray()
        self.checksum += ch[0]
        if self.frame_length == 2:
            self.frame_state = 'p1_chksum' # There is no data...
        else:    
            self.frame_state = 'p1_data' # now for the data


    def decodeP1_data(self, frame: AnalyzerFrame, ch):
        self.data_packet_save.extend(ch)
        self.checksum += ch[0]
        if ((len(self.data_packet_save)) == (self.frame_length - 2)):
            self.frame_state = 'p1_chksum'

    def decodeP1_chksum(self, frame: AnalyzerFrame, ch):
        # completed protocol 1
        self.frame_state = '1stFF'
        new_frame = None
        
        self.UpdateServoNamesTable()
        cmd = self.frame_cmd[0]
        self.frame_data = {}
        self.frame_data['id'] = str(self.servo_id[0])
        self.frame_data['protocol'] = '1'

        # check for checksum errors
        computed_checksum = (~(self.checksum & 0xff)) & 0xff
        if computed_checksum != ch[0]:
            print(">> Checksum error Computed:", hex(computed_checksum), " Read:", hex(ch[0]))
            self.frame_data["chksum"] = hex(computed_checksum) + "!=" + hex(ch[0])

        if cmd in self.s_cmd_names:
            self.frame_data['cmd'] = self.s_cmd_names[cmd]
        else:
            self.frame_data['cmd'] = ''.join([ '0x', hex(cmd).upper()[2:] ])

        if cmd in self.processP1Packets:
            new_frame = self.processP1Packets[cmd](frame, cmd)
        else:
             new_frame = self.ProcessProt1_unknown(frame, cmd)

        if cmd != 0:
            self.last_cmd = cmd
        return new_frame
    #
    # Protocol 2
    #
    def decodeP2_ID(self, frame: AnalyzerFrame, ch):
        self.servo_id = ch
        self.frame_state = 'p2_len1'                 
        self.update_crc(ch)

    def decodeP2_Len1(self, frame: AnalyzerFrame, ch):
        self.frame_length = ch[0]
        self.frame_state = 'p2_len2'
        self.update_crc(ch)

    def decodeP2_Len2(self, frame: AnalyzerFrame, ch):
        self.frame_length += ch[0] * 256
        self.frame_state = 'p2_inst'
        self.update_crc(ch)

    def decodeP2_Inst(self, frame: AnalyzerFrame, ch):
        self.frame_cmd = ch
        if self.frame_length == 3:
            self.frame_state = 'p2_crc1' # There is no data...
        else:    
            self.frame_state = 'p2_data' # now for the data
        self.data_packet_save = bytearray()
        self.update_crc(ch)

    def decodeP2_data(self, frame: AnalyzerFrame, ch):
        self.data_packet_save.extend(ch)
        if ((len(self.data_packet_save)) == (self.frame_length - 3)):
            self.frame_state = 'p2_crc1'
        self.update_crc(ch)

    def decodeP2_crc1(self, frame: AnalyzerFrame, ch):
        self.crcFirstByte = ch[0]
        self.frame_state = 'p2_crc2'

    def decodeP2_crc2(self, frame: AnalyzerFrame, ch):
        # completed protocol 2
        self.frame_state = '1stFF'
        #now lets try to dispatch the processing here
                # use dispatch table to run the decoding of the packets.
        new_frame = None
        self.UpdateServoNamesTable()
        cmd = self.frame_cmd[0]
        self.frame_data = {}

        read_crc = ((ch[0] << 8) | self.crcFirstByte) & 0xffff
        if self.crc != read_crc:           
            print(">> CRC error Computed:", hex(self.crc), " Read:", hex(read_crc))
            self.frame_data["crc"] = hex(self.crc) + "!=" + hex(read_crc)

        self.frame_data['id'] = str(self.servo_id[0])
        self.frame_data['protocol'] = '2'

        if cmd in self.s_cmd_names:
            self.frame_data['cmd'] = self.s_cmd_names[cmd]
        else:
            self.frame_data['cmd'] = ''.join([ '0x', hex(cmd).upper()[2:] ])

        if cmd in self.processP2Packets:
            new_frame = self.processP2Packets[cmd](frame, cmd)
        else:
             new_frame = self.ProcessProt2_unknown(frame, cmd)

        # Don't update last command if reply as may be many if for example ping
        if cmd != 0x55:
            self.last_cmd = cmd
        return new_frame     

#==========================================================================================
# Protocol 2 stuff. 
    crc_table = [
        0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
        0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
        0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
        0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
        0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
        0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
        0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
        0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
        0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
        0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
        0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
        0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
        0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
        0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
        0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
        0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
        0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
        0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
        0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
        0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
        0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
        0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
        0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
        0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
        0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
        0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
        0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
        0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
        0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
        0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
        0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
        0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
    ]

    def update_crc(self, ch):
        i = ((self.crc >> 8) ^ ch[0]) & 0xFF
        self.crc = ((self.crc << 8) ^ self.crc_table[i]) & 0xffff


#================================================
#  Main decode function
#================================================
    def decode(self, frame: AnalyzerFrame):
        try:
            #ch = frame.data['data'].decode('ascii')
            ch = frame.data['data']
            #ch_val = ch[0]
            #print("FS:", self.frame_state, "FT: ", frame.type, " ch: ", ch, " ", hex(ch[0]))
        except:
            # Not an ASCII character
            return

        # lets add in a timeout if there is too much of a gap between characters
        if self.frame_state != '1stFF':
            char_time = float(frame.end_time - frame.start_time)
            char_gap = float(frame.start_time - self.last_char_end_time)
            if char_gap > (self.packet_timeout_char_count * char_time):
                print("$$ packet timeout")
                self.frame_state = '1stFF'
        self.last_char_end_time = frame.end_time  

        # use dispatch table to run the decoding of the packets.
        if self.frame_state in self.decodeDispatch:
            return self.decodeDispatch[self.frame_state](frame, ch)
        else:
            print("Unknown decode state: ", frame_state)

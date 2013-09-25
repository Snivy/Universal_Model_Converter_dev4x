from data.COMMON import * #essentials
imgHeader(0.001,
          ( 'COMMONIMG', ['png'] ),
          [])

#the image handling system is still very much in the design process,
#and is currently not used. (only verified)
#functions written in here may not be implamented in UMC yet.

def DecodeImage(FT):
    #TODO: only reads (doesn't verify)
    #the updated logger will tell if there's an error
    
    
    
    SIG = bh_(8,'',' -- signature')
    
    while 1:
        length=bu32(label=' -- data-length')
        Type = string(4,label=' -- type')

        

        #character case
        #0 - CRITICAL   | not-critical
        #1 - PUBLIC     | private
        #2 - RESERVED   | not-recognized
        #3 - CHECK      | safe
        #(CHECK means to look for modifications that have
        # not touched any critical chunks)

        switch(Type)
        if case('IHDR'): #always first
            bu32(label=' -- width')
            bu32(label=' -- height')
            bu8(label=' -- bit-depth')
            bu8(label=' -- colour-type')
            bu8(label=' -- compression-type')
            bu8(label=' -- filter-type')
            bu8(label=' -- interlace-type')
            
        if case('PLTE'):
            StructArr(['u8','u8','u8'],length/3)
            
        if case('IDAT'): bu_(length, ' -- image data')
        if case('bkGD'): bu_(length, ' -- background color')
        if case('cHRM'): bu_(length, ' -- chromanence')
        if case('gAMA'): bu_(length, ' -- gamma correction')
        if case('hIST'): bu_(length, ' -- histogram')
        if case('iCCP'): bu_(length, ' -- ')
        if case('iTXt'): bu_(length, ' -- ')
        if case('pHYs'): bu_(length, ' -- ')
        if case('sPLT'): bu_(length, ' -- ')
        if case('sRGB'): bu_(length, ' -- ')
        if case('sTER'): bu_(length, ' -- sterioscopic data')
        if case('tEXt'): bu_(length, ' -- text data')
        if case('tIME'): bu_(length, ' -- ')
        if case('tRNS'): bu_(length, ' -- transparency data')
        if case('zTXt'): bu_(length, ' -- zlib compressed text data')

        CRC = bh32(label=' -- CRC')

        from zlib import crc32
        VER = struct.pack('!I', crc32(C_data,crc32(C_type)) & (2 ** 32 - 1) )
        
        if CRC != VER:
                # print repr(checksum)
                (a,) = struct.unpack('!I', checksum)
                (b,) = struct.unpack('!I', verify)
                raise ChunkError(
                  "Checksum error in %s chunk: 0x%08X != 0x%08X." %
                  (type, a, b))
            
        if Type=='IEND': break #always last
        
    return data

def EncodeImage(FT):
    bh_(8,'89504E470D0A1A0A',' -- signature')
